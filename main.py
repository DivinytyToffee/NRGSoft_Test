import json

from bson.errors import InvalidId

import dateutil
import pandas as pd

from flask import Flask, request
from flask_restful import Resource, Api
from flask_pymongo import PyMongo, ObjectId

from helpers import calculate_cagr, mongo_record, WrongDataTypeException

app = Flask(__name__)
api = Api(app)
app.config["MONGO_URI"] = "mongodb://localhost:27017/timeSeriesDB"
app.config["PORT"] = "5050"
app.config["HOST"] = '127.0.0.1'
mongo = PyMongo(app)


class TimeSeriesWorker(Resource):

    def get(self):
        try:
            _id = request.json.get('id')
        except Exception as ex:
            return {"message": ex}, 400

        if isinstance(_id, str):
            try:
                post = mongo.db.data.find_one({'_id': ObjectId(_id)})
                if post is None:
                    return {"message": "id is not exist"}, 422

                post.pop('_id')
                read_json = pd.read_json(json.dumps(post), typ='index')
                cagr = calculate_cagr(read_json)

            except InvalidId as inv_id:
                return {"message": inv_id.__str__()}, 404

            except ZeroDivisionError:
                return {"message": "Require more then one value"}, 400

            return {"cagr": cagr}, 200
        else:
            return '', 422

    def put(self):
        try:
            _id = request.json.get('id')
            data = request.json.get('data')
        except Exception as ex:
            return {"message": ex}, 400

        if isinstance(_id, str) and isinstance(data, dict):

            try:
                insert = mongo_record(data)

                result = mongo.db.data.update_one(
                    {'_id': ObjectId(_id)},
                    {'$set': insert}
                )
            except InvalidId as inv_id:
                return {"message": inv_id.__str__()}, 404

            except OverflowError:
                return {"message": "Convert keys to calendar view"}, 422

            except WrongDataTypeException:
                return {'message': 'values must be a number'}, 422

            except dateutil.parser._parser.ParserError:
                return {"message": "Wrong data format"}, 422

            if result:
                return '', 204
            else:
                return {'message': 'can\'t insert'}, 422

        else:
            return '', 422

    def post(self):
        try:
            data = request.json.get('data')
        except Exception as ex:
            return {"error": ex}

        if isinstance(data, dict):
            try:
                insert = mongo_record(data)

                post_id = mongo.db.data.insert_one(insert)

            except ValueError:
                return {"message": "keys must be a date"}, 422

            except OverflowError:
                return {"message": "convert keys to calendar view"}, 422

            except WrongDataTypeException:
                return {'message': 'values must be a number'}, 422

            except dateutil.parser._parser.ParserError:
                return {"message": "wrong data format"}, 422

            return {"id": str(post_id.inserted_id)}

        else:
            return '', 422


api.add_resource(TimeSeriesWorker, '/time-series')

if __name__ == '__main__':
    app.run(
        host=app.config.get('HOST'),
        port=app.config.get('PORT'),
    )
