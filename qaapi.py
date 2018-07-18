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

# @app.route("/bettors/<bettor_id>/matchedBets", methods=['GET'])
# def getMatchedBets(bettor_id):
# 	response = requests.get(market_maker_url + request.full_path)
# 	return (response.content, response.status_code, response.headers.items())

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