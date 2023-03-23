from flask import Flask, request, make_response
from flask_cors import CORS

import content_based_filtering as cbf

app = Flask(__name__)
CORS(app)

@app.route("/recommendation", methods=["POST"])
def route_recommendation():
    if request.method == 'POST': 
        try:
            description = request.data
            raw_recommentadions = cbf.recommendation(description, cbf.data_restaurants)
            recommendations = cbf.restaurants_data(raw_recommentadions, cbf.data_frontend)
            return recommendations
        except:
            response = make_response()
            return response.json({"error": "Internal Server Error"})
