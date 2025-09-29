# check_db.py
from app import app, db

with app.app_context():
    inspector = db.inspect(db.engine)
    
    # Print all table names
    tables = inspector.get_table_names()
    print("Tables in database:", tables)
    
    # Check if 'user' table exists
    if 'user' in tables:
        print("User table exists!")
        # Print columns in the user table
        columns = [col['name'] for col in inspector.get_columns('user')]
        print("Columns in user table:", columns)
    else:
        print("User table does NOT exist!")
