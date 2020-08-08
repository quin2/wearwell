import json
from flask import Flask, jsonify, Response, request, current_app

app = Flask(__name__)

@app.route('/')
def index():
	return "usage: send website URL as {url: 'https://example.com'} to /v1/score and get sustainability info back"

@app.route('/v1/score', methods=['POST'])
def susScore():
	#load from request
	data = request.json
	toScrape = data['url']

	return jsonify (
		score=9.8,
	)

if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True, port=80)
