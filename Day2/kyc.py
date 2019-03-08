from web3 import Web3, HTTPProvider
import json
import sys
import requests
from eth_account import Account

def AcceptAddNumberRequest(TXaddress):
    TX = web3.eth.getTransaction(TXaddress)
    return TX


args = (sys.argv)[1:]
sizeM = len(args)

if args[0] == "--confirm":
    AcceptAddNumberRequest()
