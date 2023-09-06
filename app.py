from flask import Flask,render_template,request,url_for,session,redirect,flash
from flask_mysqldb import MySQL
import os

app=Flask(__name__)

app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="root"
app.config["MYSQL_DB"]="crush"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)

@app.route("/",methods=['GET','POST'])
def index():
    if 'register' in request.form:
        if request.method == 'POST':
            uname = request.form["uname"]
            password = request.form["upass"]
            age = request.form["age"]
            address = request.form["address"]
            contact = request.form["contact"]
            mail = request.form["mail"]
            cur = mysql.connection.cursor()
            cur.execute('insert into register(name,password,age,address,contact,mail) values (%s,%s,%s,%s,%s,%s)',
                        [uname, password, age, address, contact, mail])
            mysql.connection.commit()
        return render_template("index.html")

    elif 'ulogin' in request.form:
        if request.method == 'POST':
            name = request.form["uname"]
            password = request.form["upass"]
            try:
                cur = mysql.connection.cursor()
                cur.execute("select * from register where name=%s and password=%s", [name, password])
                res = cur.fetchone()
                if res:
                    session["name"] = res["name"]
                    session["id"] = res["id"]
                    return redirect(url_for('user_home'))
                else:
                    return render_template("index.html")
            except Exception as e:
                print(e)
            finally:
                mysql.connection.commit()
                cur.close()
    return render_template("index.html")

@app.route("/user_profile")
def user_profile():
    cur = mysql.connection.cursor()
    id=session["id"]
    qry = "select * from register where id=%s"
    cur.execute(qry,[id])
    data = cur.fetchone()
    cur.close()
    count = cur.rowcount
    if count == 0:
        flash("Users Not Found...!!!!", "danger")
    else:
        return render_template("user_profile.html",res=data)	
	
@app.route("/user_home")
def user_home():
	return render_template("user_home.html")
	
@app.route("/emp",methods=['GET','POST'])
def emp():
	if 'emp' in request.form:
		if request.method =='POST':
			ename=request.form["ename"]
			eid=request.form["eid"]
			contact=request.form["contact"]
			mail=request.form["mail"]
			address=request.form["address"]
			degree=request.form["degree"]
			date=request.form["date"]
			lang=request.form["lang"]
			cur=mysql.connection.cursor()
			cur.execute('insert into emp(emp_name,emp_id,mobile_no,mail,address,degree,joinig,lang) values (%s,%s,%s,%s,%s,%s,%s,%s)',
			[ename,eid,contact,mail,address,degree,date,lang])
			
			mysql.connection.commit()
			f = request.files['file']
			f.save(os.path.join("C:/Users/SURESH/Desktop/clg python/flask_website/photos",f.filename))
			f = request.files['resume']
			f.save(os.path.join("C:/Users/SURESH/Desktop/clg python/flask_website/resume",f.filename))

			
		return render_template("user_home.html")
		


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))



if(__name__=='__main__'):
    app.secret_key='123'
    app.run(debug=True, port=8080)