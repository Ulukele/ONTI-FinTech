#!/usr/bin/env python
from web3 import Web3, HTTPProvider
import json
import sys
from eth_account import Account


def GetAdres(privateKey):
    adress = Account.privateKeyToAccount("0x"+privateKey)
    return adress

def DeployContract(abi, byte, person):
    emptiness = True# yet

def GetGas(URL):
    res = requests.get(url).json()
    return res['fast']


args = (sys.argv)[1:]

with open('KYC_RegistrarByte.txt') as file:
    byteKYC = file.read()
with open('KYC_RegistrarABI.txt') as file:
    abiKYC = file.read()
with open('Payment_HandlerByte.txt') as file:
    bytePayH = file.read()
with open('Payment_HandlerABI.txt') as file:
    abiPayH = file.read()

with open('network.json') as file:
	infor = json.load(file)
    privateKey = infor['privKey']
    RecURL = infor['rpcUrl']
    GasURL = infor['gasPriceUrl']
    defGas = infor['defaultGasPrices']

adres = GetAdres(privateKey)

web3 = Web3(HTTPProvider(RecURL))


if args[0] =='--deploy':
    DeployContract(abiKYC, byteKYC, adres)

print(GetGas(GasURL))
### Put your code below this comment ###
#print("Show must go on")
