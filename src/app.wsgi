import sys

sys.path.insert(0, "/home/ec2-user/recommendation-system-restaurants-api")

activate_this = '/home/ec2-user/recommendation-system-restaurants-api/venv/bin/activate_this.py'

with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from app import app as application