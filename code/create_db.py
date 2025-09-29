from app import app
from extensions import db
from models import User, Teacher, Course, Room, TimeSlot, Schedule, TeacherAvailability
import datetime

with app.app_context():
    print("Dropping existing tables...")
    db.drop_all()
    
    print("Creating database tables...")
    db.create_all()
    
    # Create admin user
    admin = User(username='admin', email='admin@example.com')
    admin.set_password('password')
    db.session.add(admin)
    db.session.commit()
    print("Admin user created!")
    
    # Create sample data (optional)
    # 1. Create teachers
    teacher1 = Teacher(name='John Smith', email='john@example.com', department='Computer Science')
    teacher2 = Teacher(name='Jane Doe', email='jane@example.com', department='Mathematics')
    db.session.add(teacher1)
    db.session.add(teacher2)
    db.session.commit()
    print("Sample teachers created!")
    
    # 2. Add availability for teachers
    # Monday 9:00-12:00 for John
    avail1 = TeacherAvailability(
        teacher_id=teacher1.id,
        day_of_week=0,  # Monday
        start_time=datetime.time(9, 0),
        end_time=datetime.time(12, 0)
    )
    # Tuesday 14:00-17:00 for John
    avail2 = TeacherAvailability(
        teacher_id=teacher1.id,
        day_of_week=1,  # Tuesday
        start_time=datetime.time(14, 0),
        end_time=datetime.time(17, 0)
    )
    # Monday 13:00-16:00 for Jane
    avail3 = TeacherAvailability(
        teacher_id=teacher2.id,
        day_of_week=0,  # Monday
        start_time=datetime.time(13, 0),
        end_time=datetime.time(16, 0)
    )
    db.session.add_all([avail1, avail2, avail3])
    db.session.commit()
    print("Teacher availabilities created!")
    
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
    print("Sample courses created!")
    
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
    print("Sample rooms created!")
    
    # 5. Create time slots
    # Monday 9:00-10:30
    ts1 = TimeSlot(
        day_of_week=0,
        start_time=datetime.time(9, 0),
        end_time=datetime.time(10, 30)
    )
    # Monday 11:00-12:30
    ts2 = TimeSlot(
        day_of_week=0,
        start_time=datetime.time(11, 0),
        end_time=datetime.time(12, 30)
    )
    # Monday 14:00-15:30
    ts3 = TimeSlot(
        day_of_week=0,
        start_time=datetime.time(14, 0),
        end_time=datetime.time(15, 30)
    )
    # Tuesday 14:00-15:30
    ts4 = TimeSlot(
        day_of_week=1,
        start_time=datetime.time(14, 0),
        end_time=datetime.time(15, 30)
    )
    # Tuesday 16:00-17:30
    ts5 = TimeSlot(
        day_of_week=1,
        start_time=datetime.time(16, 0),
        end_time=datetime.time(17, 30)
    )
    db.session.add_all([ts1, ts2, ts3, ts4, ts5])
    db.session.commit()
    print("Sample time slots created!")
    
    print("Database initialized with sample data!")
