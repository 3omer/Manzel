from app import app, db
from app.mongoDB import Device, User


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Device': Device, 'User': User}
