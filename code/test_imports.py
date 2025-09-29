# Test that imports are working correctly
print("Testing imports...")

# Test extensions imports
print("Importing extensions...")
from extensions import db, migrate, login_manager
print("Extensions imported successfully")

# Test models imports
print("Importing models...")
from models import User, Teacher, Course, Room, TimeSlot, Schedule, TeacherAvailability
print("Models imported successfully")

# Test route imports
print("Importing routes...")
from routes.auth import auth_bp
from routes.main import main_bp
from routes.teachers import teachers_bp
from routes.courses import courses_bp
from routes.rooms import rooms_bp
from routes.schedules import schedules_bp
print("Routes imported successfully")

print("All imports successful!")
