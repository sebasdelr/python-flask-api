import xml.etree.ElementTree as ET

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

file = ET.parse('secrets.xml')

database = file.find('db').text
user = file.find('user').text
password = file.find('password').text

database_uri = 'mysql+pymysql://' + user + ':' + password + '@' + database

print(database_uri)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parentId = db.Column(db.Integer)
    title = db.Column(db.String(70), unique=True)
    content = db.Column(db.String(100))
    dateCreated = db.Column(db.Date)
    startDate = db.Column(db.Date)
    dateDue = db.Column(db.Date)
    type = db.Column(db.Integer)
    status = db.Column(db.String(70)
    reviewed = db.Column(db.Boolean)
    color = db.Column(db.String(10))

 

    def __init__(self, parentId, title, content, dateCreated, startDate, dateDue, type, status, reviewed, color):
        self.parentId = parentId
        self.title = title
        self.content = content
        self.dateCreated = dateCreated
        self.startDate = startDate
        self.dateDue = dateDue
        self.type = type
        self.status = status
        self.reviewed = reviewed
        self.color = color

#db.create_all()

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'parentId', 'title', 'content', 'dateCreated', 'startDate', 'dateDue', 'type', 'status', 'reviewed', 'color')


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


@app.route('/tasks', methods=['Post'])
def create_task():
  parentId = request.json['parentId']
  title = request.json['title']
  content = request.json['content']
  dateCreated = request.json['dateCreated']
  startDate = request.json['startDate']
  dateDue = request.json['dateDue']
  type = request.json['type']
  status = request.json['status']
  reviewed = request.json['reviewed']
  color = request.json['color']


  new_task= Task(parentId, title, content, dateCreated, startDate, dateDue, type, status, reviewed, color)

  db.session.add(new_task)
  db.session.commit()

  return task_schema.jsonify(new_task)

@app.route('/tasks', methods=['GET'])
def get_tasks():
  all_tasks = Task.query.all()
  result = tasks_schema.dump(all_tasks)
  return jsonify(result)

@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
  task = Task.query.get(id)
  return task_schema.jsonify(task)

@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
  task = Task.query.get(id)

  parentId = request.json['parentId']
  title = request.json['title']
  content = request.json['content']
  dateCreated = request.json['dateCreated']
  startDate = request.json['startDate']
  dateDue = request.json['dateDue']
  type = request.json['type']
  status = request.json['status']
  reviewed = request.json['reviewed']
  color = request.json['color']

  task.parentId = parentId
  task.title = title
  task.content = content
  task.dateCreated = dateCreated
  task.startDate = startDate
  task.dateDue = dateDue
  task.type = type
  task.status = status
  task.reviewed = reviewed
  task.color = color

  db.session.commit()

  return task_schema.jsonify(task)

@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
  task = Task.query.get(id)
  db.session.delete(task)
  db.session.commit()
  return task_schema.jsonify(task)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to my API'})



if __name__ == "__main__":
    app.run(debug=True)