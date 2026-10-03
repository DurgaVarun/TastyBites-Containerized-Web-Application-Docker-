from flask import Flask,render_template,redirect,url_for,request,session
from flask_mysqldb import MySQL 
from forms import Loginform,Contactpage,RegistrationForm
import bcrypt
app=Flask(__name__)
app.secret_key='supersecretkey'
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="Varun@2005"
app.config["MYSQL_DB"]="tastybites"
mysql=MySQL(app)
@app.route('/', methods=['GET', 'POST'])
def home():
    form = Loginform()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s ", (username,))
        account = cur.fetchone()
        cur.close()
        if account:
            stored_hash = account[3].encode('utf-8')  
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                session["loggedin"] = True
                session["name"] = account[1]
                return redirect(url_for("welcome"))       
        return render_template("home.html", form=form, error="Invalid username or password")
    return render_template("home.html", form=form)
@app.route('/Contact.html',methods=['GET','POST'])
def contact():
    form=Contactpage()
    if form.validate_on_submit():
        name=form.name.data
        mail=form.mail.data
        message=form.message.data
        return render_template('menu.html',name=name,mail=mail,message=message)
    return render_template('Contact.html',form=form)
@app.route('/welcome.html')
def welcome():
    return render_template('welcome.html')
@app.route('/menu.html')
def menu():
    return render_template('menu.html')
@app.route('/About us.html')
def about():
    return render_template('About us.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        email = form.email.data.strip().lower()
        password = form.password.data
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cur.fetchone()
        if existing_user:
            cur.close()
            return render_template("register.html", form=form, error="This email is already registered.")
        cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, hashed_password))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("home"))   
    return render_template('register.html', form=form)
if __name__=="__main__":
    app.run(debug=True)