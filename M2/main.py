import atexit
import logging
import requests
import sys
from flask import Flask, render_template, request,render_template_string,redirect
import json
from Models.query import Query
from Models.db import Database
from Models.webpage import Webpage

app = Flask(__name__)
database = Database("mongodb://localhost:27017", "SearchEngine")

cache = []

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/search', methods=['POST','GET'])
def search():

    page = request.args.get('page', 0, type=int)

    if page == 0:
        query = request.form['query']
        page = 1
    else:
        query = request.args.get('query',type=str)
    
    dIDs = Query(query, database).findRankedResults()
    max_page = round(len(dIDs)/10)
    


    start = (page-1)*10
    end = (start + 10) if page < max_page else len(dIDs)

    prev = page - 1 if page > 1 else None
    next = page + 1 if page < max_page else None

    results = []
    for dID,weight in list(dIDs.items())[start:end]:
        webpage = Webpage(dID)
        results.append(webpage)        
    return render_template('results.html', results=results, page=page, prev=prev, next=next, query=query)



@app.route('/page/<folder>/<file>')
def page(folder,file):
    wp = Webpage(f"{folder}/{file}")
    try:
        resp = requests.get("https://"+wp.getURL(),timeout= 5)
        response = redirect("https://"+wp.getURL())
    except Exception:
        content = wp.getContent().decode()
        return render_template_string(content)

    print(resp.status_code)
    if response.status_code != 302  or resp.status_code != 200:
        content = wp.getContent().decode()
        return render_template_string(content)
    return response
   



if __name__ == "__main__":
    app.run(debug=True)
    

