import dotenv
import os

from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from marshmallow import Schema, fields

dotenv.load_dotenv()

db_user = os.environ.get('DB_USERNAME')
db_pass = os.environ.get('DB_PASSWORD')
db_hostname = os.environ.get('DB_HOSTNAME')
db_name = os.environ.get('DB_NAME')

DB_URI = 'mysql+pymysql://{db_user}:{db_pass}@{db_host}/{database}'.format(
    db_user=db_user, db_pass=db_pass, db_host=db_hostname, database=db_name)

engine = create_engine(DB_URI, echo=True)


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    cellphone = db.Column(db.String(13), unique=True, nullable=False)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class StudentSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    email = fields.Str()
    age = fields.Integer()
    cellphone = fields.Str()


student_schema = StudentSchema


@app.route('/', methods=['GET'])
def home():
    return jsonify("Hello from students API"), 200


@app.route('/api', methods=['GET'])
def api_main():
    return render_template('swaggerui.html')


@app.route('/api/students', methods=['GET'])
def get_all_students():
    students = Student.get_all()
    student_list = StudentSchema(many=True)
    response = student_list.dump(students)
    return jsonify(response), 200


@app.route('/api/students/get/<int:id>', methods=['GET'])
def get_student(id):
    student_info = Student.get_by_id(id)
    serializer = StudentSchema()
    response = serializer.dump(student_info)
    return jsonify(response), 200


@app.route('/api/students/modify/<int:id>', methods=['PATCH'])
def modify_student(id):
    student_info = Student.get_by_id(id)
    json_data = request.get_json()
    if "name" in json_data:
        student_info.name = json_data.get('name')
    if "email" in json_data:
        student_info.email = json_data.get('email')
    if "age" in json_data:
        student_info.age = json_data.get('age')
    if "cellphone" in json_data:
        student_info.cellphone = json_data.get('cellphone')

    try:
        db.session.commit()
    except ValueError:
        return jsonify("Something went wrong!"), 500

    return jsonify(), 204


@app.route('/api/students/change/<int:id>', methods=['PUT'])
def change_student(id):
    student_info = Student.get_by_id(id)
    json_data = request.get_json()

    student_info.name = json_data.get('name')
    student_info.email = json_data.get('email')
    student_info.age = json_data.get('age')
    student_info.cellphone = json_data.get('cellphone')
    try:
        db.session.commit()
    except ValueError:
        return jsonify("Something went wrong!"), 500

    return jsonify(), 204


@app.route('/api/students/delete/<int:id>', methods=['DELETE'])
def delete_student(id):
    student_to_delete = Student.get_by_id(id)
    try:
        db.session.delete(student_to_delete)
        db.session.commit()
        return jsonify("Student was deleted!"), 200
    except ValueError:
        return jsonify("Something went wrong!"), 500


@app.route('/api/students/add', methods=['POST'])
def add_student():
    json_data = request.get_json()
    new_student = Student(
        name=json_data.get('name'),
        email=json_data.get('email'),
        age=json_data.get('age'),
        cellphone=json_data.get('cellphone')
    )
    new_student.save()
    serializer = StudentSchema()
    data = serializer.dump(new_student)
    return jsonify(data), 201


@app.route('/api/health-check/ok', methods=["GET"])
def heath_check_ok():
    return jsonify('Healthy'), 200


@app.route('/api/health-check/bad', methods=["GET"])
def heath_check_bad():
    return jsonify('Not healthy'), 500


if __name__ == "__main__":
    if not database_exists(engine.url):
        create_database(engine.url)
    db.create_all()
    app.run(host="0.0.0.0", debug=True, port=5000)
