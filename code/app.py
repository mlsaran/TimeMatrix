from flask import Flask
from config import Config
from extensions import db, migrate, login_manager

# Create and configure the app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions with app
db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)

# Import models and set up login manager
from models import User, Teacher, Course, Room, TimeSlot, Schedule, TeacherAvailability

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# Register blueprints
from routes.auth import auth_bp
from routes.main import main_bp
from routes.teachers import teachers_bp
from routes.courses import courses_bp
from routes.rooms import rooms_bp
from routes.schedules import schedules_bp

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(teachers_bp)
app.register_blueprint(courses_bp)
app.register_blueprint(rooms_bp)
app.register_blueprint(schedules_bp)

if __name__ == '__main__':
    app.run(debug=True)
