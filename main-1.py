from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import os

# Init app
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'students.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'supersecretkey'

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

class StudentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email')

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

@app.route('/student', methods=['POST'])
def add_student():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']

    if Student.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400

    new_student = Student(name, email, password)
    db.session.add(new_student)
    db.session.commit()

    return student_schema.jsonify(new_student)

@app.route('/students', methods=['GET'])
def get_students():
    all_students = Student.query.all()
    return students_schema.jsonify(all_students)

@app.route('/student/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get_or_404(id)
    return student_schema.jsonify(student)

@app.route('/student/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get_or_404(id)
    data = request.get_json()

    student.name = data.get('name', student.name)
    student.email = data.get('email', student.email)
    
    if 'password' in data:
        student.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    db.session.commit()
    return student_schema.jsonify(student)

@app.route('/student/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    student = Student.query.filter_by(email=email).first()
    
    if student and bcrypt.check_password_hash(student.password, password):
        access_token = create_access_token(identity={'id': student.id, 'email': student.email})
        return jsonify({'token': access_token})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
