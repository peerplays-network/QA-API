import json
import yaml
from flask import Flask
from flask import request
import requests
from flask import redirect
from flask import jsonify
from peerplays import PeerPlays
from peerplaysbase import operations
from peerplays.amount import Amount

app = Flask(__name__)
market_maker_url = ""

@app.route("/placeBets", methods=['POST'])
def placeBets():
	response = requests.post(url + request.full_path, json = request.get_json())
	return (response.content, response.status_code, response.headers.items())

@app.route("/bets/<bet_id>", methods=['DELETE'])
def cancelBets(bet_id):
	# TODO cancel by event id, bmg id
	response = requests.delete(url + request.full_path)
	return (response.content, response.status_code, response.headers.items())

@app.route("/bettors/<bettor_id>/unmatchedBets/", methods=['GET'])
def getUnmatchedBets(bettor_id):
	response = requests.get(url + request.full_path)
	return (response.content, response.status_code, response.headers.items())

@app.route("/bettors/<bettor_id>/history", methods=['GET'])
def getHistory(bettor_id):
	response = requests.post(url + request.full_path)
	return (response.content, response.status_code, response.headers.items())

@app.route("/sports", methods=['GET'])
def getSports():
	response = requests.get(url + request.full_path)
	return (response.content, response.status_code, response.headers.items())

@app.route("/sports/<sport_id>/eventGroups")
def getEventGroups(sport_id):
	response = requests.get(url + request.full_path)
	return (response.content, response.status_code, response.headers.items())

@app.route("/eventGroups/<event_group_id>/events")
def getEvents(event_group_id):
	response = requests.get(url + request.full_path)
	return (response.content, response.status_code, response.headers.items())

@app.route("/events/<event_id>/bettingMarketGroups")
def getBettingMarketGroups(event_id):
	response = requests.get(url + request.full_path)
	return (response.content, response.status_code, response.headers.items())

@app.route("/bettingMarketGroups/<bmg_id>/bettingMarkets")
def getBettingMarkets(bmg_id):
	response = requests.get(url + request.full_path)
	return (response.content, response.status_code, response.headers.items())

@app.route("/rules/<rules_id>")
def getRules(rules_id):
	response = requests.get(url + request.full_path)
	return (response.content, response.status_code, response.headers.items())

if __name__ == '__main__':
	with open("config.yaml", 'r') as stream:
		try:
			config = yaml.safe_load(stream)
			url = config['market-maker']['url']
		except yaml.YAMLError as exc:
			print(exc)
		app.run(debug=False, host='0.0.0.0')