from flask import Flask, render_template, redirect, url_for, request
import pymongo, json
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)


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
        type = request.form['type']
        doc = request.form['document']
        if type =='create':
            try:
                data = json.loads(doc.replace("\r", "").replace("\n", "").replace(" ",""))
                result = mycol.insert_one(data)
                print('Document was successfully added: '+str(result.inserted_id))
            except:
                print('invalid json')
        if type =='update':
            mycol.update_one(doc)
        if type =='delete':
            query = {'_id': ObjectId(doc)}
            result = mycol.delete_one(query)
            # Check if the document was deleted
            if result.deleted_count > 0:
                print("Document deleted successfully: "+ str(doc))
            else:
                print("No document found with the given ID.")
    docs = list(mycol.find({}))
    for doc in docs:
        print(doc['_id'])
        doc['_id'] = str(doc['_id'])
    return render_template("collection.html",database= database,collection= collection, documents = docs ) 

if __name__ == "__main__": 
	app.run(debug=True) 
