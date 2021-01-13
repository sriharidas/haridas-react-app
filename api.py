'''from flask import Flask, request, render_template, jsonify, make_response
from flask_mysqldb import MySQL

app = Flask(__name__)
@app.route('/')
def welcome():
    return "welcome"

username = email = ''
users= []
name = "root"
@app.route('/send',methods = ['POST','GET'])
def send():
    if request.method == 'POST':
        global username, email

        try:
             username = request.form['name']
             email = request.form['email']
             return jsonify({
                'name': username,
                'email': email
            })
        except:
            username = request.args['name']
            email = request.args['email']

            return jsonify({
                'name':username,
                'email':email
            })

    u = {
        'name':username,
        'email':email
    }
    users.append(u)

    return u


@app.route('/recieve',methods = ["GET"])
def recieve():
    users = []
    users.append({
                'name':username,
                'email':email
            })
    return jsonify(users)

if __name__ == "__main__":
    app.run(debug=True)'''

#sqlalchemy
'''
#initialization

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
#Dataase
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'user.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class UserDatabase(db.Model):
    username = db.Column(db.String(100),unique=True,primary_key=True)
    email = db.Column(db.String(100))
    def __init__(self, username, email):
        self.username = username
        self.email = email

class UserSchema(ma.Schema):
    class Meta:
        fields=('username','email')

#Init Schema
user_schema = UserSchema()
#users_schema = UserSchema(many=True)

users= []
name = "root"


@app.route('/')
def welcome():
    return "welcome to chatterbot module!!!!!!"

@app.route('/signup',methods=['POST','GET'])
def request():

    username = "hari"
    email = "haridas"
    new_user = UserDatabase(username,email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        username: username,
        email: email
    })

@app.route('/bot_response',methods=['GET'])
def resp():
    return jsonify({
        'username':'haridas',
        'email':'hari@123'
    })'''

