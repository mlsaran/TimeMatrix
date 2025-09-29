from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from models import Course, Teacher
from forms import CourseForm
from extensions import db

courses_bp = Blueprint('courses', __name__, url_prefix='/courses')

@courses_bp.route('/')
@login_required
def list_courses():
    courses = Course.query.all()
    return render_template('courses/list.html', title='Courses', courses=courses)

@courses_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_course():
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(
            code=form.code.data,
            name=form.name.data,
            teacher_id=form.teacher.data,
            credit_hours=form.credit_hours.data,
            sessions_per_week=form.sessions_per_week.data
        )
        db.session.add(course)
        db.session.commit()
        flash('Course added successfully!')
        return redirect(url_for('courses.list_courses'))
    
    return render_template('courses/add.html', title='Add Course', form=form)

@courses_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_course(id):
    course = Course.query.get_or_404(id)
    form = CourseForm(obj=course)
    if form.validate_on_submit():
        course.code = form.code.data
        course.name = form.name.data
        course.teacher_id = form.teacher.data
        course.credit_hours = form.credit_hours.data
        course.sessions_per_week = form.sessions_per_week.data
        db.session.commit()
        flash('Course updated successfully!')
        return redirect(url_for('courses.list_courses'))
    
    # Pre-select the current teacher
    if course.teacher_id:
        form.teacher.data = course.teacher_id
        
    return render_template('courses/edit.html', title='Edit Course', form=form, course=course)

@courses_bp.route('/delete/<int:id>')
@login_required
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    flash('Course deleted successfully!')
    return redirect(url_for('courses.list_courses'))
