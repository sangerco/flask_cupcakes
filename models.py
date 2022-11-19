"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


default_img = 'https://tinyurl.com/demo-cupcake'


class Cupcake(db.Model):
    """ class for cupcakes """

    __tablename__ = 'cupcakes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, default=default_img)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'done': self.done
        }
