from flask import make_response
from flask import jsonify
from bos_mint.node import Node

# MINT calls
# TODO add account param for bookie object creation/update proposals

def createSport(name):
	Node().createSport(name)
	return Node().broadcastPendingTransaction()

def updateSport(sportId, name):
	Node().updateSport(sportId, name)
	return Node().broadcastPendingTransaction()

def createEventGroup(name, sportId):
	Node().createEventGroup(name, sportId)
	return Node().broadcastPendingTransaction()

def updateEventGroup(eventGroupId, name, sportId):
	Node().updateEventGroup(eventGroupId, name, sportId)
	return Node().broadcastPendingTransaction()

def createEvent(name, season, startTime, eventGroupId):
	Node().createEvent(name, season, startTime, eventGroupId)
	return Node().broadcastPendingTransaction()

def updateEvent(eventId, name, season, startTime, eventGroupId, status):
	Node().updateEvent(eventId, name, season, startTime, eventGroupId, status)
	return Node().broadcastPendingTransaction()

def updateEventStatus(eventId, status, scores=[]):
	Node().updateEventStatus(eventId, status, scores=[])
	return Node().broadcastPendingTransaction()

def createBettingMarketGroup(description, eventId, bettingMarketRuleId, asset):
	Node().createBettingMarketGroup(description, eventId, bettingMarketRuleId, asset)
	return Node().broadcastPendingTransaction()

def updateBettingMarketGroup(bmgId, description, eventId, rulesId, status):
	Node().updateBettingMarketGroup(bmgId, description, eventId, rulesId, status)
	return Node().broadcastPendingTransaction()

def updateBettingMarketGroupRule(bmgrId, name, description):
	Node().updateBettingMarketGroupRule(bmgrId, name, description)
	return Node().broadcastPendingTransaction()

def createBettingMarket(payoutCondition, description, bettingMarketGroupId):
	Node().createBettingMarket(payoutCondition, description, bettingMarketGroupId)
	return Node().broadcastPendingTransaction()

def updateBettingMarket(bmId, payout_condition, description, bmgId):
	Node().updateBettingMarket(bmId, payout_condition, description, bmgId)
	return Node().broadcastPendingTransaction()

def resolveBettingMarketGroup(bettingMarketGroupId, resultList):
	Node().resolveBettingMarketGroup(bettingMarketGroupId, resultList)
	return Node().broadcastPendingTransaction()

def getProposals(account=None):
	if account is None:
		return Node().getAllProposals()
	else:
		return Node().getAllProposals(accountName=account)

def approveProposal(proposal_id, approve):
	if approve is True:
		return Node().acceptProposal(proposal_id)
	else:
		return Node().rejectProposal(proposal_id)
