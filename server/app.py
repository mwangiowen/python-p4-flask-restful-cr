#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///newsletters.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Index(Resource):
    def get(self):
        response_dict = {
            "index": "Welcome to the Newsletter RESTful API",
        }

        response = make_response(
            jsonify(response_dict),
            200,
        )

        return response


api.add_resource(Index, "/")


class Newsletters(Resource):
    def get(self):
        response_dict_list = [n.to_dict() for n in Newsletter.query.all()]

        response = make_response(
            jsonify(response_dict_list),
            200,
        )

        return response

    def post(self):
        try:
            data = request.get_json()

            if not isinstance(data, dict):
                raise ValueError("Invalid JSON format. Expected a JSON object.")

            title = data.get("title")
            body = data.get("body")

            if title is None or body is None:
                raise ValueError(
                    "Both 'title' and 'body' must be provided in the request."
                )

            new_record = Newsletter(
                title=title,
                body=body,
            )

            db.session.add(new_record)
            db.session.commit()

            response_dict = new_record.to_dict()

            response = make_response(
                jsonify(response_dict),
                201,
            )

            return response
        except ValueError as e:
            error_response = {"error": str(e)}
            return make_response(jsonify(error_response), 400)


api.add_resource(Newsletters, "/newsletters")


class NewsletterByID(Resource):
    def get(self, id):
        response_dict = Newsletter.query.filter_by(id=id).first().to_dict()

        response = make_response(
            jsonify(response_dict),
            200,
        )

        return response


api.add_resource(NewsletterByID, "/newsletters/<int:id>")


if __name__ == "__main__":
    app.run(port=5555)
