def check_teacher_conflict(schedule, new_item):
    """
    Check if adding a new schedule item would create a teacher conflict.
    """
    for item in schedule:
        if (item['time_slot_id'] == new_item['time_slot_id'] and 
            item['course'].teacher_id == new_item['course'].teacher_id):
            return True
    return False

def check_room_conflict(schedule, new_item):
    """
    Check if adding a new schedule item would create a room conflict.
    """
    for item in schedule:
        if (item['time_slot_id'] == new_item['time_slot_id'] and 
            item['room_id'] == new_item['room_id']):
            return True
    return False

def check_teacher_availability(teacher_id, timeslot, availabilities):
    """
    Check if a teacher is available at a given timeslot based on their availability.
    """
    for availability in availabilities:
        if (availability.teacher_id == teacher_id and
            availability.day_of_week == timeslot.day_of_week and
            availability.start_time <= timeslot.start_time and
            availability.end_time >= timeslot.end_time):
            return True
    return False
