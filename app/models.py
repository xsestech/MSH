from app import db

class Devices(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(20), unique=True)
     dev_id = db.Column(db.Integer, index=True, unique=True)
     type = db.Column(db.String(20), index=True)
     state = db.Column(db.Boolean)
     prev_state = db.Column(db.Boolean)
     def __repr__(self):
         return '<Device dev_id {}>'.format(self.dev_id)
class Scripts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), index=True)
    state = db.Column(db.Boolean)
    prev_state = db.Column(db.Boolean)

    def __repr__(self):
        return '<Device dev_id {}>'.format(self.dev_id)


