#!/usr/bin/env python
import sys
import json
from eth_account import Account
from web3 import Web3, HTTPProvider
from eth_account import Account

def GetPerson():
    with open('person.json') as file:
        infor = json.load(file)
        return (infor['id'])

def HashIt(ident, pin):
    ident = (ident[:8] + ident[9:13] + ident[14:18] + ident[19:23] + ident[24:])

    pin = str(pin)
    pin = [('0'+pin[0]), ('0'+pin[1]), ('0'+pin[2]), ('0'+pin[3])]

    #Calculate privateKey
    data = b''
    for i in range(4):
        data = (web3.sha3(data).hex())[2:]
        data = data + ident + pin[i]
        data = bytes.fromhex(data)
    data = (web3.sha3(data).hex())[2:]
    privateKey = data
    return privateKey

def HashCodeWithPinCodeAndPerson(PINcode):
    personInfo = GetPerson()
    key = HashIt(personInfo, PINcode)
    return key

def BalanceAll(balance):
    currency = ["wei", "kwei", "mwei", "gwei", "szabo", "finney", "poa"]
    ind = 0
    while (balance > 10):
        balance /= 1000
        ind += 1
    if balance < 1:
        balance *= 1000
        ind -= 1
    balance = str(round(balance, 6))
    if balance[-1] == '0':
        balance = balance[:-2]
    return (balance, currency[ind])

def GetAdress(privateKey):
    adress = Account.privateKeyToAccount("0x"+privateKey)
    return adress

def PrintBalance(privateKey):
    adress = GetAdress(privateKey)
    balance = BalanceAll(web3.eth.getBalance(adress.address))
    print("Your balance is {} {}".format(balance[0], balance[1]))

args = (sys.argv)[1:]
sizeM = len(args)

with open('network.json') as file:
    infor = json.load(file)
    privateKey = infor["privKey"]
    RecURL = infor["rpcUrl"]
    GasURL = infor["gasPriceUrl"]
    defGas = infor["defaultGasPrice"]

web3 = Web3(HTTPProvider(RecURL))

if args[0] == "--balance":
    if sizeM == 2:
        PINcode = args[1]
        Key = HashCodeWithPinCodeAndPerson(PINcode)
        PrintBalance(Key)
