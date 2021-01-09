from flask import Flask, render_template, request, jsonify
from flask_cors import CORS,cross_origin
from reviewScraping import reviewScrapper
import os
import json

app = Flask(__name__)

@app.route('/',methods=['GET'])
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/review', methods = ['POST', 'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        reviews = []
        searchString = request.form['content'].replace(" ","")
        if os.path.exists(searchString):
            with open(searchString,"r") as review_file:
                reviews = json.load(review_file)
        else:
            prodReviewScrap = reviewScrapper(searchString)
            reviews = prodReviewScrap.reviewScrap()
            with open(searchString,"w") as review_file:
                json.dump(reviews, review_file)
        return render_template('results.html', reviews=reviews)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    # app.run(port=8001, debug=True)
    port = int(os.environ.get('PORT','5000'))
    app.run(debug=True, port = port)

