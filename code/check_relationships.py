from app import app
from extensions import db
from models import Teacher, Course, Room, TimeSlot, Schedule, TeacherAvailability

with app.app_context():
    print("\n=== CHECKING DATABASE RELATIONSHIPS ===\n")
    
    # Check Schedules
    schedules = Schedule.query.all()
    print(f"Found {len(schedules)} schedule entries")
    
    if schedules:
        sample = schedules[0]
        print(f"Sample Schedule ID: {sample.id}")
        print(f"  Course ID: {sample.course_id}")
        print(f"  Room ID: {sample.room_id}")
        print(f"  TimeSlot ID: {sample.time_slot_id}")
        print(f"  Semester: {sample.semester}")
        
        # Test relationships
        try:
            course = Course.query.get(sample.course_id)
            print(f"  Related Course: {course.code if course else 'None'}")
        except Exception as e:
            print(f"  ERROR accessing course: {str(e)}")
        
        try:
            room = Room.query.get(sample.room_id)
            print(f"  Related Room: {room.name if room else 'None'}")
        except Exception as e:
            print(f"  ERROR accessing room: {str(e)}")
        
        try:
            timeslot = TimeSlot.query.get(sample.time_slot_id)
            if timeslot:
                days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                day_name = days[timeslot.day_of_week] if 0 <= timeslot.day_of_week < 7 else f"Unknown({timeslot.day_of_week})"
                print(f"  Related TimeSlot: {day_name} {timeslot.start_time}-{timeslot.end_time}")
            else:
                print("  Related TimeSlot: None")
        except Exception as e:
            print(f"  ERROR accessing time_slot: {str(e)}")
    
    # Check Course to Teacher relationship
    courses = Course.query.all()
    print(f"\nFound {len(courses)} courses")
    
    if courses:
        sample = courses[0]
        print(f"Sample Course: {sample.code}")
        print(f"  Teacher ID: {sample.teacher_id}")
        try:
            teacher = Teacher.query.get(sample.teacher_id)
            print(f"  Related Teacher: {teacher.name if teacher else 'None'}")
        except Exception as e:
            print(f"  ERROR accessing teacher: {str(e)}")
    
    print("\n=== RELATIONSHIP CHECK COMPLETE ===\n")
