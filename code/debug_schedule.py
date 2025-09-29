from app import app
from extensions import db
from models import Teacher, Course, Room, TimeSlot, Schedule, TeacherAvailability
from timetable.generator import generate_timetable
import datetime

with app.app_context():
    print("\n=== DEBUGGING SCHEDULE GENERATION ===\n")
    
    # Check if we have the necessary data
    teachers = Teacher.query.all()
    courses = Course.query.all()
    rooms = Room.query.all()
    timeslots = TimeSlot.query.all()
    
    print(f"Found {len(teachers)} teachers, {len(courses)} courses, {len(rooms)} rooms, {len(timeslots)} timeslots")
    
    if not teachers or not courses or not rooms or not timeslots:
        print("ERROR: Missing essential data. Make sure you have teachers, courses, rooms, and timeslots.")
        exit(1)
    
    # Check teacher availabilities
    for teacher in teachers:
        availabilities = TeacherAvailability.query.filter_by(teacher_id=teacher.id).all()
        print(f"Teacher {teacher.name} has {len(availabilities)} availabilities")
        if not availabilities:
            print(f"WARNING: Teacher {teacher.name} has no availabilities defined.")
    
    # Check course-teacher assignments
    for course in courses:
        if course.teacher_id:
            teacher = Teacher.query.get(course.teacher_id)
            print(f"Course {course.code} assigned to {teacher.name if teacher else 'Unknown teacher'}")
        else:
            print(f"WARNING: Course {course.code} has no assigned teacher.")
    
    # Clear existing test schedules
    test_semester = "Debug Test"
    Schedule.query.filter_by(semester=test_semester).delete()
    db.session.commit()
    
    # Generate a new schedule
    print("\nGenerating test schedule...")
    schedule_items = generate_timetable(courses, rooms, timeslots, teachers)
    
    print(f"Generated {len(schedule_items)} schedule items")
    
    # Save to database
    if schedule_items:
        for item in schedule_items:
            print(f"Adding: Course ID {item['course_id']}, Room ID {item['room_id']}, TimeSlot ID {item['time_slot_id']}")
            schedule = Schedule(
                course_id=item['course_id'],
                room_id=item['room_id'],
                time_slot_id=item['time_slot_id'],
                semester=test_semester
            )
            db.session.add(schedule)
        
        db.session.commit()
        print("Schedule saved to database")
        
        # Verify the saved schedule
        saved_schedules = Schedule.query.filter_by(semester=test_semester).all()
        print(f"Found {len(saved_schedules)} saved schedule entries")
        
        for schedule in saved_schedules:
            course = Course.query.get(schedule.course_id)
            room = Room.query.get(schedule.room_id)
            timeslot = TimeSlot.query.get(schedule.time_slot_id)
            
            if course and room and timeslot:
                days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                day_name = days[timeslot.day_of_week] if 0 <= timeslot.day_of_week < 7 else f"Unknown({timeslot.day_of_week})"
                print(f"Schedule: {course.code} in {room.name} on {day_name} at {timeslot.start_time.strftime('%H:%M')}-{timeslot.end_time.strftime('%H:%M')}")
            else:
                print(f"WARNING: Incomplete schedule entry: Course ID {schedule.course_id}, Room ID {schedule.room_id}, TimeSlot ID {schedule.time_slot_id}")
    else:
        print("ERROR: No schedule items were generated!")
    
    print("\n=== DEBUG COMPLETE ===\n")
