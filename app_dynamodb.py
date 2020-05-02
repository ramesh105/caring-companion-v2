"""
Flask backend with DynamoDB
Client -> Flask -> DynamoDB
"""
import boto3
import json
from flask import Flask
from flask_cors import CORS,cross_origin
from flask import jsonify,request


#Add logging
#https://docs.aws.amazon.com/lambda/latest/dg/python-logging.html
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
app = Flask(__name__)

"""
Get all citizens present in the DB
"""
@app.route("/getcitizens")
@cross_origin()
def get_citizens():
    response = table.scan()["Items"]
    return jsonify(response)
    logger.info("All citizens returned")


@app.route("/getmatchingcitizens")
@cross_origin()
def get_matching_citizens():
    volunteer = request.headers.get('X-volunteer')
    vaibhav_interests = ['sleeping','home building','garden walks']
    arsalan_interests = ['music','politics','science','reading']
    # senior_list = [post for post in posts.find()]
    #get all citizens
    senior_list = table.scan()["Items"]
    if request.headers['X-volunteer'] == "Vaibhav":
        dummy_volunteer_interest_list = vaibhav_interests
        matching_list = []
        for senior in senior_list:
            match = len(set(dummy_volunteer_interest_list) & set(senior['interests'])) / float(len(set(dummy_volunteer_interest_list) | set(senior['interests']))) * 100
            if match >= 20:
                matching_list.append(senior)
        if len(matching_list) == 0:
            return(jsonify("No matches found!"))
        logger.info("Vaibhav Matching citizens returned")
    elif request.headers['X-volunteer'] == "Arsalan":
        dummy_volunteer_interest_list = arsalan_interests
        matching_list = []
        # senior_list = [post for post in posts.find()]
        for senior in senior_list:
            match = len(set(dummy_volunteer_interest_list) & set(senior['interests'])) / float(len(set(dummy_volunteer_interest_list) | set(senior['interests']))) * 100
            if match >= 20:
                matching_list.append(senior)
        if len(matching_list) == 0:
            return jsonify("No matches found!")
        logger.info("Arsalan Matching citizens returned")
    else:
        return jsonify("Send a valid user header!")
    return jsonify(matching_list)
    


if __name__ == "__main__":
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")
    table = dynamodb.Table('citizens')
    print("Connected to DynamoDB..")
    #run app on port 80
    app.run(port=80)
    
    