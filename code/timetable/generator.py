import random
from datetime import time
from models import Teacher, TeacherAvailability, Course, Room, TimeSlot
from extensions import db

def generate_timetable(courses, rooms, timeslots, teachers):
    """
    Generate a timetable based on courses, rooms, timeslots and teachers.
    Returns a list of dictionaries containing schedule assignments.
    """
    print(f"Starting timetable generation with {len(courses)} courses, {len(rooms)} rooms, {len(timeslots)} timeslots")
    
    # List to store the generated schedule
    schedule = []
    
    # Track used timeslots for each room and teacher
    used_room_slots = {}  # room_id -> set of timeslot_ids
    used_teacher_slots = {}  # teacher_id -> set of timeslot_ids
    
    # Initialize tracking dictionaries
    for room in rooms:
        used_room_slots[room.id] = set()
    for teacher in teachers:
        used_teacher_slots[teacher.id] = set()
    
    # Create availability lookup for teachers
    teacher_availability = {}
    for teacher in teachers:
        available_slots = []
        availabilities = TeacherAvailability.query.filter_by(teacher_id=teacher.id).all()
        print(f"Teacher {teacher.name} has {len(availabilities)} availability records")
        
        for timeslot in timeslots:
            # Check if timeslot falls within any of the teacher's availability windows
            for avail in availabilities:
                if (avail.day_of_week == timeslot.day_of_week and
                    avail.start_time <= timeslot.start_time and
                    avail.end_time >= timeslot.end_time):
                    available_slots.append(timeslot.id)
                    break
        
        teacher_availability[teacher.id] = set(available_slots)
        print(f"Teacher {teacher.name} is available for {len(teacher_availability[teacher.id])} timeslots")
    
    # Sort courses by constraints (number of sessions, specific requirements)
    sorted_courses = sorted(courses, key=lambda c: c.sessions_per_week, reverse=True)
    
    # Assign courses to rooms and timeslots
    for course in sorted_courses:
        # Skip if the course has no teacher assigned
        if not course.teacher_id:
            print(f"Skipping course {course.code}: no teacher assigned")
            continue
        
        # Get available timeslots for this teacher
        available_teacher_slots = teacher_availability.get(course.teacher_id, set())
        print(f"Course {course.code} teacher has {len(available_teacher_slots)} available slots")
        
        # Schedule each session for this course
        for session in range(course.sessions_per_week):
            assigned = False
            
            # Try random room and timeslot combinations until one works
            possible_slots = []
            for room in rooms:
                for timeslot_id in available_teacher_slots:
                    # Skip if this room or teacher is already booked for this timeslot
                    if (timeslot_id in used_room_slots[room.id] or 
                        timeslot_id in used_teacher_slots[course.teacher_id]):
                        continue
                    possible_slots.append((room.id, timeslot_id))
            
            # If we found possible slots, randomly choose one
            if possible_slots:
                room_id, timeslot_id = random.choice(possible_slots)
                
                # Mark this timeslot as used for this room and teacher
                used_room_slots[room_id].add(timeslot_id)
                used_teacher_slots[course.teacher_id].add(timeslot_id)
                
                # Add to schedule
                schedule.append({
                    'course_id': course.id,
                    'room_id': room_id,
                    'time_slot_id': timeslot_id
                })
                assigned = True
                print(f"Assigned course {course.code} session {session+1} to room {room_id}, timeslot {timeslot_id}")
            
            # If we couldn't assign a slot for this session, log it
            if not assigned:
                print(f"WARNING: Could not assign a slot for course {course.code} session {session+1}")
    
    print(f"Generated schedule with {len(schedule)} sessions")
    return schedule
