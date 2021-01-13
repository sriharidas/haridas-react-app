from flask import Flask, Blueprint,request, render_template, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import os
import time
import datetime
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import spacy
import  socket

app = Flask(__name__)
db = SQLAlchemy()
db.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
englishBot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
trainer = ChatterBotCorpusTrainer(englishBot)
trainer.train("data/data.yml")
IP = socket.gethostbyname(socket.gethostname())

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    emailid = db.Column(db.String(100))
    mobile_no = db.Column(db.Integer)
    password_1 = db.Column(db.String(100))
    password_2 = db.Column(db.String(100))
    ip_address = db.Column(db.String(100))

class UserLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100))
    password_1 = db.Column(db.String(100))
    password_2 = db.Column(db.String(100))
    log_data = db.Column(db.TIMESTAMP)
    ip_address = db.Column(db.String(100))

class Bot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    user_text = db.Column(db.String(500))
    bot_text = db.Column(db.String(500))
    text_time = db.Column(db.TIMESTAMP)
    ip_address = db.Column(db.String(100))
u = {'username':""}
chatbot = {
    'usertext': None,
    'bottext': []
}
logged_user = []
@app.route('/')
def welcome():

    return str(IP)

@app.route('/signin',methods=['POST'])
def user():
    user_data = request.get_json()
    if user_data['password_1'] == user_data['password_2']:
        new_user = Users(username=user_data['username'], emailid=user_data['emailid'],\
                         name=user_data['name'],mobile_no=user_data['mobile_no'],password_1=user_data['password_1'],\
                         password_2=user_data['password_2'],ip_address=IP)
        u['username'] = user_data['username']
        db.session.add(new_user)
        db.session.commit()
    else:
        return "password doesn't match"

    return jsonify({
        'username': user_data['username'],
        'email':user_data['emailid'],
        'name':user_data['name'],
        'mobile_no' : user_data['mobile_no'],
        'status':201
    }
    )

@app.route('/signin',methods=['GET'])
def users():
    users_list = Users.query.filter_by(ip_address=IP).first()
    users = []

    users.append({
        'username':users_list.username,
        'email adress': users_list.emailid,
    })

    return jsonify(users)

user = {'username':""}
@app.route('/login/',methods=['POST'])
def login():
    user_data = request.get_json()
    exst_user = Users.query.filter_by(username=str(user_data['username'])).first()
    status = []
    if exst_user is None:
        return str(str(user_data['username']+" is not found. Please Sign in if you haven't regustered already"))
    else:
        if (user_data['password_1'] == str(exst_user.password_1 )) and (user_data['password_2']==str(exst_user.password_1)):

            status.append(True)
            user_logs = UserLog(username=user_data['username'], email=user_data['email'],name=user_data['name'],\
                                password_1=user_data['password_1'],password_2=user_data['password_2'],\
                                log_data=datetime.datetime.now(), ip_address=IP)
            db.session.add(user_logs)
            db.session.commit()
            user['username'] = user_data['username']
            return str("welcome " +str(user_data['username']))

        else:
            status.append(False)
            return "invalid password!"
    return {
        'status':status[0]
    }

@app.route('/login/',methods=['GET'])
def userlogs():
    users = []
    if user['username'] == '':
        try:
            userlogs = UserLog.query.filter_by(ip_address=IP).first()
            u = userlogs.username
            logged_user.append(str(u))
            users.append(u)
        except:
            return "Please Sign up to continue"
    else:

        userlogs = UserLog.query.filter_by(username=user['username']).first()
        u = userlogs.username
        users.append(u)
    return jsonify(
        {
            'username':str(users)
        }
    )
@app.route('/chatbot',methods=['POST'])
def Chatbot():
    global chatbot, user
    userText = str(request.args.get('msg'))
    bot_text = str(englishBot.get_response(userText))
    chatbot['usertext'] = userText
    chatbot['bottext'] = bot_text
    if userText != None:
         bot = Bot(username=user['username'], user_text=userText, bot_text=bot_text, text_time=datetime.datetime.now(),\
                   ip_address=IP)
         db.session.add(bot)
         db.session.commit()
    else:
        return "Please input a valid sentence."
    return "Done.", 201
@app.route('/chatbot', methods=['GET'])
def chats():
    chat_bot = []

    if user['username'] == '':
        chts = Bot.query.filter_by(ip_address=IP, username=logged_user[0]).all()
        try:

            for chat in chts:
                chat_bot.append(
                    {
                        str("\'" + logged_user[0] + "\'"): str(chat.user_text),
                        "Bot": str(chat.bot_text),
                        "time": str(chat.text_time)
                    }
                )
        except:
            return "Please Sign up to continue"
    else:
        chts = Bot.query.filter_by(username=user['username']).all()
        try:
            for chat in chts:
                chat_bot.append(
                    {
                        str("\'" + logged_user[0] + "\'"): str(chat.user_text),
                        "Bot": str(chat.bot_text),
                        "time": str(chat.text_time)
                    }
                )
        except:
            return "Please Sign up to continue"

    '''return {
       
        "bot" : str(chats.bot_text)

    }'''
    return jsonify(chat_bot)
if __name__ == '__main__':
    app.run(debug=True)
