from flask import Flask, render_template,request,redirect,url_for
from bson import ObjectId
from pymongo import MongoClient
import os



app = Flask(__name__)

client = MongoClient("mongodb://127.0.0.1:27017") #host uri  
db = client.todo_app #Select the database  
todos = db.todo #Select the collection name 

@app.route('/')
def index():
    all_todos = todos.find()
    return render_template('index.html',todos=all_todos)

@app.route('/insert', methods=['post'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['desc']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        pr = request.form['pr']
        todos.insert({ "name":name, "desc":desc, "start_date":start_date, "end_date":end_date, "pr":pr,"done":"no"})    
    return redirect("/")

@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        desc = request.form['desc']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        pr = request.form['pr']
        todos.update({"_id":ObjectId(id)}, {'$set':{ "name":name, "desc":desc, "start_date":start_date, "end_date":end_date, "pr":pr}})    
        return redirect(url_for('index'))

@app.route('/delete/<string:id_data>', methods=['GET'])
def delete(id_data):
    # flash("Record Has Been Deleted Successfully")
    key=id_data
    todos.remove({"_id":ObjectId(key)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)