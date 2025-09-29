from app import app
from extensions import db
from models import Teacher, Course, Room, TimeSlot, Schedule, TeacherAvailability
import traceback

with app.app_context():
    print("\n=== FIXING DATABASE RELATIONSHIPS ===\n")
    
    # Get all schedules
    schedules = Schedule.query.all()
    
    if not schedules:
        print("No schedules found. Nothing to fix.")
        exit(0)
        
    print(f"Found {len(schedules)} schedules to check")
    
    # Check and fix each schedule
    for schedule in schedules:
        print(f"Checking schedule ID {schedule.id}...")
        
        # Check course relationship
        course = Course.query.get(schedule.course_id)
        if not course:
            print(f"  ERROR: Course ID {schedule.course_id} does not exist")
            continue
            
        # Check room relationship
        room = Room.query.get(schedule.room_id)
        if not room:
            print(f"  ERROR: Room ID {schedule.room_id} does not exist")
            continue
            
        # Check time_slot relationship
        time_slot = TimeSlot.query.get(schedule.time_slot_id)
        if not time_slot:
            print(f"  ERROR: TimeSlot ID {schedule.time_slot_id} does not exist")
            continue
        
        print(f"  All relationships valid for schedule ID {schedule.id}")
    
    # Fix relationship mappings by recreating the schedules
    print("\nRecreating schedules with proper relationships...")
    
    # Get all data
    try:
        # Create a backup of all existing schedules
        backup_schedules = []
        for schedule in schedules:
            backup_schedules.append({
                'course_id': schedule.course_id,
                'room_id': schedule.room_id,
                'time_slot_id': schedule.time_slot_id,
                'semester': schedule.semester,
                'created_at': schedule.created_at
            })
        
        # Delete all existing schedules
        print(f"Deleting {len(schedules)} existing schedule entries...")
        db.session.query(Schedule).delete()
        
        # Recreate the schedules
        print("Recreating schedules...")
        for data in backup_schedules:
            # Validate the references
            course = Course.query.get(data['course_id'])
            room = Room.query.get(data['room_id'])
            time_slot = TimeSlot.query.get(data['time_slot_id'])
            
            if course and room and time_slot:
                # Create a new schedule entry
                schedule = Schedule(
                    course_id=data['course_id'],
                    room_id=data['room_id'],
                    time_slot_id=data['time_slot_id'],
                    semester=data['semester'],
                    created_at=data['created_at']
                )
                db.session.add(schedule)
                print(f"  Recreated schedule: Course {course.code} in Room {room.name} at {time_slot.start_time.strftime('%H:%M')}")
            else:
                print(f"  Skipping invalid schedule: Course ID {data['course_id']}, Room ID {data['room_id']}, TimeSlot ID {data['time_slot_id']}")
        
        # Commit changes
        db.session.commit()
        print("Schedules recreated successfully!")
        
    except Exception as e:
        db.session.rollback()
        print(f"ERROR during recreation: {str(e)}")
        traceback.print_exc()
    
    print("\n=== RELATIONSHIPS FIXED ===\n")
