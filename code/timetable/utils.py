def get_day_name(day_number):
    """
    Convert day number (0-6) to day name.
    """
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return days[day_number]

def format_time(time_obj):
    """
    Format time object to string.
    """
    return time_obj.strftime('%H:%M')

def get_schedule_by_day(schedules):
    """
    Group schedules by day for easier rendering in templates.
    """
    result = {}
    for schedule in schedules:
        day = schedule.time_slot.day_of_week
        if day not in result:
            result[day] = []
        result[day].append(schedule)
    
    # Sort each day's schedules by start time
    for day in result:
        result[day].sort(key=lambda s: s.time_slot.start_time)
    
    return result
