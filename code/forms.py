from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, TimeField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from models import User, Teacher, Course, Room

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class TeacherForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    department = StringField('Department')
    submit = SubmitField('Submit')

class TeacherAvailabilityForm(FlaskForm):
    day_of_week = SelectField('Day of Week', choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'),
                                                     (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'),
                                                     (6, 'Sunday')], coerce=int)
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    submit = SubmitField('Add Availability')

class CourseForm(FlaskForm):
    code = StringField('Course Code', validators=[DataRequired()])
    name = StringField('Course Name', validators=[DataRequired()])
    teacher = SelectField('Teacher', coerce=int)
    credit_hours = IntegerField('Credit Hours', default=3)
    sessions_per_week = IntegerField('Sessions Per Week', default=1)
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.teacher.choices = [(t.id, t.name) for t in Teacher.query.all()]

class RoomForm(FlaskForm):
    name = StringField('Room Name', validators=[DataRequired()])
    capacity = IntegerField('Capacity')
    has_projector = BooleanField('Has Projector')
    building = StringField('Building')
    submit = SubmitField('Submit')

class TimeSlotForm(FlaskForm):
    day_of_week = SelectField('Day of Week', choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'),
                                                     (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'),
                                                     (6, 'Sunday')], coerce=int)
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    submit = SubmitField('Add Time Slot')

class GenerateScheduleForm(FlaskForm):
    semester = StringField('Semester (e.g., "Fall 2023")', validators=[DataRequired()])
    submit = SubmitField('Generate Timetable')
