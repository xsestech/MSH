from app import db


class Devices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dev_name = db.Column(db.String(20), unique=True)
    dev_id = db.Column(db.Integer, index=True, unique=True)
    type = db.Column(db.String(20), index=True)
    state = db.Column(db.Boolean)
    prev_state = db.Column(db.Boolean)

    def __repr__(self):
        return '<Device dev_id {}>'.format(self.dev_id)


class Timer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dev_name = db.Column(db.String(20), index=True)
    on_hour = db.Column(db.Integer, index=True)
    on_minute = db.Column(db.Integer, index=True)
    off_hour = db.Column(db.Integer, index=True)
    off_minute = db.Column(db.Integer, index=True)
