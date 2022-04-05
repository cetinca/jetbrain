import datetime
from flask import make_response, jsonify, request
from flask_restful import Resource, reqparse, inputs
from event_model import EventModel


def event_parser():
    parser = reqparse.RequestParser()
    parser.add_argument(
        'id',
        type=int,
        help="ID is required!",
        required=False,
        location="form"
    )

    parser.add_argument(
        'event',
        type=str,
        help='The event name is required!',
        required=True,
        location="form"
    )

    parser.add_argument(
        'date',
        type=inputs.date,
        help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
        required=True,
        location="form"
    )

    return parser.parse_args()


class EventResource(Resource):

    def get(self):
        data = request.args
        start_time = data.get("start_time", default=None)
        end_time = data.get("end_time", default=None)
        if not start_time or not end_time:
            return jsonify(EventModel.find_all())

        filtered_events = EventModel.find_between(
            datetime.datetime.fromisoformat(start_time).date(),
            datetime.datetime.fromisoformat(end_time).date()
        )
        return jsonify(filtered_events)

    def post(self):
        data = event_parser()
        event = EventModel(event=data["event"], date=data["date"].date())
        event.save_to_db()
        data['date'] = str(data['date'].date())
        data['message'] = "The event has been added!"
        return make_response(data, 200)


class TodayResource(Resource):
    def get(self):
        events = EventModel.find_all()
        events = [event for event in events if event["date"] == str(datetime.date.today())]
        return jsonify(events)


class IdResource(Resource):
    def get(self, _id):
        event = EventModel.find_by_id(_id)
        if not event:
            return make_response(jsonify({"message": "The event doesn't exist!"}), 404)
        return event.json()

    def delete(self, _id):
        event = EventModel.find_by_id(_id)
        if not event:
            return make_response(jsonify({"message": "The event doesn't exist!"}), 404)
        event.delete()
        return jsonify({"message": "The event has been deleted!"})
