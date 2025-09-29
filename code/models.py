from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from extensions import db, login_manager

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    department = db.Column(db.String(100))
    
    # Define relationships explicitly
    availabilities = db.relationship('TeacherAvailability', backref='teacher', lazy='dynamic', cascade="all, delete-orphan")
    courses = db.relationship('Course', backref='teacher', lazy='dynamic')
    
    def __repr__(self):
        return f'<Teacher {self.name}>'

class TeacherAvailability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id', ondelete='CASCADE'), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0=Monday, 6=Sunday
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    
    def __repr__(self):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_name = days[self.day_of_week] if 0 <= self.day_of_week < 7 else f"Unknown({self.day_of_week})"
        return f'<Availability {self.teacher.name}: {day_name} {self.start_time}-{self.end_time}>'

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    credit_hours = db.Column(db.Integer, default=3)
    sessions_per_week = db.Column(db.Integer, default=1)
    
    # Define schedules relationship
    schedules = db.relationship('Schedule', backref='course_ref', lazy='dynamic', cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Course {self.code}: {self.name}>'

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer)
    has_projector = db.Column(db.Boolean, default=False)
    building = db.Column(db.String(50))
    
    # Define schedules relationship
    schedules = db.relationship('Schedule', backref='room_ref', lazy='dynamic', cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Room {self.name}>'

class TimeSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0=Monday, 6=Sunday
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    
    # Define schedules relationship
    schedules = db.relationship('Schedule', backref='time_slot_ref', lazy='dynamic', cascade="all, delete-orphan")
    
    def __repr__(self):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_name = days[self.day_of_week] if 0 <= self.day_of_week < 7 else f"Unknown({self.day_of_week})"
        return f'<TimeSlot {day_name}: {self.start_time.strftime("%H:%M")}-{self.end_time.strftime("%H:%M")}>'

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    time_slot_id = db.Column(db.Integer, db.ForeignKey('time_slot.id'), nullable=False)
    semester = db.Column(db.String(20))  # e.g., "Fall 2023"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Schedule {self.id}: Course {self.course_id} in Room {self.room_id} at TimeSlot {self.time_slot_id}>'
