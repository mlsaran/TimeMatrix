from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from models import Room
from forms import RoomForm
from extensions import db

rooms_bp = Blueprint('rooms', __name__, url_prefix='/rooms')

@rooms_bp.route('/')
@login_required
def list_rooms():
    rooms = Room.query.all()
    return render_template('rooms/list.html', title='Rooms', rooms=rooms)

@rooms_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_room():
    form = RoomForm()
    if form.validate_on_submit():
        room = Room(
            name=form.name.data,
            capacity=form.capacity.data,
            has_projector=form.has_projector.data,
            building=form.building.data
        )
        db.session.add(room)
        db.session.commit()
        flash('Room added successfully!')
        return redirect(url_for('rooms.list_rooms'))
    
    return render_template('rooms/add.html', title='Add Room', form=form)

@rooms_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_room(id):
    room = Room.query.get_or_404(id)
    form = RoomForm(obj=room)
    if form.validate_on_submit():
        room.name = form.name.data
        room.capacity = form.capacity.data
        room.has_projector = form.has_projector.data
        room.building = form.building.data
        db.session.commit()
        flash('Room updated successfully!')
        return redirect(url_for('rooms.list_rooms'))
    
    return render_template('rooms/edit.html', title='Edit Room', form=form, room=room)

@rooms_bp.route('/delete/<int:id>')
@login_required
def delete_room(id):
    room = Room.query.get_or_404(id)
    db.session.delete(room)
    db.session.commit()
    flash('Room deleted successfully!')
    return redirect(url_for('rooms.list_rooms'))
