from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from models import Course, Room, TimeSlot, Schedule, Teacher, TeacherAvailability
from forms import TimeSlotForm, GenerateScheduleForm
from extensions import db
from timetable.generator import generate_timetable
import traceback

schedules_bp = Blueprint('schedules', __name__, url_prefix='/schedules')

@schedules_bp.route('/')
@login_required
def list_schedules():
    try:
        # Get all semesters that have schedules
        semesters = db.session.query(Schedule.semester).distinct().all()
        semesters = [s[0] for s in semesters]
        
        print(f"Available semesters: {semesters}")
        
        # If no schedules exist yet, show a message
        if not semesters:
            flash('No schedules have been generated yet. Create one now!', 'info')
            return render_template('schedules/list.html', 
                               title='Schedules', 
                               schedules=[], 
                               semesters=[], 
                               selected_semester=None,
                               days=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
        
        # Get the selected semester from query parameters or use the first one
        selected_semester = request.args.get('semester', semesters[0])
        print(f"Selected semester: {selected_semester}")
        
        # Get all schedules for the selected semester
        schedules = Schedule.query.filter_by(semester=selected_semester).all()
        print(f"Found {len(schedules)} schedule entries for semester {selected_semester}")
        
        # Check if time slots exist for each schedule
        for schedule in schedules:
            # Get the time slot for each schedule
            time_slot = TimeSlot.query.get(schedule.time_slot_id)
            if time_slot:
                print(f"Schedule {schedule.id} has time slot on day {time_slot.day_of_week} at {time_slot.start_time}-{time_slot.end_time}")
            else:
                print(f"Schedule {schedule.id} has no time slot!")
        
        return render_template('schedules/list.html', 
                          title='Schedules', 
                          schedules=schedules, 
                          semesters=semesters, 
                          selected_semester=selected_semester,
                          days=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    
    except Exception as e:
        traceback.print_exc()
        flash(f"An error occurred: {str(e)}", "danger")
        return render_template('schedules/list.html', 
                          title='Schedules Error', 
                          schedules=[], 
                          semesters=semesters if 'semesters' in locals() else [], 
                          selected_semester=selected_semester if 'selected_semester' in locals() else None,
                          days=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

@schedules_bp.route('/timeslots', methods=['GET', 'POST'])
@login_required
def manage_timeslots():
    form = TimeSlotForm()
    if form.validate_on_submit():
        timeslot = TimeSlot(
            day_of_week=form.day_of_week.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data
        )
        db.session.add(timeslot)
        db.session.commit()
        flash('Time slot added successfully!', 'success')
        return redirect(url_for('schedules.manage_timeslots'))
    
    timeslots = TimeSlot.query.order_by(TimeSlot.day_of_week, TimeSlot.start_time).all()
    return render_template('schedules/timeslots.html', title='Time Slots', form=form, timeslots=timeslots)

@schedules_bp.route('/timeslots/delete/<int:id>')
@login_required
def delete_timeslot(id):
    timeslot = TimeSlot.query.get_or_404(id)
    db.session.delete(timeslot)
    db.session.commit()
    flash('Time slot deleted successfully!', 'success')
    return redirect(url_for('schedules.manage_timeslots'))

@schedules_bp.route('/generate', methods=['GET', 'POST'])
@login_required
def generate_schedule():
    form = GenerateScheduleForm()
    if form.validate_on_submit():
        try:
            # Clear existing schedules for this semester
            existing = Schedule.query.filter_by(semester=form.semester.data).count()
            print(f"Deleting {existing} existing schedules for semester {form.semester.data}")
            Schedule.query.filter_by(semester=form.semester.data).delete()
            
            # Fetch data needed for schedule generation
            courses = Course.query.all()
            rooms = Room.query.all()
            timeslots = TimeSlot.query.all()
            teachers = Teacher.query.all()
            
            print(f"Starting schedule generation with: {len(courses)} courses, {len(rooms)} rooms, {len(timeslots)} timeslots, {len(teachers)} teachers")
            
            # Make sure we have data to work with
            if not courses:
                flash('Error: No courses found. Add courses before generating a schedule.', 'danger')
                return redirect(url_for('courses.list_courses'))
            
            if not rooms:
                flash('Error: No rooms found. Add rooms before generating a schedule.', 'danger')
                return redirect(url_for('rooms.list_rooms'))
                
            if not timeslots:
                flash('Error: No time slots found. Add time slots before generating a schedule.', 'danger')
                return redirect(url_for('schedules.manage_timeslots'))
                
            if not teachers:
                flash('Error: No teachers found. Add teachers before generating a schedule.', 'danger')
                return redirect(url_for('teachers.list_teachers'))
            
            # Check if teachers have availability
            teachers_without_availability = []
            for teacher in teachers:
                availabilities = TeacherAvailability.query.filter_by(teacher_id=teacher.id).count()
                if availabilities == 0:
                    teachers_without_availability.append(teacher.name)
            
            if teachers_without_availability:
                flash(f'Error: Some teachers have no availability set: {", ".join(teachers_without_availability)}', 'danger')
                return redirect(url_for('teachers.list_teachers'))
            
            # Check if courses have teachers assigned
            courses_without_teachers = []
            for course in courses:
                if not course.teacher_id:
                    courses_without_teachers.append(course.code)
            
            if courses_without_teachers:
                flash(f'Error: Some courses have no teacher assigned: {", ".join(courses_without_teachers)}', 'danger')
                return redirect(url_for('courses.list_courses'))
            
            # Generate the new schedule
            schedule_items = generate_timetable(courses, rooms, timeslots, teachers)
            
            # Save generated schedule to database
            if schedule_items:
                for item in schedule_items:
                    schedule = Schedule(
                        course_id=item['course_id'],
                        room_id=item['room_id'],
                        time_slot_id=item['time_slot_id'],
                        semester=form.semester.data
                    )
                    db.session.add(schedule)
                
                db.session.commit()
                flash(f'Schedule generated successfully with {len(schedule_items)} sessions!', 'success')
            else:
                flash('Could not generate a schedule. Check teacher availabilities and course requirements.', 'danger')
            
            return redirect(url_for('schedules.list_schedules', semester=form.semester.data))
            
        except Exception as e:
            traceback.print_exc()
            flash(f"An error occurred during schedule generation: {str(e)}", "danger")
            return redirect(url_for('schedules.generate_schedule'))
    
    return render_template('schedules/generate.html', title='Generate Schedule', form=form)
