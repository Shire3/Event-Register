from App.resources.event import Event
from App.config.config import db
from flask_restx import Namespace, Resource, fields, marshal_with
from flask import request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import BadRequest, Conflict
from datetime import datetime
from http import HTTPStatus 

event_ns = Namespace('events', description='Event operations')

event_model = event_ns.model('Event', {
    'id': fields.Integer(readonly=True),
    'title': fields.String(required=True),
    'description': fields.String(),
    'start_time': fields.DateTime(required=True),
    'end_time': fields.DateTime(required=True),
    'location': fields.String(required=True),
})

@event_ns.route("/event")
class EventCreate(Resource):
    @event_ns.expect(event_model)
    @event_ns.marshal_with(event_model)
    @jwt_required()
    def post(self):
        """Add a new event to the system"""
        data = request.get_json()
        user_id = get_jwt_identity()

        title = data["title"]
        description = data.get("description")
        start_time = data["start_time"]
        end_time = data["end_time"]
        location = data["location"]
        created_by = user_id


        try:

            if start_time >= end_time:
                raise Conflict(f"Your start time can't be more than your ending time")



            new_event = Event(
                title=title,
                description=description,
                start_time=start_time,
                end_time=end_time,
                location=location,
                created_by=created_by
            )

            db.session.add(new_event)
            db.session.commit()


            return new_event, HTTPStatus.CREATED
        except Exception as e:
            return {"Error": str(e)}, HTTPStatus.BAD_REQUEST
        
        
@event_ns.route('/<int:event_id>')
class EventResource(Resource):
    @jwt_required()
    @marshal_with(event_model)
    def get(self, event_id):
        event = Event.query.get_or_404(event_id)
        return event, 200

    @jwt_required()
    @event_ns.expect(event_model)
    @marshal_with(event_model)
    def put(self, event_id):
        event = Event.query.get_or_404(event_id)
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if user.role == 'organizer' and event.created_by != user_id:
            abort(403, "You can only update your own events.")

        data = request.get_json()
        start = datetime.fromisoformat(data['start_time'])
        end = datetime.fromisoformat(data['end_time'])

        conflict = Event.query.filter(
            Event.id != event.id,
            Event.start_time < end,
            Event.end_time > start
        ).first()

        if conflict:
            abort(409, "Time conflict with another event.")

        event.title = data['title']
        event.description = data.get('description')
        event.start_time = start
        event.end_time = end
        event.location = data['location']

        db.session.commit()
        return event, 200

    @jwt_required()
    def delete(self, event_id):
        event = Event.query.get_or_404(event_id)
        user_id = get_jwt_identity()

        if user_id != event.created_by:
            abort(403, "You can only delete your own events.")

        db.session.delete(event)
        db.session.commit()
        return '', 204

@event_ns.route('/get_all')
class EventResource(Resource):
    @jwt_required()
    @marshal_with(event_model)
    def get(self):
        event = Event.query.all()
        return event, 200
