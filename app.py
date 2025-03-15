from flask import Flask, render_template, redirect, url_for, request, flash
import pymongo, json, ast
from bson.json_util import dumps
from bson.objectid import ObjectId
import collections  # From Python standard library.
import bson
from bson.codec_options import CodecOptions

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


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
    id = False

    if request.method =='POST':
        type = request.form['type']
        try:
            doc = request.form['document']
        except:
            selected_doc = request.form['document_editor']
            selected_id = request.form['document_editor_doc_id']
        if type =='create':
            try:
                data = json.loads(doc.replace("\r", "").replace("\n", "").replace(" ",""))
                result = mycol.insert_one(data)
                print('Document was successfully added: '+str(result.inserted_id))
            except:
                print('invalid json')
                flash("Invalid json",'error')
        if type =='update':
            print('received update request for id: '+ selected_id)
            print('received update request for doc:'+selected_doc)
            try:
                update_doc = ast.literal_eval(selected_doc)
                update_doc["_id"] = ObjectId(selected_id)
                result = mycol.replace_one({'_id': ObjectId(selected_id)},update_doc)
                if(result.modified_count == 0):
                    info = 'no updates were made, because there was no change'
                else:
                    info = 'successfully modified '+ str(result.modified_count) + ' documents'
                flash(info, 'info')
            except:
                flash('something went wrong, please check if document is valid', 'error')
            docs = list(mycol.find({}))
            for doc in docs:
                print(doc['_id'])
                doc['_id'] = str(doc['_id'])
            return render_template("collection.html",database= database,collection= collection, documents = docs, selected_id= selected_id, selected_doc = selected_doc ) 

        if type =='delete':
            query = {'_id': ObjectId(doc)}
            result = mycol.delete_one(query)
            # Check if the document was deleted
            if result.deleted_count > 0:
                print("Document deleted successfully: "+ str(doc))
            else:
                print("No document found with the given ID.")
                flash("Document not found, ignored delete request", 'warning')
    docs = list(mycol.find({}))
    for doc in docs:
        print(doc['_id'])
        doc['_id'] = str(doc['_id'])
    return render_template("collection.html",database= database,collection= collection, documents = docs ) 

if __name__ == "__main__": 
	app.run(debug=True) 
