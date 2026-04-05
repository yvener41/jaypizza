import sys
import os

# Add your project directory to the path
# Replace 'yourusername' with your actual PythonAnywhere username
project_home = '/home/yourusername/pizza_db_project'

if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set working directory so SQLite db is created in the right place
os.chdir(project_home)

from app import app as application
