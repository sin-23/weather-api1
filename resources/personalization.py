# resources/personalization.py
from flask_restful import Resource, reqparse
from flask import request
from marshmallow import ValidationError
from schemas.preferences_schema import preferences_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.external_api import (
    save_user_preferences,
    get_suggested_activities,
    get_weather_recommendation,
    get_prediction_confidence,
    update_user_location
)

from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.external_api import save_user_preferences

class UserPreferences(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        # Expecting a JSON body with preferences
        preferences = request.get_json(force=True)
        result = save_user_preferences(user_id, preferences)
        return {"status": "success", "message": result}, 201

class SuggestedActivities(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('location', type=str, required=True, help="Location is required")
        args = parser.parse_args()
        data = get_suggested_activities(args['location'])
        return {"status": "success", "data": data}, 200

class WeatherRecommendation(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        data = get_weather_recommendation(user_id)
        return {"status": "success", "data": data}, 200

class PredictionConfidence(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('location', type=str, required=True, help="Location is required")
        args = parser.parse_args()
        data = get_prediction_confidence(args['location'])
        return {"status": "success", "data": data}, 200

class UpdateLocation(Resource):
    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        parser = reqparse.RequestParser()
        parser.add_argument('location', type=str, required=True, help="New location is required")
        args = parser.parse_args()
        result = update_user_location(user_id, args['location'])
        return {"status": "success", "message": result}, 200
