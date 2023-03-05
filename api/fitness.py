from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource, reqparse
from __init__ import db
from model.fitness import FitnessEntry
from flask import Blueprint, jsonify  # jsonify creates an endpoint response object
from flask_restful import Api, Resource # used for REST API building


diets_api = Blueprint('diets_api', __name__,
                   url_prefix='/api/diets')
api = Api(diets_api)

class DietAPI(Resource):
    class _ReadAll(Resource):
        def get(self):
            query = FitnessEntry.query.all()    # read/extract all players from database
            json_ready = [player.read() for player in query]  # prepare output in json body
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
        
    class _ReadPerson(Resource):
        def get(self, username):
            query = FitnessEntry.query.all()    # read/extract all players from database
            json_ready = [player.read() for player in query if player._username == username]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    class _Update(Resource):
        def put(self, username, diet):
            update = request.get_json()["update"]
            query = FitnessEntry.query.all()    
            json_ready = [person for person in query if person._username == username and diet == person._diet_name]  # prepare output in json
            if len(json_ready) <= 0:
                return {"message" : "There is nothing like this!"}
            for entry in json_ready:
                entry.update(update)
            return {"message" : "Action Complete!"}  # jsonify creates Flask response object, more specific to APIs than json.dumps
        
    class _Post(Resource):
        def post(self):
            # username, dietname, calories, protein, fat, carbs, notes
            body = request.get_json()
            # validate name
            
            name = body.get('username')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 210
            dietname = body.get('diet_name')
            if name is None or len(name) < 2:
                return {'message': f'Diet Name is missing, or is less than 2 characters'}, 210
            cals = body.get('calories')
            protein = body.get('protein')
            fat = body.get('fat')
            carbs = body.get('carbs')
            notes = body.get('extra_notes')
            ''' #1: Key code block, setup PLAYER OBJECT '''
            fit = FitnessEntry(username=name, 
                        diet_name=dietname,
                        calories=cals,
                        protein=protein,
                        fat=fat,
                        carbs=carbs,
                        extra_notes=notes)
            print(fit)
            ''' #2: Key Code block to add user to database '''
            # create player in database
            player = fit.create()
            print("posted")
            # success returns json of player
            if player:
                return jsonify(player.read())
            # failure returns error
            return {'message': f'Processed {name}, either a format error or User ID is duplicate'}, 210
    class _Delete(Resource):
        def delete(self, id):
            query = FitnessEntry.query.all()    # read/extract all players from database
            entries = [player for player in query if player.id == id]  # prepare output in json
            for entry in entries:
                entry.delete()
            return jsonify({"message" : 'deleted'})  # jsonify creates Flask response object, more specific to APIs than json.dumps


    api.add_resource(_ReadAll, "/") 
    api.add_resource(_ReadPerson, "/<string:username>")
    api.add_resource(_Update, "/<string:username>_<string:diet>")
    api.add_resource(_Post, "/post")
    api.add_resource(_Delete, "/delete/<int:id>")