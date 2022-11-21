# Using flask to make an api
# import necessary libraries and functions
# from flask import Flask, jsonify, request

# # creating a Flask app
# app = Flask(__name__)

# # on the terminal type: curl http://127.0.0.1:5000/
# # returns hello world when we use GET.
# # returns the data that we send when we use POST.
# @app.route('/', methods = ['GET', 'POST'])
# def home():
# 	if(request.method == 'GET'):

# 		data = "hello world"
# 		return jsonify({'data': data})


# # A simple function to calculate the square of a number
# # the number to be squared is sent in the URL when we use GET
# # on the terminal type: curl http://127.0.0.1:5000 / home / 10
# # this returns 100 (square of 10)

from flask import Flask, request, redirect,jsonify,abort
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True

# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Creating an SQLAlchemy instance
db = SQLAlchemy(app)
@app.route('/v1/tasks', methods = ['POST','GET','PUT','DELETE'])
def disp():
	if request.method=="POST":
		data=request.get_json()
		boolVal=True if data['is_completed']=='true' else False
		p=Profile(title=data['title'],is_completed=boolVal)
		db.session.add(p)
		db.session.flush()

		return jsonify({'id': p.id})
	if request.method == "GET" :
		profiles = db.session.query(Profile).all()
		return jsonify({'tasks':str(profiles)})
@app.route('/v1/tasks/<int:id>', methods = ['POST','GET','PUT','DELETE'])
def check(id):
	if request.method=="GET":
		data = Profile.query.get(id)
		if data==None:
			abort(404,{"error":"There is no task at that id"})
		return jsonify({'id':id,'data':str(data)})
	if request.method=="DELETE":
		user = Profile.query.get(id)
		db.session.delete(user)
		db.session.commit()
		return 'there no data', 204
	if request.method=="PUT":
		user = Profile.query.get(id)
		data=request.get_json()
		print(user)
		if user==None:
			abort(404,{"error":"There is no task at that id"})
		user.title=data['title']
		user.is_completed=data['is_completed']
		db.session.commit()
		return jsonify({"res":"updated"})
class Profile(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(20), unique=False, nullable=False)
	is_completed = db.Column(db.Boolean, nullable=False)

	# repr method represents how one object of this datatable
	# will look like
	def __repr__(self):
		return f"title : {self.title}, is_completed: {self.is_completed}"

if __name__ == '__main__':
	app.run()

