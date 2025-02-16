from flask import Flask, render_template, redirect, url_for, request
import pymongo
from bson.json_util import dumps

app = Flask(__name__)

# @app.route("/")
# def home():
#     myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#     dbs = list(filter(lambda x: (x!= 'config' and x!= 'local' and x!= 'admin'),myclient.list_database_names()))
#     return render_template("index.html",databases= dbs ) 

# @app.route("/database/<db_name>", methods=['GET','POST']) 
# def db_edit(db_name):
#     if request.method=='POST': 
#         myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#         myclient.drop_database(db_name)
#         return redirect(url_for('home')) 
#     else: 
#         database = db_name
#         myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#         mydb = myclient[db_name]
#         return render_template("edit_db.html", database=db_name, collections =mydb.list_collection_names()) 
	
# @app.route("/database/<db_name>/<col_name>", methods=['GET','POST']) 
# def col_edit(db_name, col_name):
#     if request.method=='POST': 
#         myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#         mydb = myclient[db_name]
#         mydb.drop_collection(col_name)
#         return redirect(url_for('db_edit', db_name = db_name)) 
#     else: 
#         database = db_name
#         myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#         mydb = myclient[db_name]
#         mycol = mydb[col_name]
#         documents = mycol.find({})
#         print(documents)
#         return render_template("edit_col.html", database=db_name, collection =col_name, documents = list(mycol.find({}))) 


# @app.route("/database", methods=['POST']) 
# def db_create(): 
#     print('Got Request to create database')
#     print('database name: '+request.form['database'])
#     myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#     mydb = myclient[request.form['database']]
#     mycol = mydb[request.form['collection']]
# 	#create data so mongodb actually create collection
#     mydict = { "message": "Hello World", "author":"James Bond" }
#     x = mycol.insert_one(mydict)
# 	#delete data, so the collection is empty
#     myquery = { "message": "Hello World" }
#     mycol.delete_one(myquery)
#     return redirect(url_for('home')) 






@app.route("/", methods=['POST','GET']) 
def workspace():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/") 
    if request.method =='POST':
        #check if delete or create
        type = request.form['type']
        if type =='create':
            #create database with database name and default collection
            mydb = myclient[request.form['database']]
            #create default collection
            mycol = mydb['default']
            #create data so mongodb actually create collection
            mydict = { "message": "Hello World", "author":"James Bond" }
            x = mycol.insert_one(mydict)
            #delete data, so the collection is empty
            myquery = { "message": "Hello World" }
            mycol.delete_one(myquery)
        elif type == 'delete':
            myclient.drop_database(request.form['database'])
        
    dbs = list(filter(lambda x: (x!= 'config' and x!= 'local' and x!= 'admin'),myclient.list_database_names()))
    return render_template("index.html",databases= dbs ) 

@app.route("/<string:database>", methods=['POST','GET']) 
def database(database):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient[database]
    if request.method =='POST':
        #check if delete or create
        type = request.form['type']
        if type =='create':
            #create  collection
            mycol = mydb[request.form['collection']]
            #create data so mongodb actually create collection
            mydict = { "message": "Hello World", "author":"James Bond" }
            x = mycol.insert_one(mydict)
            #delete data, so the collection is empty
            myquery = { "message": "Hello World" }
            mycol.delete_one(myquery)
        elif type=='delete':
            mydb.drop_collection(request.form['collection'])
    cols = mydb.list_collection_names()
    return render_template("database.html",database= database,collections= cols ) 

@app.route("/<string:database>/<string:collection>", methods=['POST','GET']) 
def collection(database, collection):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient[database] 
    mycol = mydb[collection]
    if request.method =='POST':
        print('create doc')
    docs = list(mycol.find({}))
    return render_template("collection.html",database= database,collection= collection, documents = docs ) 

if __name__ == "__main__": 
	app.run(debug=False) 
