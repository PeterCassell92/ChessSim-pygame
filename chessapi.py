#!/usr/bin/python


# response = requests.get(
#     'https://api.github.com/search/repositories',
#     params={'q': 'requests+language:python'},
#     headers={'Accept': 'application/vnd.github.v3.text-match+json'},
# )
import json
import requests

def printResp(resp):
	print(resp.status_code)
	print(resp.content)
	print(resp.text)

def createGame():
	print("requesting new game")
	resp = requests.get("http://chess-api-chess.herokuapp.com/api/v1/chess/one")


	printResp(resp)
	textDict = json.loads(resp.text)

	return textDict.get('game_id')

def movePiece(currentGrid, targetGrid, gameID):
	print("player moving piece from " + currentGrid.lower() + " to " + targetGrid.lower())
	resp = requests.post('http://chess-api-chess.herokuapp.com/api/v1/chess/one/move/player',
		headers={'Content-Type':'application/x-www-form-urlencoded'},
		data = {'from': currentGrid.lower(),
				'to': targetGrid.lower(),
				'game_id': gameID
				}
			)
	printResp(resp)

def moveAI(gameID):
	print("moving using AI")
	resp = requests.post('http://chess-api-chess.herokuapp.com/api/v1/chess/one/move/ai',
		headers = {'Content-Type': 'application/x-www-form-urlencoded'},
		data = {
				'game_id': gameID
				})
	printResp(resp)

	textDict = json.loads(resp.text)

	return textDict.get('from'), textDict.get('to')


def checkGameover(gameID):
	resp = requests.post('http://chess-api-chess.herokuapp.com/api/v1/chess/one/check',
		headers={'Content-Type': 'application/x-www-form-urlencoded'},
		data= {
				'game_id': gameID
				}
			)
	textDict = json.loads(resp.text)
	printResp(resp)
	return textDict.get('status')
# 	curl --location --request POST 'http://chess-api-chess.herokuapp.com/api/v1/chess/one/check' \
# --header 'Content-Type: application/x-www-form-urlencoded' \
# --data-urlencode 'game_id=5a3c356be4538a2628f17ca4'


# 	curl --location --request POST 'http://chess-api-chess.herokuapp.com/api/v1/chess/one/move/ai' \
# --header 'Content-Type: application/x-www-form-urlencoded' \
# --data-urlencode 'game_id=5a43c4f3d326e114807278d2'



	# curl --location --request POST 'http://chess-api-chess.herokuapp.com/api/v1/chess/one/move/player' \
	# --header 'Content-Type: application/x-www-form-urlencoded' \
	# --data-urlencode 'from=a2' \
	# --data-urlencode 'to=a3' \
	# --data-urlencode 'game_id=5a43ca62772e4e00148e207b'