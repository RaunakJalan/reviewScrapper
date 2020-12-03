from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import pymongo
from reviewScraping import reviewScrapper
import sys


app = Flask(__name__)

@app.route('/',methods=['GET'])
def homePage():
    return render_template("index.html")

@app.route('/review', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        searchString = request.form['content'].replace(" ","")
        try:
            dbConn = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
            db = dbConn["crawlerDb"]
            reviews = db[searchString].find({})
            if reviews.count() > 0:
                return render_template('results.html', reviews=reviews)
            else:
                table = db[searchString]
                prodReviewScrap = reviewScrapper(searchString)
                reviews = prodReviewScrap.reviewScrap()
                if reviews[0]['Name'] == '-':
                    return render_template('results.html', reviews=reviews)
                else:
                    for review in reviews:
                        x = table.insert(review)
                    return render_template('results.html', reviews=reviews)

        except:
            return "Something is Wrong!"

    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(port=8001, debug=True)
    # app.run(debug=True)
