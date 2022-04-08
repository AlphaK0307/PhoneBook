from app import app, db
from app.models import User, Post, Phone


@app.shell_context_processor
def makae_context():
    return {'db': db, 'User': User, 'Post': Post, 'Phone': Phone}
