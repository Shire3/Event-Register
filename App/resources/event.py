from App.config.config import db

class Event(db.Model):
    __tablename__= "events"
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    start_time = db.Column(db.String(), nullable=False, unique= True)
    end_time = db.Column(db.String(), nullable=False, unique= True)
    location = db.Column(db.String(), nullable = False)
    created_by = db.Column(db.Integer(),db.ForeignKey("user.id"))
    
    user= db.relationship("User", backref=db. backref("Event", lazy = True))

def __repr__(self):
    return f"<Event {self.id}>"

def save(self):
    db.session.add(self)
    db.session.commit()

def get_event_by_id(self,id):
    return self.query.get_or_404(id)

def to_dict(self):
    return{
    "id": self.id,
    "title": self.title,
    "description": self.description,
    "start_time": self.start_time,
    "end_time": self.end_time,
    "location": self.location,
        }