from flask import Flask, render_template, redirect, url_for, request
import pymongo

app = Flask(__name__) 


@app.route("/")
def home():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    dbs = list(filter(lambda x: (x!= 'config' and x!= 'local' and x!= 'admin'),myclient.list_database_names()))
    return render_template("index.html",databases= dbs ) 

@app.route("/database/<db_name>", methods=['GET','POST']) 
def db_edit(db_name):
    if request.method=='POST': 
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        myclient.drop_database(db_name)
        return redirect(url_for('home')) 
    else: 
        database = db_name
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient[db_name]
        return render_template("edit_db.html", database=db_name, collections =mydb.list_collection_names()) 
	
@app.route("/database/<db_name>/<col_name>", methods=['GET','POST']) 
def col_edit(db_name, col_name):
    if request.method=='POST': 
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient[db_name]
        mydb.drop_collection(col_name)
        return redirect(url_for('db_edit')) 
    else: 
        database = db_name
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient[db_name]
        return render_template("edit_col.html", database=db_name, collection =col_name) 


@app.route("/database", methods=['POST']) 
def db_create(): 
    print('Got Request to create database')
    print('database name: '+request.form['database'])
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient[request.form['database']]
    mycol = mydb[request.form['collection']]
	#create data so mongodb actually create collection
    mydict = { "message": "Hello World", "author":"James Bond" }
    x = mycol.insert_one(mydict)
	#delete data, so the collection is empty
    myquery = { "message": "Hello World" }
    mycol.delete_one(myquery)
    return redirect(url_for('home')) 

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
