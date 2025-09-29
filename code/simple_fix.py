from app import app
from extensions import db
from models import User, Teacher, Course, Room, TimeSlot, Schedule, TeacherAvailability
import datetime
import traceback

with app.app_context():
    print("\n=== SIMPLE DATABASE FIX ===\n")
    
    try:
        # Recreate the entire database
        print("Dropping all tables...")
        db.drop_all()
        
        print("Creating all tables...")
        db.create_all()
        
        # Create admin user
        print("Creating admin user...")
        admin = User(username='admin', email='admin@example.com')
        admin.set_password('password')
        db.session.add(admin)
        db.session.commit()
        
        # Create sample data
        print("Creating sample data...")
        
        # 1. Create teachers
        teacher1 = Teacher(name='John Smith', email='john@example.com', department='Computer Science')
        teacher2 = Teacher(name='Jane Doe', email='jane@example.com', department='Mathematics')
        db.session.add_all([teacher1, teacher2])
        db.session.commit()
        
        # 2. Add availability
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
        db.session.commit()
        
        # 3. Create courses
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
        db.session.commit()
        
        # 4. Create rooms
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
        db.session.commit()
        
        # 5. Create time slots
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
        db.session.commit()
        
        # 6. Create a sample schedule
        print("Creating sample schedule...")
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
        
        print("\nDatabase reset complete. You can now run the application.")
        print("Login with username 'admin' and password 'password'")
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        traceback.print_exc()
        print("Fix operation failed. Please check the error message.")
