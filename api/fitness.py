from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from __init__ import db
from model.fitness import FitnessEntry

diets_bp = Blueprint("diets", __name__)
diets_api = Api(diets_bp)


class DietAPI(Resource):
    def get(self):
        username = request.args.get("username")
        entry = db.session.query(FitnessEntry).filter_by(_username=username).all()
        print("abc" + str(username))
        if len(entry) != 0:
            return [e.to_dict() for e in entry]
        return {"error": "user not found"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True, type=str)
        parser.add_argument("calories", required=True, type=int)
        parser.add_argument("protein", required=True, type=int)
        parser.add_argument("fat", required=True, type=int)
        parser.add_argument("carbs", required=True, type=int)
        parser.add_argument("extra_notes", required=True, type=str)
        parser.add_argument("diet_name", required=True, type=str)
        args = parser.parse_args()

        entry = FitnessEntry(
            args["username"],
            args["diet_name"],
            args["calories"],
            args["protein"],
            args["fat"],
            args["carbs"],
            args["extra_notes"],
        )
        try:
            db.session.add(entry)
            db.session.commit()
            return entry.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"error": f"server error: {e}"}, 500

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", required=True, type=int)
        parser.add_argument("calories", required=False, type=int)
        parser.add_argument("protein", required=False, type=int)
        parser.add_argument("fat", required=False, type=int)
        parser.add_argument("carbs", required=False, type=int)
        parser.add_argument("extra_notes", required=False, type=str)
        parser.add_argument("diet_name", required=True, type=str)
        args = parser.parse_args()

        try:
            entry = db.session.query(FitnessEntry).get(args["id"])
            if entry:
                if args["calories"]:
                    entry.calories = args["calories"]
                if args["protein"]:
                    entry.protein = args["protein"]
                if args["fat"]:
                    entry.fat = args["fat"]
                if args["carbs"]:
                    entry.carbs = args["carbs"]
                if args["extra_notes"]:
                    entry.extra_notes = args["extra_notes"]
                if args["diet_name"]:
                    entry.extra_notes = args["diet_name"]
                db.session.commit()
                return entry.to_dict()
            else:
                return {"error": "entry not found"}, 404
        except Exception as e:
            db.session.rollback()
            return {"error": f"server error: {e}"}, 500

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", required=True, type=int)
        args = parser.parse_args()

        try:
            entry = db.session.query(FitnessEntry).get(args["id"])
            if entry:
                db.session.delete(entry)
                db.session.commit()
                return entry.to_dict()
            else:
                return {"error": "entry not found"}, 404
        except Exception as e:
            db.session.rollback()
            return {"error": f"server error: {e}"}, 500


diets_api.add_resource(DietAPI, "/diet")
