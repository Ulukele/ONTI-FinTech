#!/usr/bin/env python
import sys
import json
from eth_account import Account
from web3 import Web3, HTTPProvider
from eth_hash.auto import keccak

def GetPerson():
    try:
        with open('person.json') as file:
            infor = json.load(file)
            return (infor['id'])
    except:
        return None

def HashIt(ident, pin):
    ident = (ident[:8] + ident[9:13] + ident[14:18] + ident[19:23] + ident[24:])

    pin = str(pin)
    pin = [('0'+pin[0]), ('0'+pin[1]), ('0'+pin[2]), ('0'+pin[3])]

    #Calculate privateKey
    data = b''
    for i in range(4):
        data = (keccak(data).hex())[2:]
        data = data + ident + pin[i]
        data = bytes.fromhex(data)
    data = (keccak(data).hex())[2:]
    privateKey = data
    return privateKey

def HashCodeWithPinCodeAndPerson(PINcode):
    personInfo = GetPerson()
    if personInfo == None:
        return None
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
    if balance == 0:
        return (0, "poa")
    return (balance, currency[ind])

def GetAdress(privateKey):
    adress = Account.privateKeyToAccount("0x"+privateKey)
    return adress

def PrintBalance(privateKey):
    adress = GetAdress(privateKey)
    balance = [0, 0]
    balance[0], balance[1] = BalanceAll(web3.eth.getBalance(adress.address))
    if balance[0] == '':
        balance[0] = 0
    print("Your balance is {} {}".format(balance[0], balance[1]))

args = (sys.argv)[1:]
sizeM = len(args)


web3 = Web3(HTTPProvider("https://sokol.poa.network"))

if args[0] == "--balance":
    if sizeM == 2:
        PINcode = args[1]
        Key = HashCodeWithPinCodeAndPerson(PINcode)
        if Key == None:
            print("ID is not found")
        else:
            PrintBalance(Key)
