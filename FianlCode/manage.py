#!/user/bin/env python

__author__ = 'Wei'

from app import app
from app.models import *
# from flask_script import Manager
#from flask_migrate import Migrate, MigrateCommand 

#migrate = Migrate(app,db)
#manage = Manager(app)




if __name__ == '__main__':
    #manage.run()
    app.run()
    #app.run(port=8080)