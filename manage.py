from flask_script import Manager
from flask_migrate import MigrateCommand
from dynamic.v1.app import app, db, migrate

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

