from app import app
from extensions import db
from models import Teacher, Course, Room, TimeSlot, Schedule, TeacherAvailability

with app.app_context():
    print("\n=== VIEWING ALL SCHEDULE ENTRIES ===\n")
    
    # Get all schedules
    schedules = Schedule.query.all()
    
    if not schedules:
        print("No schedules found.")
        exit(0)
        
    print(f"Found {len(schedules)} total schedules")
    
    # Group schedules by semester
    semesters = {}
    for schedule in schedules:
        if schedule.semester not in semesters:
            semesters[schedule.semester] = []
        semesters[schedule.semester].append(schedule)
    
    # Display schedules by semester
    for semester, semester_schedules in semesters.items():
        print(f"\nSCHEDULES FOR {semester} ({len(semester_schedules)} entries):")
        
        # Group by day of week
        days = [[] for _ in range(7)]
        for schedule in semester_schedules:
            try:
                time_slot = TimeSlot.query.get(schedule.time_slot_id)
                if time_slot and 0 <= time_slot.day_of_week < 7:
                    days[time_slot.day_of_week].append(schedule)
                else:
                    print(f"  Invalid time slot for schedule ID {schedule.id}")
            except Exception as e:
                print(f"  Error processing schedule ID {schedule.id}: {str(e)}")
        
        # Display schedules by day
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day_idx, day_schedules in enumerate(days):
            if day_schedules:
                print(f"\n  {day_names[day_idx]} ({len(day_schedules)} entries):")
                
                # Sort by start time
                sorted_schedules = sorted(day_schedules, key=lambda s: TimeSlot.query.get(s.time_slot_id).start_time)
                
                for schedule in sorted_schedules:
                    course = Course.query.get(schedule.course_id)
                    room = Room.query.get(schedule.room_id)
                    time_slot = TimeSlot.query.get(schedule.time_slot_id)
                    
                    if course and room and time_slot:
                        teacher = Teacher.query.get(course.teacher_id) if course.teacher_id else None
                        teacher_name = teacher.name if teacher else "No teacher"
                        
                        print(f"    {time_slot.start_time.strftime('%H:%M')}-{time_slot.end_time.strftime('%H:%M')}: {course.code} ({course.name}) with {teacher_name} in {room.name}")
                    else:
                        print(f"    Invalid schedule ID {schedule.id}: missing course, room, or time_slot")
