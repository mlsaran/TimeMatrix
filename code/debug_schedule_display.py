from app import app
from extensions import db
from models import Teacher, Course, Room, TimeSlot, Schedule, TeacherAvailability
import traceback

with app.app_context():
    print("\n=== DEBUGGING SCHEDULE DISPLAY ISSUE ===\n")
    
    # Get all schedules in the database
    schedules = Schedule.query.all()
    print(f"Found {len(schedules)} schedule entries total")
    
    if not schedules:
        print("No schedules found. Try running debug_schedule.py first.")
        exit(1)
    
    # Examine each schedule entry in detail
    for idx, schedule in enumerate(schedules):
        print(f"\nSchedule #{idx+1} (ID: {schedule.id}):")
        print(f"  Course ID: {schedule.course_id}")
        print(f"  Room ID: {schedule.room_id}")
        print(f"  TimeSlot ID: {schedule.time_slot_id}")
        print(f"  Semester: {schedule.semester}")
        
        # Check each relationship
        try:
            course = Course.query.get(schedule.course_id)
            if course:
                print(f"  Course: {course.code} - {course.name}")
                if course.teacher_id:
                    teacher = Teacher.query.get(course.teacher_id)
                    if teacher:
                        print(f"  Teacher: {teacher.name}")
                    else:
                        print("  Teacher: Not found (invalid teacher_id in course)")
                else:
                    print("  Teacher: None assigned (course.teacher_id is None)")
            else:
                print("  Course: Not found (invalid course_id in schedule)")
        except Exception as e:
            print(f"  ERROR retrieving course data: {str(e)}")
            traceback.print_exc()
            
        try:
            room = Room.query.get(schedule.room_id)
            if room:
                print(f"  Room: {room.name}")
            else:
                print("  Room: Not found (invalid room_id in schedule)")
        except Exception as e:
            print(f"  ERROR retrieving room data: {str(e)}")
            traceback.print_exc()
            
        try:
            time_slot = TimeSlot.query.get(schedule.time_slot_id)
            if time_slot:
                days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                day_name = days[time_slot.day_of_week] if 0 <= time_slot.day_of_week < 7 else f"Invalid day ({time_slot.day_of_week})"
                print(f"  TimeSlot: {day_name} {time_slot.start_time}-{time_slot.end_time}")
            else:
                print("  TimeSlot: Not found (invalid time_slot_id in schedule)")
        except Exception as e:
            print(f"  ERROR retrieving time_slot data: {str(e)}")
            traceback.print_exc()
