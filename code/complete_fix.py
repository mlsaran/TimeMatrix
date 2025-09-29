from app import app
from extensions import db
from models import User, Teacher, Course, Room, TimeSlot, Schedule, TeacherAvailability
import datetime
import traceback


with app.app_context():
    print("\n=== COMPREHENSIVE DATABASE FIX ===\n")
    
    try:
        # 1. Identify the issue
        print("Diagnosing current database state...")
        
        schedules = Schedule.query.all()
        print(f"Found {len(schedules)} schedules in database")
        
        for idx, schedule in enumerate(schedules):
            print(f"\nSchedule #{idx+1} (ID: {schedule.id}):")
            print(f"  Course ID: {schedule.course_id}")
            print(f"  Room ID: {schedule.room_id}")
            print(f"  TimeSlot ID: {schedule.time_slot_id}")
            print(f"  Semester: {schedule.semester}")
            
            # Check if the related objects exist
            course = Course.query.get(schedule.course_id)
            room = Room.query.get(schedule.room_id)
            timeslot = TimeSlot.query.get(schedule.time_slot_id)
            
            print(f"  Course exists: {bool(course)}")
            print(f"  Room exists: {bool(room)}")
            print(f"  TimeSlot exists: {bool(timeslot)}")
            
            if timeslot:
                print(f"  TimeSlot day: {timeslot.day_of_week}")
                print(f"  TimeSlot time: {timeslot.start_time}-{timeslot.end_time}")
        
        # 2. Drop and recreate all tables
        print("\nRecreating database schema...")
        db.drop_all()
        db.create_all()
        
        # 3. Create sample data
        print("\nCreating sample data...")
        
        # Create admin user
        admin = User(username='admin', email='admin@example.com')
        admin.set_password('password')
        db.session.add(admin)
        
        # Create teachers
        teacher1 = Teacher(name='John Smith', email='john@example.com', department='Computer Science')
        teacher2 = Teacher(name='Jane Doe', email='jane@example.com', department='Mathematics')
        db.session.add(teacher1)
        db.session.add(teacher2)
        db.session.commit()
        
        # Create teacher availability
        avail1 = TeacherAvailability(
            teacher_id=teacher1.id,
            day_of_week=0,  # Monday
            start_time=datetime.time(9, 0),
            end_time=datetime.time(12, 0)
        )
        avail2 = TeacherAvailability(
            teacher_id=teacher1.id,
            day_of_week=1,  # Tuesday
            start_time=datetime.time(14, 0),
            end_time=datetime.time(17, 0)
        )
        avail3 = TeacherAvailability(
            teacher_id=teacher2.id,
            day_of_week=0,  # Monday
            start_time=datetime.time(13, 0),
            end_time=datetime.time(16, 0)
        )
        db.session.add_all([avail1, avail2, avail3])
        
        # Create courses
        course1 = Course(
            code='CS101',
            name='Introduction to Programming',
            teacher_id=teacher1.id,
            credit_hours=3,
            sessions_per_week=2
        )
        course2 = Course(
            code='MATH201',
            name='Calculus I',
            teacher_id=teacher2.id,
            credit_hours=4,
            sessions_per_week=2
        )
        db.session.add_all([course1, course2])
        
        # Create rooms
        room1 = Room(
            name='A101',
            capacity=30,
            has_projector=True,
            building='Main Building'
        )
        room2 = Room(
            name='B205',
            capacity=25,
            has_projector=True,
            building='Science Building'
        )
        db.session.add_all([room1, room2])
        
        # Create time slots
        ts1 = TimeSlot(
            day_of_week=0,  # Monday
            start_time=datetime.time(9, 0),
            end_time=datetime.time(10, 30)
        )
        ts2 = TimeSlot(
            day_of_week=0,  # Monday
            start_time=datetime.time(11, 0),
            end_time=datetime.time(12, 30)
        )
        ts3 = TimeSlot(
            day_of_week=1,  # Tuesday
            start_time=datetime.time(14, 0),
            end_time=datetime.time(15, 30)
        )
        db.session.add_all([ts1, ts2, ts3])
        
        # Commit everything so far
        db.session.commit()
        
        # 4. Create a sample schedule
        print("\nCreating a sample schedule...")
        
        # Create a new schedule with valid relationships
        schedule1 = Schedule(
            course_id=course1.id,
            room_id=room1.id,
            time_slot_id=ts1.id,
            semester="Sample Semester"
        )
        schedule2 = Schedule(
            course_id=course2.id,
            room_id=room2.id,
            time_slot_id=ts2.id,
            semester="Sample Semester"
        )
        schedule3 = Schedule(
            course_id=course1.id,
            room_id=room2.id,
            time_slot_id=ts3.id,
            semester="Sample Semester"
        )
        db.session.add_all([schedule1, schedule2, schedule3])
        db.session.commit()
        
        # 5. Verify the schedule entries
        print("\nVerifying the new schedule entries...")
        
        new_schedules = Schedule.query.all()
        print(f"Created {len(new_schedules)} new schedule entries")
        
        for idx, schedule in enumerate(new_schedules):
            print(f"\nNew Schedule #{idx+1} (ID: {schedule.id}):")
            
            # Use the relationships directly
            try:
                print(f"  Course: {schedule.course.code if schedule.course else 'None'}")
                print(f"  Room: {schedule.room.name if schedule.room else 'None'}")
                print(f"  TimeSlot: Day {schedule.time_slot.day_of_week if schedule.time_slot else 'None'}, " +
                      f"Time {schedule.time_slot.start_time.strftime('%H:%M')}-{schedule.time_slot.end_time.strftime('%H:%M') if schedule.time_slot else 'None'}")
                print(f"  Teacher: {schedule.course.teacher.name if schedule.course and schedule.course.teacher else 'None'}")
                print("  All relationships working correctly!")
            except Exception as e:
                print(f"  ERROR accessing relationships: {str(e)}")
                traceback.print_exc()
        
        print("\n=== DATABASE RESET AND FIXED SUCCESSFULLY ===\n")
        print("You can now run the application and the schedule should display correctly.")
        print("Login with username 'admin' and password 'password'")
    
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        traceback.print_exc()
        print("\nFix operation failed. Please check the error message.")
