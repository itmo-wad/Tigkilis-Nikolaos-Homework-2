import os ,json
from flask import Flask, flash, render_template , redirect, url_for , request , session
from flask_pymongo import PyMongo
from itsdangerous import exc
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/wad"
app.secret_key = 'super67sEcret459!!key@s'
mongo = PyMongo(app)

print('---LOG: best debug method: WEBSITE: OK')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signup',methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
      email = request.form['email']
      password = request.form['pass']

      email_found = mongo.db.users.find_one({"email": email})
      if(email_found):
          print("---LOG: memory loss!")
          #print user already exists message
          return redirect(url_for('fail',name = email))
      else:
        #create user inside mongo
        user_data = {'email': email, 'password': password}
        mongo.db.users.insert_one(user_data)
        print('---LOG: great success')
        messages = json.dumps({"main":email})
        session['messages'] = email
        return redirect(url_for('.profile',messages=messages))

        #return redirect(url_for('profile',name = email))
    else: #get method
      return render_template("signup.html")

@app.route('/profile')
def profile():
    try:
        messages = session['messages']
        if(messages):
            flash(messages)
            return render_template("profile.html")
        else:
            return redirect(url_for('index'))
    except:
        return redirect(url_for('index'))


#@app.route('/success/<name>')
#signup sucess
#def success(name):
#    flash(name)
#    return render_template("profile.html")

@app.route('/fail/<name>')
#signup fail
def fail(name):
    session.clear()
    return 'User %s already exists.' % name

@app.route('/auth',methods = ['POST', 'GET'])
def auth():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        #auth check

        user = mongo.db.users.find_one({"email": email, "password": password})
        try:
            db_email=str(user.get('email'))
            db_password=str(user.get('password'))
            if(db_email==email and db_password==password):
                #login success
                messages = json.dumps({"main":email})
                session['messages'] = email
                return redirect(url_for('.profile',messages=messages))
                #return render_template("profile.html")
            else:
                session.clear()
                flash("Wrong username or password!")
                return render_template('index.html')
        except:
            session.clear()
            flash("Wrong username or password!")
            return render_template('index.html')
    else: #get method
        return render_template("login.html")

app.run(host='localhost', port=5000)