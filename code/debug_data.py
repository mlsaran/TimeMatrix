from app import app, db
from models import Teacher, Course, Room, TimeSlot, TeacherAvailability, Schedule

with app.app_context():
    # Check teachers
    teachers = Teacher.query.all()
    print(f"Found {len(teachers)} teachers:")
    for t in teachers:
        print(f"  - {t.name} (ID: {t.id})")
        availabilities = TeacherAvailability.query.filter_by(teacher_id=t.id).all()
        if availabilities:
            print(f"    Has {len(availabilities)} availability records")
            for a in availabilities:
                days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                print(f"    - {days[a.day_of_week]} {a.start_time} - {a.end_time}")
        else:
            print(f"    WARNING: No availability records!")
    
    # Check courses
    courses = Course.query.all()
    print(f"\nFound {len(courses)} courses:")
    for c in courses:
        teacher = "None" if c.teacher_id is None else f"{c.teacher.name} (ID: {c.teacher_id})"
        print(f"  - {c.code}: {c.name}, Teacher: {teacher}, Sessions: {c.sessions_per_week}")
    
    # Check rooms
    rooms = Room.query.all()
    print(f"\nFound {len(rooms)} rooms:")
    for r in rooms:
        print(f"  - {r.name} (ID: {r.id}), Capacity: {r.capacity}")
    
    # Check timeslots
    timeslots = TimeSlot.query.all()
    print(f"\nFound {len(timeslots)} timeslots:")
    for t in timeslots:
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        print(f"  - ID: {t.id}, {days[t.day_of_week]} {t.start_time} - {t.end_time}")
    
    # Check schedules
    schedules = Schedule.query.all()
    print(f"\nFound {len(schedules)} schedule entries:")
    for s in schedules:
        try:
            print(f"  - Course: {s.course.code}, Room: {s.room.name}, Day: {days[s.time_slot.day_of_week]}, Time: {s.time_slot.start_time}-{s.time_slot.end_time}, Semester: {s.semester}")
        except Exception as e:
            print(f"  - ERROR reading schedule entry {s.id}: {str(e)}")
