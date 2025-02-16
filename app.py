from flask import Flask, render_template, redirect, url_for 
import pymongo

app = Flask(__name__) 


@app.route("/")
def home():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    dbs = list(filter(lambda x: (x!= 'config' and x!= 'local' and x!= 'admin'),myclient.list_database_names()))
    return render_template("index.html",databases= dbs ) 

@app.route("/db/<db_name>") 
def db(db_name): 
	database = db_name
	return render_template("edit_db.html", database=db_name) 

@app.route("/default") 
def default(): 
	return render_template("layout.html") 


@app.route("/variable") 
def var(): 
	user = "Erik"
	return render_template("variable_example.html", name=user) 


@app.route("/if") 
def ifelse(): 
	user = "Practice GeeksforGeeks"
	return render_template("if_example.html", name=user) 


@app.route("/for") 
def for_loop(): 
	list_of_courses = ['Java', 'Python', 'C++', 'MATLAB'] 
	return render_template("for_example.html", courses=list_of_courses) 


@app.route("/choice/<pick>") 
def choice(pick): 
	if pick == 'variable': 
		return redirect(url_for('var')) 
	if pick == 'if': 
		return redirect(url_for('ifelse')) 
	if pick == 'for': 
		return redirect(url_for('for_loop')) 


if __name__ == "__main__": 
	app.run(debug=False) 
