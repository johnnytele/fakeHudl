'''
import sys
sys.path.insert(0, '/var/www/fudl')

activate_this = '/home/ubuntu/.local/share/virtualenvs/fudl-PaE10qZl/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from routing import app as application
'''

import sys 
sys.path.insert(0, '/var/www/html/flaskapp')
from flaskapp import app as application