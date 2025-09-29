from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from models import Teacher, TeacherAvailability
from forms import TeacherForm, TeacherAvailabilityForm
from  extensions import db

teachers_bp = Blueprint('teachers', __name__, url_prefix='/teachers')

@teachers_bp.route('/')
@login_required
def list_teachers():
    teachers = Teacher.query.all()
    return render_template('teachers/list.html', title='Teachers', teachers=teachers)

@teachers_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_teacher():
    form = TeacherForm()
    if form.validate_on_submit():
        teacher = Teacher(
            name=form.name.data,
            email=form.email.data,
            department=form.department.data
        )
        db.session.add(teacher)
        db.session.commit()
        flash('Teacher added successfully!')
        return redirect(url_for('teachers.list_teachers'))
    
    return render_template('teachers/add.html', title='Add Teacher', form=form)

@teachers_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    form = TeacherForm(obj=teacher)
    
    if form.validate_on_submit():
        teacher.name = form.name.data
        teacher.email = form.email.data
        teacher.department = form.department.data
        db.session.commit()
        flash('Teacher updated successfully!')
        return redirect(url_for('teachers.list_teachers'))
    
    return render_template('teachers/edit.html', title='Edit Teacher', form=form, teacher=teacher)

@teachers_bp.route('/delete/<int:id>')
@login_required
def delete_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    db.session.delete(teacher)
    db.session.commit()
    flash('Teacher deleted successfully!')
    return redirect(url_for('teachers.list_teachers'))

@teachers_bp.route('/<int:id>/availability', methods=['GET', 'POST'])
@login_required
def teacher_availability(id):
    teacher = Teacher.query.get_or_404(id)
    form = TeacherAvailabilityForm()
    
    if form.validate_on_submit():
        availability = TeacherAvailability(
            teacher_id=teacher.id,
            day_of_week=form.day_of_week.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data
        )
        db.session.add(availability)
        db.session.commit()
        flash('Availability added successfully!')
        return redirect(url_for('teachers.teacher_availability', id=teacher.id))
    
    availabilities = TeacherAvailability.query.filter_by(teacher_id=teacher.id).all()
    return render_template('teachers/availability.html', title='Teacher Availability', 
                          form=form, teacher=teacher, availabilities=availabilities)

@teachers_bp.route('/availability/delete/<int:id>')
@login_required
def delete_availability(id):
    availability = TeacherAvailability.query.get_or_404(id)
    teacher_id = availability.teacher_id
    db.session.delete(availability)
    db.session.commit()
    flash('Availability deleted successfully!')
    return redirect(url_for('teachers.teacher_availability', id=teacher_id))
