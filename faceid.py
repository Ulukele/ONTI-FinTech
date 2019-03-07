#!/usr/bin/env python

### Put your code below this comment ###
#print("Show must go on")

from eth_account import Account

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

def IGetAdress(privateKey):
    adress = Account.privateKeyToAccount("0x"+privateKey)
    return adress

def PrintBalance(privateKey):
    adress = IGetAdress(privateKey)
    balance = BalanceAll(web3.eth.getBalance(adress))
    print("Balance on {0} is {1} {2}".format('"'+ adress[2:] +'"', balance[0], balance[1]))

args = (sys.argv)[1:]
sizeM = len(args)

if args[0] == "--balance":
    if sizeM == 2:
        PrintBalance(args[1])
