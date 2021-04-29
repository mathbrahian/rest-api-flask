from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.abspath(os.getcwd()) +"/database.db"
api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Note_db(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default= datetime.datetime.utcnow())
    updated_at = db.Column(db.DateTime, default= datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())

class Note_schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Note_db
        include_fk = True

note_schema = Note_schema()
notes_schema = Note_schema(many=True)

class Note_rest(Resource):
    def get(self):
        notes = Note_db.query.all()
        return notes_schema.jsonify(notes)
    
    def post(self):
        note_json = request.get_json()
        note = Note_db(title = note_json['title'], description = note_json['description'])
        db.session.add(note)
        db.session.commit()
        return note_schema.jsonify(note)

class Note_rest_id(Resource):
    def get(self, id):
        note = Note_db.query.get(id)
        if note == None:
            return {"message": "Todo could not be found"}, 404
        else:
            return note_schema.jsonify(note)

    def delete(self, id):
        note = Note_db.query.get(id)
        if note == None:
            return {"message": "Todo could not be found"}, 404
        else:
            db.session.delete(note)
            db.session.commit()
            return note_schema.jsonify(note)
    
    def put(self, id):
        note = Note_db.query.get(id)
        if note == None:
            return {"message": "Todo could not be found"}, 404
        else:
            note_json = request.get_json()
            note.title = note_json['title']
            note.description = note_json['description']
            db.session.commit()
            return note_schema.jsonify(note)



api.add_resource(Note_rest, '/')
api.add_resource(Note_rest_id, '/<string:id>')
    
if __name__ == '__main__':
    app.run(debug=True)