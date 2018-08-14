import json
import yaml
from flask import Flask
from flask import request
from flask import make_response
import requests
from flask import redirect
from flask import jsonify
from datetime import datetime
from peerplays import PeerPlays
from peerplaysbase import operations
from peerplays.amount import Amount
import mint

app = Flask(__name__)

@app.route("/placeBets", methods=['POST'])
def placeBets():
	"""
	**POST** ``/placeBets``

	* query-params:
		+ account:
			- type: string
			- description: account name or account id

	* body:
	.. code-block:: json

		[{
			"asset_symbol": "BTF",
			"bet_amount": 1,
			"betting_market_id": "1.21.3119",
			"odds": 1.44,
			"back_or_lay": "back"
		}]

	* returns:
		+ 200:
		.. code-block:: json

			[
		       {
		         "expiration": "2018-07-04T05:07:11",
		         "extensions": [],
		         "operations": [
		           [
		               62,
		               {
		                   "amount_to_bet": {
		                       "amount": 100000000,
		                       "asset_id": "1.3.1"
		                   },
		                   "back_or_lay": "back",
		                   "backer_multiplier": 14400,
		                   "betting_market_id": "1.21.3119",
		                   "bettor_id": "1.2.18",
		                   "extensions": [],
		                   "fee": {
		                       "amount": 1000,
		                       "asset_id": "1.3.1"
		                   }
		               }
		           ]
		         ],
		         "ref_block_num": 60890,
		         "ref_block_prefix": 3193047218,
		         "signatures": [
		           "200e759209844e2370cddc60e42d880c2ed62f446f3799c6ab32ad95d3e69038b2786482393ead92a94aa9367176449b274305197502c8baf71efa308ab28c57a8"
		         ]
		       }
         	 ]

	"""
	response = requests.post(market_maker_url + request.full_path, json = request.get_json())
	return (response.content, response.status_code, response.headers.items())

@app.route("/placeSingleBet", methods=['POST'])
def placeSingleBet():
	"""
	**POST** ``/placeSingleBet``

	* query-params:
		+ account:
			- type: string
			- description: account name or account id

	* body:
	.. code-block:: json

		{
			"asset_symbol": "BTF",
			"bet_amount": 1,
			"betting_market_id": "1.21.3295",
			"odds": 1.44,
			"back_or_lay": "back"
		}

	* returns:
		+ 200:
		.. code-block:: json

			{
			    "amount_to_bet": {
			        "amount": 10000000,
			        "asset_id": "1.3.1"
			    },
			    "back_or_lay": "back",
			    "backer_multiplier": 100000,
			    "betting_market_id": "1.21.3295",
			    "bettor_id": "1.2.104",
			    "id": "1.22.1074"
			}

	"""
	response = requests.post(market_maker_url + request.full_path, json = request.get_json())
	return (response.content, response.status_code, response.headers.items())

@app.route("/bets/<bet_id>", methods=['DELETE'])
def cancelBets(bet_id):
	"""
	**DELETE** ``/bets/<bet_id>``

	* query-params:
		+ account:
			- type: string
			- description: account name or account id

	* path-params:
		+ bet_id:
			- type: string
			- description: bet id

	* returns:
		+ 200:
		.. code-block:: json

			{
			    "expiration": "2018-07-05T04:15:16",
			    "extensions": [],
			    "operations": [
			        [
			            68,
			            {
			                "bet_to_cancel": "1.22.533",
			                "bettor_id": "1.2.18",
			                "extensions": [],
			                "fee": {
			                    "amount": 0,
			                    "asset_id": "1.3.1"
			                }
			            }
			        ]
			    ],
			    "ref_block_num": 22274,
			    "ref_block_prefix": 3672811153,
			    "signatures": [
			        "201e63f37f76aa86639bb6a2f74affddef453371d065ee2748a050962d191cf19054acb1c6f0646a9e646ae12e2ac569d816208619447c5b86b385d041e1aab06c"
			    ]
			}

	"""
	# TODO cancel by event id, bmg id
	response = requests.delete(market_maker_url + request.full_path)
	return (response.content, response.status_code, response.headers.items())

@app.route("/bettors/<bettor_id>/matchedBets", methods=['GET'])
def getMatchedBets(bettor_id):
	"""
	**GET** ``/bettors/<bettor_id>/matchedBets``

	* path-params:
		+ bettor_id:
			- type: string
			- description: account name

	* returns:
		+ 200:
		.. code-block:: json

			[
			    {
			        "amount_matched": 295400,
			        "amount_to_bet": {
			            "amount": 4600,
			            "asset_id": "1.3.1"
			        },
			        "associated_operations": [
			            "1.11.13540",
			            "1.11.13558"
			        ],
			        "back_or_lay": "back",
			        "backer_multiplier": 0,
			        "betting_market_id": "1.21.3135",
			        "bettor_id": "1.2.104",
			        "id": "1.22.794"
			    },
			    {
			        "amount_matched": 295400,
			        "amount_to_bet": {
			            "amount": 4600,
			            "asset_id": "1.3.1"
			        },
			        "associated_operations": [
			            "1.11.13533",
			            "1.11.13557"
			        ],
			        "back_or_lay": "back",
			        "backer_multiplier": 0,
			        "betting_market_id": "1.21.3134",
			        "bettor_id": "1.2.104",
			        "id": "1.22.792"
			    }
			]	

	"""
	response = requests.get(market_maker_url + request.full_path)
	return (response.content, response.status_code, response.headers.items())

@app.route("/bettors/<bettor_id>/unmatchedBets", methods=['GET'])
def getUnmatchedBets(bettor_id):
	"""
	**GET** ``/bettors/<bettor_id>/unmatchedBets``

	* path-params:
		+ bettor_id:
			- type: string
			- description: account name

	* returns:
		+ 200:
		.. code-block:: json

			[
			    {
			        "amount_to_bet": {
			            "amount": 10000000,
			            "asset_id": "1.3.1"
			        },
			        "back_or_lay": "back",
			        "backer_multiplier": 17000,
			        "betting_market_id": "1.21.3134",
			        "bettor_id": "1.2.18",
			        "id": "1.22.537"
			    },
			    {
			        "amount_to_bet": {
			            "amount": 10000000,
			            "asset_id": "1.3.1"
			        },
			        "back_or_lay": "back",
			        "backer_multiplier": 17000,
			        "betting_market_id": "1.21.3134",
			        "bettor_id": "1.2.18",
			        "id": "1.22.538"
			    }
			]	

	"""
	response = requests.get(market_maker_url + request.full_path)
	return (response.content, response.status_code, response.headers.items())

@app.route("/sports/<sport_id>", methods=['GET'])
def getSport(sport_id):
	"""
	**GET** ``/sports/<sport_id>``

	* path-params:
		+ sport_id
			- type: string
			- description: sport id
	* returns:
		+ 200:
		.. code-block:: json

		    {
		        "id": "1.16.0",
		        "name": [
		            [
		                "en",
		                "Soccer"
		            ],
		            [
		                "identifier",
		                "Soccer"
		            ],
		            [
		                "sen",
		                "Soccer"
		            ]
		        ]
		    }	

	"""
	response = requests.get(market_maker_url + request.full_path)
	return (response.content, response.status_code, response.headers.items())

@app.route("/sports", methods=['GET'])
def getSports():
	"""
	**GET** ``/sports``

	* returns:
		+ 200:
		.. code-block:: json

			[
			    {
			        "id": "1.16.0",
			        "name": [
			            [
			                "en",
			                "Soccer"
			            ],
			            [
			                "identifier",
			                "Soccer"
			            ],
			            [
			                "sen",
			                "Soccer"
			            ]
			        ]
			    },
			    {
			        "id": "1.16.1",
			        "name": [
			            [
			                "en",
			                "Baseball"
			            ],
			            [
			                "identifier",
			                "Baseball"
			            ],
			            [
			                "sen",
			                "Baseball"
			            ]
			        ]
			    },
			]	

	"""
	response = requests.get(market_maker_url + request.full_path)
	return (response.content, response.status_code, response.headers.items())

@app.route("/eventGroups/<event_group_id>", methods=['GET'])
def getEventGroup(event_group_id):
	"""
	**GET** ``/sports/<sport_id>/eventGroups``

	* path-params:
		+ sport_id:
			- type: string
			- description: sport id

	* returns:
		+ 200:
		.. code-block:: json

		    {
		        "id": "1.17.1",
		        "name": [
		            [
		                "en",
		                "UEFA Europa League"
		            ],
		            [
		                "identifier",
		                "UEFA Europa League"
		            ],
		            [
		                "sen",
		                "Europa League"
		            ]
		        ],
		        "sport_id": "1.16.0"
		    }

	"""
	response = requests.get(market_maker_url + request.full_path)
	return (response.content, response.status_code, response.headers.items())

@app.route("/sports/<sport_id>/eventGroups", methods=['GET'])
def getEventGroups(sport_id):
	"""
	**GET** ``/sports/<sport_id>/eventGroups``

	* path-params:
		+ sport_id:
			- type: string
			- description: sport id

	* returns:
		+ 200:
		.. code-block:: json

			[
			    {
			        "id": "1.17.1",
			        "name": [
			            [
			                "en",
			                "UEFA Europa League"
			            ],
			            [
			                "identifier",
			                "UEFA Europa League"
			            ],
			            [
			                "sen",
			                "Europa League"
			            ]
			        ],
			        "sport_id": "1.16.0"
			    },
			    {
			        "id": "1.17.5",
			        "name": [
			            [
			                "en",
			                "FA Cup"
			            ],
			            [
			                "identifier",
			                "FA Cup"
			            ],
			            [
			                "sen",
			                "FA Cup"
			            ]
			        ],
			        "sport_id": "1.16.0"
			    }
			]

	"""
	response = requests.get(market_maker_url + request.full_path)
	return (response.content, response.status_code, response.headers.items())

@app.route("/events/<event_id>", methods=['GET'])
def getEvent(event_id):
	"""
	**GET** ``/events/<event_id>``

	* path-params:
		+ event_id:
			- type: string
			- description: event id

	* returns:
		+ 200:
		.. code-block:: json

		    {
		        "event_group_id": "1.17.8",
		        "id": "1.18.286",
		        "name": [
		            [
		                "en",
		                "Uruguay v France"
		            ]
		        ],
		        "scores": [],
		        "season": [
		            [
		                "en",
		                "2018"
		            ]
		        ],
		        "start_time": "2018-07-06T14:00:00",
		        "status": "upcoming"
		    }

	"""
	response = requests.get(market_maker_url + request.full_path)
	return (response.content, response.status_code, response.headers.items())

@app.route("/eventGroups/<event_group_id>/events", methods=['GET'])
def getEvents(event_group_id):
	"""
	**GET** ``/eventGroups/<event_group_id>/events``

	* path-params:
		+ event_group_id:
			- type: string
			- description: event group id

	* returns:
		+ 200:
		.. code-block:: json

			[
			    {
			        "event_group_id": "1.17.8",
			        "id": "1.18.286",
			        "name": [
			            [
			                "en",
			                "Uruguay v France"
			            ]
			        ],
			        "scores": [],
			        "season": [
			            [
			                "en",
			                "2018"
			            ]
			        ],
			        "start_time": "2018-07-06T14:00:00",
			        "status": "upcoming"
			    },
			    {
			        "event_group_id": "1.17.8",
			        "id": "1.18.288",
			        "name": [
			            [
			                "en",
			                "Russia v Croatia"
			            ]
			        ],
			        "scores": [],
			        "season": [
			            [
			                "en",
			                "2018"
			            ]
			        ],
			        "start_time": "2018-07-07T18:00:00",
			        "status": "upcoming"
			    }
			]

	"""
	response = requests.get(market_maker_url + request.full_path)
	return (response.content, response.status_code, response.headers.items())

@app.route("/bettingMarketGroups/<bmg_id>", methods=['GET'])
def getBettingMarketGroup(bmg_id):
	"""
	**GET** ``/bettingMarketGroups/<bmg_id>``

	* path-params:
		+ bmg_id:
			- type: string
			- description: bmg id

	* returns:
		+ 200:
		.. code-block:: json

		    {
		        "asset_id": "1.3.1",
		        "delay_before_settling": 0,
		        "description": [
		            [
		                "display_name",
		                "Match Odds"
		            ],
		            [
		                "en",
		                "Match Odds"
		            ],
		            [
		                "sen",
		                "Match Odds"
		            ]
		        ],
		        "event_id": "1.18.286",
		        "id": "1.20.1495",
		        "never_in_play": false,
		        "rules_id": "1.19.1",
		        "settling_time": null,
		        "status": "upcoming",
		        "total_matched_bets_amount": 3993000
		    }

	"""
	response = requests.get(market_maker_url + request.full_path)
	return (response.content, response.status_code, response.headers.items())

@app.route("/events/<event_id>/bettingMarketGroups", methods=['GET'])
def getBettingMarketGroups(event_id):
	"""
	**GET** ``/events/<event_id>/bettingMarketGroups``

	* path-params:
		+ event_id:
			- type: string
			- description: event id

	* returns:
		+ 200:
		.. code-block:: json

			[
			    {
			        "asset_id": "1.3.1",
			        "delay_before_settling": 0,
			        "description": [
			            [
			                "display_name",
			                "Match Odds"
			            ],
			            [
			                "en",
			                "Match Odds"
			            ],
			            [
			                "sen",
			                "Match Odds"
			            ]
			        ],
			        "event_id": "1.18.286",
			        "id": "1.20.1495",
			        "never_in_play": false,
			        "rules_id": "1.19.1",
			        "settling_time": null,
			        "status": "upcoming",
			        "total_matched_bets_amount": 3993000
			    },
			    {
			        "asset_id": "1.3.1",
			        "delay_before_settling": 0,
			        "description": [
			            [
			                "display_name",
			                "Over/Under 0.5 Goals"
			            ],
			            [
			                "en",
			                "Over/Under 0.5 Goals"
			            ],
			            [
			                "sen",
			                "O/U 0.5"
			            ]
			        ],
			        "event_id": "1.18.286",
			        "id": "1.20.1496",
			        "never_in_play": false,
			        "rules_id": "1.19.4",
			        "settling_time": null,
			        "status": "upcoming",
			        "total_matched_bets_amount": 0
			    }
			]

	"""
	response = requests.get(market_maker_url + request.full_path)
	return (response.content, response.status_code, response.headers.items())

@app.route("/bettingMarket", methods=['GET'])
def getBettingMarketByQuery():
	"""
	**GET** ``/bettingMarket``

	* query-params:
		+ sport:
			- type: string
			- description: sport name
		+ eventGroup:
			- type: string
			- description: event group name
		+ event:
			- type: string
			- description: event name
		+ bettingMarketGroup:
			- type: string
			- description: betting market group name
		+ bettingMarket:
			- type: string
			- description: betting market name

	* returns:
		+ 200:
		.. code-block:: json

		    {
		        "description": [
		            [
		                "en",
		                "Philadelphia Phillies"
		            ]
		        ],
		        "group_id": "1.20.1578",
		        "id": "1.21.3292",
		        "payout_condition": [],
		        "resolution": null,
		        "status": "unresolved"
		    }

	"""
	response = requests.get(market_maker_url + request.full_path)
	return (response.content, response.status_code, response.headers.items())

@app.route("/bettingMarkets/<betting_market_id>", methods=['GET'])
def getBettingMarket(betting_market_id):
	"""
	**GET** ``/bettingMarkets/<betting_market_id>``

	* path-params:
		+ betting_market_id:
			- type: string
			- description: betting market id

	* returns:
		+ 200:
		.. code-block:: json

		    {
		        "description": [
		            [
		                "en",
		                "Philadelphia Phillies"
		            ]
		        ],
		        "group_id": "1.20.1578",
		        "id": "1.21.3292",
		        "payout_condition": [],
		        "resolution": null,
		        "status": "unresolved"
		    }

	"""
	response = requests.get(market_maker_url + request.full_path)
	return (response.content, response.status_code, response.headers.items())

@app.route("/bettingMarketGroups/<bmg_id>/bettingMarkets", methods=['GET'])
def getBettingMarkets(bmg_id):
	"""
	**GET** ``/bettingMarketGroups/<bmg_id>/bettingMarkets``

	* path-params:
		+ bmg_id:
			- type: string
			- description: betting market group id

	* returns:
		+ 200:
		.. code-block:: json

			[
			    {
			        "description": [
			            [
			                "en",
			                "Uruguay"
			            ]
			        ],
			        "group_id": "1.20.1495",
			        "id": "1.21.3119",
			        "payout_condition": [],
			        "resolution": null,
			        "status": "unresolved"
			    },
			    {
			        "description": [
			            [
			                "en",
			                "France"
			            ]
			        ],
			        "group_id": "1.20.1495",
			        "id": "1.21.3120",
			        "payout_condition": [],
			        "resolution": null,
			        "status": "unresolved"
			    },
			    {
			        "description": [
			            [
			                "en",
			                "The Draw"
			            ]
			        ],
			        "group_id": "1.20.1495",
			        "id": "1.21.3121",
			        "payout_condition": [],
			        "resolution": null,
			        "status": "unresolved"
			    }
			]

	"""
	response = requests.get(market_maker_url + request.full_path)
	return (response.content, response.status_code, response.headers.items())

@app.route("/rules/<rules_id>", methods=['GET'])
def getRules(rules_id):
	"""
	**GET** ``/rules/<rules_id>``

	* path-params:
		+ rules_id:
			- type: string
			- description: rules id
	* returns:
		+ 200:
		.. code-block:: json

			{
			    "description": [
			        [
			            "en",
			            "MARKET INFORMATION How many goals in total will be scored in this match - more or less than the stated number? All bets apply to Full Time result according to the match officials, plus any stoppage time. Extra-time/penalty shoot-outs are not included. At the start of play any unmatched bets will be automatically cancelled and the market will turn in-play. Please note that this market will not be actively managed therefore it is the responsibility of all users to manage their in-play positions. Please also be aware that transmissions described as “live” may actually involve a certain time delay which can vary from case to case. Commission and Transaction Fees apply to all bets placed in this market. For further information please see Bookie Rules."
			        ],
			        [
			            "grading",
			            "{\"metric\": \"{result.hometeam} + {result.awayteam}\", \"resolutions\": [{\"not_win\": \"{metric} > 5.5\", \"void\": \"False\", \"win\": \"{metric} < 5.5\"}, {\"not_win\": \"{metric} < 5.5\", \"void\": \"False\", \"win\": \"{metric} > 5.5\"}]}"
			        ]
			    ],
			    "id": "1.19.0",
			    "name": [
			        [
			            "en",
			            "R_Soccer_OU_5.5_1"
			        ],
			        [
			            "identifier",
			            "R_Soccer_OU_5.5_1"
			        ]
			    ]
			}

	"""
	response = requests.get(market_maker_url + request.full_path)
	return (response.content, response.status_code, response.headers.items())

# MINT Calls

@app.route("/sports", methods=['POST'])
def createSport():
	"""
	**POST** ``/sports``

	* body:
	.. code-block:: json

		{
			"name": [["en", "Michael Sport"], ["de", "Michael Spoort"]]
		}

	* returns:
		+ 200:
		.. code-block:: json

			{
			    "expiration": "2018-08-14T03:25:59",
			    "extensions": [],
			    "operations": [
			        [
			            22,
			            {
			                "expiration_time": "2018-08-15T03:25:29",
			                "extensions": [],
			                "fee": {
			                    "amount": 2000000,
			                    "asset_id": "1.3.0"
			                },
			                "fee_paying_account": "1.2.7",
			                "proposed_ops": [
			                    {
			                        "op": [
			                            52,
			                            {
			                                "extensions": [],
			                                "fee": {
			                                    "amount": 0,
			                                    "asset_id": "1.3.0"
			                                },
			                                "name": [
			                                    [
			                                        "de",
			                                        "Michael Spoort"
			                                    ],
			                                    [
			                                        "en",
			                                        "Michael Sport"
			                                    ]
			                                ]
			                            }
			                        ]
			                    }
			                ]
			            }
			        ]
			    ],
			    "ref_block_num": 24645,
			    "ref_block_prefix": 3184223600,
			    "signatures": [
			        "1f57acd0862ad0ecfa7d6ca5f7857a803af725b92e325af9aab5e0ea118fa0174d2f9a61646d914f6543d530446d798af12675e04ab81c0db8ea351eda0b80ee96"
			    ]
			}

	"""
	try:
		body = request.get_json()
		name = body['name']
		return jsonify(mint.createSport(name))
	except Exception as e:
		return make_response(jsonify(error=str(e)), 500)

@app.route("/sports", methods=['PUT'])
def updateSport():
	"""
	**PUT** ``/sports``

	* body:
	.. code-block:: json

		{
			"name": [["en", "Michael Sport"], ["de", "Michael Sporte"]],
			"sport_id": "1.16.9"
		}

	* returns:
		+ 200:
		.. code-block:: json

			{
			    "expiration": "2018-08-14T03:50:00",
			    "extensions": [],
			    "operations": [
			        [
			            22,
			            {
			                "expiration_time": "2018-08-15T03:49:30",
			                "extensions": [],
			                "fee": {
			                    "amount": 2000000,
			                    "asset_id": "1.3.0"
			                },
			                "fee_paying_account": "1.2.7",
			                "proposed_ops": [
			                    {
			                        "op": [
			                            53,
			                            {
			                                "extensions": [],
			                                "fee": {
			                                    "amount": 0,
			                                    "asset_id": "1.3.0"
			                                },
			                                "new_name": [
			                                    [
			                                        "de",
			                                        "Michael Sporte"
			                                    ],
			                                    [
			                                        "en",
			                                        "Michael Sport"
			                                    ]
			                                ],
			                                "sport_id": "1.16.9"
			                            }
			                        ]
			                    }
			                ]
			            }
			        ]
			    ],
			    "ref_block_num": 25111,
			    "ref_block_prefix": 2306565201,
			    "signatures": [
			        "202260fd3551a76d9ceba1ed9c5a6aab080365de67b5282bf9e74ea461875ae2e362f91d2441f4c7000862ceb8005169bcf2605f0b63893721ee7f7a7dadf6b013"
			    ]
			}

	"""
	try:
		body = request.get_json()
		sport_id = body['sport_id']
		name = body['name']
		return jsonify(mint.updateSport(sport_id, name))
	except Exception as e:
		return make_response(jsonify(error=str(e)), 500)

@app.route("/eventGroups", methods=['POST'])
def createEventGroup():
	"""
	**POST** ``/eventGroups``

	* body:
	.. code-block:: json

		{
			"name": [["en", "Michael Group"], ["de", "Michael Group"]],
			"sport_id": "1.16.9"
		}

	* returns:
	  	+ 200:
	  	.. code-block:: json
			{
			    "expiration": "2018-08-14T02:39:53",
			    "extensions": [],
			    "operations": [
			        [
			            22,
			            {
			                "expiration_time": "2018-08-15T02:39:23",
			                "extensions": [],
			                "fee": {
			                    "amount": 2000000,
			                    "asset_id": "1.3.0"
			                },
			                "fee_paying_account": "1.2.7",
			                "proposed_ops": [
			                    {
			                        "op": [
			                            54,
			                            {
			                                "extensions": [],
			                                "fee": {
			                                    "amount": 0,
			                                    "asset_id": "1.3.0"
			                                },
			                                "name": [
			                                    [
			                                        "de",
			                                        "Michael Group"
			                                    ],
			                                    [
			                                        "en",
			                                        "Michael Group"
			                                    ]
			                                ],
			                                "sport_id": "1.16.9"
			                            }
			                        ]
			                    }
			                ]
			            }
			        ]
			    ],
			    "ref_block_num": 23750,
			    "ref_block_prefix": 3528624841,
			    "signatures": [
			        "1f428671ece4d4966987c7ec2ec9b6f4702c07ab2a728e25a54ab06b933d6438021af30a07d88f23a579abc6957ffc13466db9916889fbbfb81b2a51a31763bdde"
			    ]
			} 
	"""
	try:
		body = request.get_json()
		name = body['name']
		sport_id = body['sport_id']
		return jsonify(mint.createEventGroup(name, sport_id))
	except Exception as e:
		return make_response(jsonify(error=str(e)), 500)

@app.route("/eventGroups", methods=['PUT'])
def updateEventGroup():
	"""
	**PUT** ``/eventGroups``

	* body:
	.. code-block:: json

		{
			"name": [["en", "Michael Group"], ["de", "Michael Group"]],
			"sport_id": "1.16.4",
			"event_group_id": "1.17.17"
		}

	* returns:
	  	+ 200:
	  	.. code-block:: json

			{
			    "expiration": "2018-08-14T03:55:25",
			    "extensions": [],
			    "operations": [
			        [
			            22,
			            {
			                "expiration_time": "2018-08-15T03:54:54",
			                "extensions": [],
			                "fee": {
			                    "amount": 2000000,
			                    "asset_id": "1.3.0"
			                },
			                "fee_paying_account": "1.2.7",
			                "proposed_ops": [
			                    {
			                        "op": [
			                            55,
			                            {
			                                "event_group_id": "1.17.17",
			                                "extensions": [],
			                                "fee": {
			                                    "amount": 0,
			                                    "asset_id": "1.3.0"
			                                },
			                                "new_name": [
			                                    [
			                                        "de",
			                                        "Michael Groupe"
			                                    ],
			                                    [
			                                        "en",
			                                        "Michael Group"
			                                    ]
			                                ],
			                                "new_sport_id": "1.16.4"
			                            }
			                        ]
			                    }
			                ]
			            }
			        ]
			    ],
			    "ref_block_num": 25216,
			    "ref_block_prefix": 920330615,
			    "signatures": [
			        "2059282a31f9670b250e2e3fa26782758992c92ea835a5c6d2c904836c791a2e5052ec6f1d2166f6bdefb97bfee6a7f438db8dc0caaec1e403bf263ccaabd934a6"
			    ]
			}

	"""
	try:
		body = request.get_json()
		event_group_id = body['event_group_id']
		name = body['name']
		sport_id = body['sport_id']
		return jsonify(mint.updateEventGroup(event_group_id, name, sport_id))
	except Exception as e:
		return make_response(jsonify(error=str(e)), 500)

@app.route("/events", methods=['POST'])
def createEvent():
	"""
	**POST** ``/events``

	* body:
	.. code-block:: json

		{
			"name": [["en", "Michael Event"], ["de", "Michael Evante"]],
			"season": [["en", "2018"], ["de", "2018"]],
			"start_time": "2018-08-17T21:08:47",
			"event_group_id": "1.17.17"
		}


	* returns:
	  	+ 200:
	  	.. code-block:: json

			{
			    "expiration": "2018-08-14T04:15:41",
			    "extensions": [],
			    "operations": [
			        [
			            22,
			            {
			                "expiration_time": "2018-08-15T04:15:11",
			                "extensions": [],
			                "fee": {
			                    "amount": 2000000,
			                    "asset_id": "1.3.0"
			                },
			                "fee_paying_account": "1.2.7",
			                "proposed_ops": [
			                    {
			                        "op": [
			                            56,
			                            {
			                                "event_group_id": "1.17.17",
			                                "extensions": [],
			                                "fee": {
			                                    "amount": 0,
			                                    "asset_id": "1.3.0"
			                                },
			                                "name": [
			                                    [
			                                        "de",
			                                        "Michael Evante"
			                                    ],
			                                    [
			                                        "en",
			                                        "Michael Event"
			                                    ]
			                                ],
			                                "season": [
			                                    [
			                                        "de",
			                                        "2018"
			                                    ],
			                                    [
			                                        "en",
			                                        "2018"
			                                    ]
			                                ],
			                                "start_time": "2018-08-17T21:08:47"
			                            }
			                        ]
			                    }
			                ]
			            }
			        ]
			    ],
			    "ref_block_num": 25609,
			    "ref_block_prefix": 2528423905,
			    "signatures": [
			        "201227d4498aaac9e27fb43c2df83f455aee4f4c774f178574d4907874f6d3222b4eefe7a6aae14c2e7aa683223e6b6ad3a7d0b634d304820c40f94df4a50df509"
			    ]
			}

	"""
	try:
		body = request.get_json()
		name = body['name']
		season = body['season']
		start_time = body['start_time']
		start_time_format = datetime.strptime(start_time,'%Y-%m-%dT%H:%M:%S')
		event_group_id = body['event_group_id']
		return jsonify(mint.createEvent(name, season, start_time_format, event_group_id))
	except Exception as e:
		return make_response(jsonify(error=str(e)), 500)

@app.route("/events", methods=['PUT'])
def updateEvent():
	"""
	**PUT** ``/events``

	* body:
	.. code-block:: json

		{
			"name": [["en", "Michael Event"], ["de", "Michael Evante"]],
			"season": [["en", "2018"], ["de", "2018"]],
			"start_time": "2018-08-18T21:08:47",
			"event_group_id": "1.17.13",
			"event_id": "1.18.59",
			"status": "frozen"
		}



	* returns:
	  	+ 200:
	  	.. code-block:: json

			{
			    "expiration": "2018-08-14T04:30:25",
			    "extensions": [],
			    "operations": [
			        [
			            22,
			            {
			                "expiration_time": "2018-08-15T04:29:55",
			                "extensions": [],
			                "fee": {
			                    "amount": 2000000,
			                    "asset_id": "1.3.0"
			                },
			                "fee_paying_account": "1.2.7",
			                "proposed_ops": [
			                    {
			                        "op": [
			                            57,
			                            {
			                                "event_id": "1.18.59",
			                                "extensions": [],
			                                "fee": {
			                                    "amount": 0,
			                                    "asset_id": "1.3.0"
			                                },
			                                "new_event_group_id": "1.17.13",
			                                "new_name": [
			                                    [
			                                        "de",
			                                        "Michael Evante"
			                                    ],
			                                    [
			                                        "en",
			                                        "Michael Event"
			                                    ]
			                                ],
			                                "new_season": [
			                                    [
			                                        "de",
			                                        "2018"
			                                    ],
			                                    [
			                                        "en",
			                                        "2018"
			                                    ]
			                                ],
			                                "new_start_time": "2018-08-18T21:08:47",
			                                "new_status": "frozen"
			                            }
			                        ]
			                    }
			                ]
			            }
			        ]
			    ],
			    "ref_block_num": 25895,
			    "ref_block_prefix": 2859863074,
			    "signatures": [
			        "207d9e5a8ff3f9d79eded681f3737779de689560283020fb06ee22a6cd263bd06f4cc1aa47adc5361c413f2872fcd6d0aa982b7b3eeba1ddc601f0c594acd2a405"
			    ]
			}

	"""
	try:
		body = request.get_json()
		event_id = body['event_id']
		name = body['name']
		season = body['season']
		start_time = body['start_time']
		start_time_format = datetime.strptime(start_time,'%Y-%m-%dT%H:%M:%S')
		event_group_id = body['event_group_id']
		status = body['status']
		return jsonify(mint.updateEvent(event_id, name, season, start_time_format, event_group_id, status))
	except Exception as e:
		return make_response(jsonify(error=str(e)), 500)

@app.route("/events/status", methods=['PUT'])
def updateEventStatus():
	"""
	**PUT** ``/events/status``

	* body:
	.. code-block:: json

		{
			"scores": [["en", "1-0"], ["de", "1-0"]],
			"event_id": "1.18.59",
			"status": "frozen"
		}



	* returns:
	  	+ 200:
	  	.. code-block:: json

			{
			    "expiration": "2018-08-14T04:28:32",
			    "extensions": [],
			    "operations": [
			        [
			            22,
			            {
			                "expiration_time": "2018-08-15T04:28:02",
			                "extensions": [],
			                "fee": {
			                    "amount": 2000000,
			                    "asset_id": "1.3.0"
			                },
			                "fee_paying_account": "1.2.7",
			                "proposed_ops": [
			                    {
			                        "op": [
			                            72,
			                            {
			                                "event_id": "1.18.59",
			                                "extensions": [],
			                                "fee": {
			                                    "amount": 0,
			                                    "asset_id": "1.3.0"
			                                },
			                                "scores": [],
			                                "status": "frozen"
			                            }
			                        ]
			                    }
			                ]
			            }
			        ]
			    ],
			    "ref_block_num": 25857,
			    "ref_block_prefix": 1565774390,
			    "signatures": [
			        "1f5fff23560217af19025c4092ee74175608adb8991f06187f3a0df2d4fc8e0ded00a7af2c26504711d91ca2b8d23010dea19247bd1d54dc31c5af9d63bccb9bdd"
			    ]
			}

	"""
	try:
		body = request.get_json()
		event_id = body['event_id']
		status = body['status']
		scores = body['scores']
		return jsonify(mint.updateEventStatus(event_id, status, scores))
	except Exception as e:
		return make_response(jsonify(error=str(e)), 500)

@app.route("/bettingMarketGroups", methods=['POST'])
def createBettingMarketGroup():
	"""
	**POST** ``/bettingMarketGroups``

	* body:
	.. code-block:: json

		{
			"description": [["en","Moneyline"],["de", "Moneeline"]],
			"event_id": "1.18.404",
			"betting_market_rule_id": "1.19.0",
			"asset": "1.3.1"
		}




	* returns:
	  	+ 200:
	  	.. code-block:: json

			{
			    "expiration": "2018-08-14T05:10:40",
			    "extensions": [],
			    "operations": [
			        [
			            22,
			            {
			                "expiration_time": "2018-08-15T05:10:10",
			                "extensions": [],
			                "fee": {
			                    "amount": 2000000,
			                    "asset_id": "1.3.0"
			                },
			                "fee_paying_account": "1.2.7",
			                "proposed_ops": [
			                    {
			                        "op": [
			                            60,
			                            {
			                                "asset_id": "1.3.1",
			                                "delay_before_settling": 0,
			                                "description": [
			                                    [
			                                        "de",
			                                        "Moneeline"
			                                    ],
			                                    [
			                                        "en",
			                                        "Moneyline"
			                                    ]
			                                ],
			                                "event_id": "1.18.404",
			                                "extensions": [],
			                                "fee": {
			                                    "amount": 0,
			                                    "asset_id": "1.3.0"
			                                },
			                                "never_in_play": false,
			                                "rules_id": "1.19.0"
			                            }
			                        ]
			                    }
			                ]
			            }
			        ]
			    ],
			    "ref_block_num": 26676,
			    "ref_block_prefix": 954659182,
			    "signatures": [
			        "2065e0341ff57d96b3ec2e4df6ed461b46dea6e0f295556302d526f2561cfd73a72b47963658fe7dbb7a2db71c4d48e53ec1e0aaa0cd2cbd3789e76b9ba007719d"
			    ]
			}

	"""
	try:
		body = request.get_json()
		description = body['description']
		event_id = body['event_id']
		betting_market_rule_id = body['betting_market_rule_id']
		asset = body['asset']
		return jsonify(mint.createBettingMarketGroup(description, event_id, betting_market_rule_id, asset))
	except Exception as e:
		return make_response(jsonify(error=str(e)), 500)

@app.route("/bettingMarketGroups", methods=['PUT'])
def updateBettingMarketGroup():
	"""
	**PUT** ``/bettingMarketGroups``

	* body:
	.. code-block:: json

		{
			"description": [["en","Moneyline"],["de", "Monexline"]],
			"event_id": "1.18.59",
			"betting_market_group_id": "1.20.418",
			"betting_market_rule_id": "1.19.8",
			"status": "upcoming"
		}

	* returns:
	  	+ 200:
	  	.. code-block:: json

			{
			    "expiration": "2018-08-14T05:11:30",
			    "extensions": [],
			    "operations": [
			        [
			            22,
			            {
			                "expiration_time": "2018-08-15T05:11:00",
			                "extensions": [],
			                "fee": {
			                    "amount": 2000000,
			                    "asset_id": "1.3.0"
			                },
			                "fee_paying_account": "1.2.7",
			                "proposed_ops": [
			                    {
			                        "op": [
			                            70,
			                            {
			                                "betting_market_group_id": "1.20.418",
			                                "extensions": [],
			                                "fee": {
			                                    "amount": 0,
			                                    "asset_id": "1.3.0"
			                                },
			                                "new_description": [
			                                    [
			                                        "de",
			                                        "Monexline"
			                                    ],
			                                    [
			                                        "en",
			                                        "Moneyline"
			                                    ]
			                                ],
			                                "new_rules_id": "1.19.8",
			                                "status": "upcoming"
			                            }
			                        ]
			                    }
			                ]
			            }
			        ]
			    ],
			    "ref_block_num": 26693,
			    "ref_block_prefix": 1054910509,
			    "signatures": [
			        "206b94d167a14bb7972d1084061fd5a9ff882643f28bf9e4d7febc7efbdf0ff32b5811a95fe54d49e06aaaf968d5b415bed9bfde4c1f3f0d6772171420c7725795"
			    ]
			}

	"""
	try:
		body = request.get_json()
		bmg_id = body['betting_market_group_id']
		description = body['description']
		event_id = body['event_id']
		betting_market_rule_id = body['betting_market_rule_id']
		status = body['status']
		return jsonify(mint.updateBettingMarketGroup(bmg_id, description, event_id, betting_market_rule_id, status))
	except Exception as e:
		return make_response(jsonify(error=str(e)), 500)

@app.route("/bettingMarketGroups/rules", methods=['PUT'])
def updateBettingMarketGroupRule():
	"""
	**PUT** ``/bettingMarketGroups/rules``

	* body:
	.. code-block:: json

		{
			"description": [["en","Big rule"],["de", "Bige Rule"]],
			"betting_market_rule_id": "1.19.8",
			"name": [["en", "MLB_2018"], ["de", "LMB_2018"]]
		}


	* returns:
	  	+ 200:
	  	.. code-block:: json

			{
			    "expiration": "2018-08-14T04:56:54",
			    "extensions": [],
			    "operations": [
			        [
			            22,
			            {
			                "expiration_time": "2018-08-15T04:56:24",
			                "extensions": [],
			                "fee": {
			                    "amount": 2000000,
			                    "asset_id": "1.3.0"
			                },
			                "fee_paying_account": "1.2.7",
			                "proposed_ops": [
			                    {
			                        "op": [
			                            59,
			                            {
			                                "betting_market_rules_id": "1.19.8",
			                                "extensions": [],
			                                "fee": {
			                                    "amount": 0,
			                                    "asset_id": "1.3.0"
			                                },
			                                "new_description": [
			                                    [
			                                        "de",
			                                        "Bige Rule"
			                                    ],
			                                    [
			                                        "en",
			                                        "Big rule"
			                                    ]
			                                ],
			                                "new_name": [
			                                    [
			                                        "de",
			                                        "LMB_2018"
			                                    ],
			                                    [
			                                        "en",
			                                        "MLB_2018"
			                                    ]
			                                ]
			                            }
			                        ]
			                    }
			                ]
			            }
			        ]
			    ],
			    "ref_block_num": 26410,
			    "ref_block_prefix": 419842553,
			    "signatures": [
			        "2065c3b58af4444302baed030d16e8dc0ad0146301cc39b6bc132295adf5c606b53ec950628fc91ff524344a315d9af7a29e3ce03176e1eb929a7f8e087b503a74"
			    ]
			}

	"""
	try:
		body = request.get_json()
		bmgr_id = body['betting_market_rule_id']
		name = body['name']
		description = body['description']
		return jsonify(mint.updateBettingMarketGroupRule(bmgr_id, name, description))
	except Exception as e:
		return make_response(jsonify(error=str(e)), 500)

@app.route("/bettingMarkets", methods=['POST'])
def createBettingMarket():
	"""
	**POST** ``/bettingMarkets``

	* body:
	.. code-block:: json

		{
			"payout_condition": [["en","Team must satisfy bmg rules"],["de", "German stuff"]],
			"betting_market_group_id": "1.20.417",
			"description": [["en", "New York Yankees"], ["de", "New Yirk Yonkees"]]
		}




	* returns:
	  	+ 200:
	  	.. code-block:: json

			{
			    "expiration": "2018-08-14T05:01:16",
			    "extensions": [],
			    "operations": [
			        [
			            22,
			            {
			                "expiration_time": "2018-08-15T05:00:46",
			                "extensions": [],
			                "fee": {
			                    "amount": 2000001,
			                    "asset_id": "1.3.0"
			                },
			                "fee_paying_account": "1.2.7",
			                "proposed_ops": [
			                    {
			                        "op": [
			                            61,
			                            {
			                                "description": [
			                                    [
			                                        "de",
			                                        "New Yirk Yonkees"
			                                    ],
			                                    [
			                                        "en",
			                                        "New York Yankees"
			                                    ]
			                                ],
			                                "extensions": [],
			                                "fee": {
			                                    "amount": 0,
			                                    "asset_id": "1.3.0"
			                                },
			                                "group_id": "1.20.417",
			                                "payout_condition": [
			                                    [
			                                        "de",
			                                        "German stuff"
			                                    ],
			                                    [
			                                        "en",
			                                        "Team must satisfy bmg rules"
			                                    ]
			                                ]
			                            }
			                        ]
			                    }
			                ]
			            }
			        ]
			    ],
			    "ref_block_num": 26494,
			    "ref_block_prefix": 750610868,
			    "signatures": [
			        "2021226fc1fd7fdc73ce87edabf6cd41576722b968070f28b6c9282ba8dadffd3a422c383d6fa64fc2e6fe6c7582fec7773167173f1828c84a9a039d00fbedc732"
			    ]
			}

	"""
	try:
		body = request.get_json()
		payout_condition = body['payout_condition']
		description = body['description']
		betting_market_group_id = body['betting_market_group_id']
		return jsonify(mint.createBettingMarket(payout_condition, description, betting_market_group_id))
	except Exception as e:
		return make_response(jsonify(error=str(e)), 500)

@app.route("/bettingMarkets", methods=['PUT'])
def updateBettingMarket():
	"""
	**PUT** ``/bettingMarkets``

	* body:
	.. code-block:: json

		{
			"payout_condition": [["en","Team must satisfy bmg rules"],["de", "German stuff"]],
			"betting_market_group_id": "1.20.417",
			"description": [["en", "New York Yankees"], ["de", "New Yirk Yonkees"]],
			"betting_market_id": "1.21.883"
		}





	* returns:
	  	+ 200:
	  	.. code-block:: json

			{
			    "expiration": "2018-08-14T05:03:34",
			    "extensions": [],
			    "operations": [
			        [
			            22,
			            {
			                "expiration_time": "2018-08-15T05:03:04",
			                "extensions": [],
			                "fee": {
			                    "amount": 2000001,
			                    "asset_id": "1.3.0"
			                },
			                "fee_paying_account": "1.2.7",
			                "proposed_ops": [
			                    {
			                        "op": [
			                            71,
			                            {
			                                "betting_market_id": "1.21.883",
			                                "extensions": [],
			                                "fee": {
			                                    "amount": 0,
			                                    "asset_id": "1.3.0"
			                                },
			                                "new_description": [
			                                    [
			                                        "de",
			                                        "New Yirk Yonkees"
			                                    ],
			                                    [
			                                        "en",
			                                        "New York Yankees"
			                                    ]
			                                ],
			                                "new_group_id": "1.20.417",
			                                "new_payout_condition": [
			                                    [
			                                        "de",
			                                        "German stuff"
			                                    ],
			                                    [
			                                        "en",
			                                        "Team must satisfy bmg rules"
			                                    ]
			                                ]
			                            }
			                        ]
			                    }
			                ]
			            }
			        ]
			    ],
			    "ref_block_num": 26537,
			    "ref_block_prefix": 1019350048,
			    "signatures": [
			        "1f362fb8f03fcca714c6b060cc554d6c31d0224540cfa651211858f32f9353079c24e4b270fbbd9d8697d4c10eede81becab06cc35639358d92e5ab05a5b476219"
			    ]
			}
	"""
	try:
		body = request.get_json()
		betting_market_id = body['betting_market_id']
		payout_condition = body['payout_condition']
		description = body['description']
		betting_market_group_id = body['betting_market_group_id']
		return jsonify(mint.updateBettingMarket(betting_market_id, payout_condition, description, betting_market_group_id))
	except Exception as e:
		return make_response(jsonify(error=str(e)), 500)

@app.route("/bettingMarkets/<betting_market_id>/resolve", methods=['PUT'])
def resolveBettingMarkets(betting_market_id):
	"""
	**PUT** ``/bettingMarkets``

	* body:
	.. code-block:: json

		{
			"result_list": [["1.21.833","win"],["1.21.822", "not_win"]],
			"betting_market_group_id": "1.20.417"
		}





	* returns:
	  	+ 200:
	  	.. code-block:: json

			{
			    "expiration": "2018-08-14T05:07:07",
			    "extensions": [],
			    "operations": [
			        [
			            22,
			            {
			                "expiration_time": "2018-08-15T05:06:37",
			                "extensions": [],
			                "fee": {
			                    "amount": 2000000,
			                    "asset_id": "1.3.0"
			                },
			                "fee_paying_account": "1.2.7",
			                "proposed_ops": [
			                    {
			                        "op": [
			                            63,
			                            {
			                                "betting_market_group_id": "1.20.417",
			                                "extensions": [],
			                                "fee": {
			                                    "amount": 0,
			                                    "asset_id": "1.3.0"
			                                },
			                                "resolutions": [
			                                    [
			                                        "1.21.822",
			                                        "not_win"
			                                    ],
			                                    [
			                                        "1.21.833",
			                                        "win"
			                                    ]
			                                ]
			                            }
			                        ]
			                    }
			                ]
			            }
			        ]
			    ],
			    "ref_block_num": 26608,
			    "ref_block_prefix": 3916725088,
			    "signatures": [
			        "207a7bfe7b16341167b639f153b7f0c0b7bab8be8c4b3602d3b002a2fd1794903b4a0723c71c7c729782020bcab78546883a37edbb251b65aeb8cfc2f863f293f9"
			    ]
			}
	"""
	try:
		body = request.get_json()
		result_list = body['result_list']
		betting_market_group_id = body['betting_market_group_id']
		return jsonify(mint.resolveBettingMarketGroup(betting_market_group_id, result_list))
	except Exception as e:
		return make_response(jsonify(error=str(e)), 500)

@app.route("/proposals", methods=['GET'])
def getProposals():
	"""
	**GET** ``/proposals``

	* query-params:
		+ account:
			- type: string
			- description: account name or id

	* returns:
		+ 200:
		.. code-block: json
			[
			    {
			        "available_active_approvals": [],
			        "available_key_approvals": [],
			        "available_owner_approvals": [],
			        "expiration_time": "2018-08-15T02:39:23",
			        "id": "1.10.2020",
			        "proposed_transaction": {
			            "expiration": "2018-08-15T02:39:23",
			            "extensions": [],
			            "operations": [
			                [
			                    54,
			                    {
			                        "extensions": [],
			                        "fee": {
			                            "amount": 0,
			                            "asset_id": "1.3.0"
			                        },
			                        "name": [
			                            [
			                                "[",
			                                "'"
			                            ]
			                        ],
			                        "sport_id": "1.16.9"
			                    }
			                ]
			            ],
			            "ref_block_num": 0,
			            "ref_block_prefix": 0
			        },
			        "proposer": "1.2.7",
			        "required_active_approvals": [
			            "1.2.1"
			        ],
			        "required_owner_approvals": []
			    },
			    {
			        "available_active_approvals": [
			            "1.2.7"
			        ],
			        "available_key_approvals": [],
			        "available_owner_approvals": [],
			        "expiration_time": "2018-08-14T03:42:00",
			        "id": "1.10.2022",
			        "proposed_transaction": {
			            "expiration": "2018-08-14T03:42:00",
			            "extensions": [],
			            "operations": [
			                [
			                    63,
			                    {
			                        "betting_market_group_id": "1.20.2109",
			                        "extensions": [],
			                        "fee": {
			                            "amount": 0,
			                            "asset_id": "1.3.0"
			                        },
			                        "resolutions": [
			                            [
			                                "1.21.4374",
			                                "not_win"
			                            ],
			                            [
			                                "1.21.4375",
			                                "win"
			                            ]
			                        ]
			                    }
			                ],
			                [
			                    63,
			                    {
			                        "betting_market_group_id": "1.20.2161",
			                        "extensions": [],
			                        "fee": {
			                            "amount": 0,
			                            "asset_id": "1.3.0"
			                        },
			                        "resolutions": [
			                            [
			                                "1.21.4484",
			                                "not_win"
			                            ],
			                            [
			                                "1.21.4485",
			                                "win"
			                            ]
			                        ]
			                    }
			                ]
			            ],
			            "ref_block_num": 0,
			            "ref_block_prefix": 0
			        },
			        "proposer": "1.2.7",
			        "required_active_approvals": [
			            "1.2.1"
			        ],
			        "required_owner_approvals": []
			    }
			]
	"""
	try:
		account = request.args.get("account")
		return jsonify(mint.getProposals(account))
	except Exception as e:
		return make_response(jsonify(error=str(e)), 500)

@app.route("/proposals/<proposal_id>", methods=['PUT'])
def approveProposal(proposal_id):
	"""
	**PUT** ``/proposals/<proposal_id>

	* path-params:
		+ proposal_id:
			- type: string
			- description: proposal id

	* query-params:
		+ approve:
			- type: Boolean
			- description: approve or disapprove proposal
		+ account:
			- type: string
			- description: account name or id

	* returns:
		+ 200:
		.. code-block: json
			{
			    "expiration": "2018-08-14T03:02:53",
			    "extensions": [],
			    "operations": [
			        [
			            23,
			            {
			                "active_approvals_to_add": [],
			                "active_approvals_to_remove": [
			                    "1.2.7"
			                ],
			                "extensions": [],
			                "fee": {
			                    "amount": 2000000,
			                    "asset_id": "1.3.0"
			                },
			                "fee_paying_account": "1.2.7",
			                "key_approvals_to_add": [],
			                "key_approvals_to_remove": [],
			                "owner_approvals_to_add": [],
			                "owner_approvals_to_remove": [],
			                "proposal": "1.10.2020"
			            }
			        ]
			    ],
			    "ref_block_num": 24195,
			    "ref_block_prefix": 1095264235,
			    "signatures": [
			        "1f62b9e802ebbe616d4fabbf43f2f54a1ee772eda52c924cd41d2b15e87d82cae922304b54f7662d628cf47852119082202592f4810468d9938cd80b1c7eca02a6"
			    ]
			}
	"""
	try:
		approve = request.args.get("approve")
		account = request.args.get("account")
		if approve is None:
			return make_response(jsonify(error="Specify approve in query params"), 500)
		return jsonify(mint.approveProposal(proposal_id, approve))
	except Exception as e:
		return make_response(jsonify(error=str(e)), 500)

# Other Calls

@app.route("/bettors/<bettor_id>/history", methods=['GET'])
def getHistory(bettor_id):
	"""
	**GET** ``/bettors/<bettor_id>/history``

	* path-params:
		+ bettor_id:
			- type: string
			- description: account name or id

	* returns:
		+ 200:
		.. code-block:: json

			[
			    {
			        "block_num": 1046928,
			        "id": "1.11.13588",
			        "op": [
			            64,
			            {
			                "betting_market_group_id": "1.20.1500",
			                "bettor_id": "1.2.104",
			                "fee": {
			                    "amount": 0,
			                    "asset_id": "1.3.0"
			                },
			                "fees_paid": 0,
			                "resolutions": [
			                    [
			                        "1.21.3130",
			                        "win"
			                    ],
			                    [
			                        "1.21.3131",
			                        "not_win"
			                    ]
			                ],
			                "winnings": 1495318
			            }
			        ],
			        "op_in_trx": 1,
			        "result": [
			            0,
			            {}
			        ],
			        "trx_in_block": 1,
			        "virtual_op": 33813
			    }
			]	

	"""
	response = requests.get(market_maker_url + request.full_path)
	return (response.content, response.status_code, response.headers.items())

@app.route("/bettors/<bettor_id>/accountDetails", methods=['GET'])
def getAccountDetails(bettor_id):
	"""
	**GET** ``/bettors/<bettor_id>/accountDetails``

	* path-params:
		+ bettor_id:
			- type: string
			- description: account name or id
	* returns:
		+ 200:
		.. code-block:: json

			{
			    "active": {
			        "account_auths": [],
			        "address_auths": [],
			        "key_auths": [
			            [
			                "PPY6EACxBdQcHFPXij4UY6ZkpcqpQ6GsyzRTUV5o4zYef9AdqPz44",
			                1
			            ]
			        ],
			        "weight_threshold": 1
			    },
			    "active_special_authority": [
			        0,
			        {}
			    ],
			    "assets": [],
			    "balances": [
			        {
			            "asset_type": "1.3.1",
			            "balance": 1092830104,
			            "id": "2.5.114",
			            "owner": "1.2.104"
			        }
			    ],
			    "blacklisted_accounts": [],
			    "blacklisting_accounts": [],
			    "call_orders": [],
			    "id": "1.2.104",
			    "lifetime_referrer": "1.2.19",
			    "lifetime_referrer_fee_percentage": 3000,
			    "lifetime_referrer_name": "bookie-faucet",
			    "limit_orders": [],
			    "membership_expiration_date": "1970-01-01T00:00:00",
			    "name": "bettor1",
			    "network_fee_percentage": 2000,
			    "options": {
			        "extensions": [],
			        "memo_key": "PPY8AAdJSiRLqYWsiXyrAKJ2THh1h69bg73Vw94QbM6Bt7PaT6FNv",
			        "num_committee": 0,
			        "num_witness": 0,
			        "votes": [],
			        "voting_account": "1.2.5"
			    },
			    "owner": {
			        "account_auths": [],
			        "address_auths": [],
			        "key_auths": [
			            [
			                "PPY8TM2Tj5AvEqBCoaXnTCBomExR2EkKcdDtQTPVKAoPGaF3ouiii",
			                1
			            ]
			        ],
			        "weight_threshold": 1
			    },
			    "owner_special_authority": [
			        0,
			        {}
			    ],
			    "pending_dividend_payments": [],
			    "proposals": [],
			    "referrer": "1.2.19",
			    "referrer_name": "bookie-faucet",
			    "referrer_rewards_percentage": 5000,
			    "registrar": "1.2.19",
			    "registrar_name": "bookie-faucet",
			    "settle_orders": [],
			    "statistics": {
			        "id": "2.6.104",
			        "lifetime_fees_paid": 2214476,
			        "most_recent_op": "2.9.15061",
			        "owner": "1.2.104",
			        "pending_fees": 0,
			        "pending_vested_fees": 0,
			        "removed_ops": 0,
			        "total_core_in_orders": 0,
			        "total_ops": 658
			    },
			    "top_n_control_flags": 0,
			    "vesting_balances": [],
			    "votes": [],
			    "whitelisted_accounts": [],
			    "whitelisting_accounts": [],
			    "withdraws": []
			}

	"""
	response = requests.get(market_maker_url + request.full_path)
	return (response.content, response.status_code, response.headers.items())

if __name__ == '__main__':
	with open("config.yaml", 'r') as stream:
		try:
			config = yaml.safe_load(stream)
			market_maker_url = config['market-maker']['url']
		except yaml.YAMLError as exc:
			print(exc)
		app.run(debug=False, host='0.0.0.0', port=5050)
