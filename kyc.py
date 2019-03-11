#!/usr/bin/env python
import sys
import json
from eth_account import Account
from web3 import Web3, HTTPProvider
import sha3
import requests

def GetAdress(privateKey):
    adress = Account.privateKeyToAccount("0x"+privateKey)
    return adress

def GetGas(URL, defGas):
    try:
        response = requests.get(URL).text
        gasinfo = json.loads(response)['fast']
    except:
        return defGas
    return int(gasinfo * 1000000000)

def GetContractInfo():
    try:
        with open('registrar.json') as file:
            infor = json.load(file)
            Caddress = infor['registrar']['address']
    except:
        Caddress = None
    with open('KYC_RegistrarByte.txt') as file:
        byteKYC = str(file.read())
        if byteKYC[-1] == '\n':
            byteKYC = byteKYC[:-1]
    with open('KYC_RegistrarABI.txt') as file:
        abiKYC = file.read()
        abiKYC = json.loads(abiKYC)
    return (Caddress, abiKYC, byteKYC)

def ApproveRequest(person, addres, URL, defGas):
    (Caddress, abiKYC, byteKYC) = GetContractInfo()

    if Caddress == None:
        return {'status': -2}
    try:
        contract_by_address =  web3.eth.contract(address = Caddress, abi = abiKYC)
    except:
        return {'status': -3}


    statusA = contract_by_address.functions.GetPersonInfoAR(addres).call()
    statusD = contract_by_address.functions.GetPersonInfoDR(addres).call()
    """
    if(not (statusA or statusD)):
        return {'status': -1}
    """
    tx_wo_sign = contract_by_address.functions.Confirm(addres).buildTransaction({
        'from': person.address,
        'nonce': web3.eth.getTransactionCount(person.address),
        'gas': 8000000,
        'gasPrice': GetGas(GasURL, defGas)
    })

    signed_tx = person.signTransaction(tx_wo_sign)
    txId = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    TX = web3.eth.waitForTransactionReceipt(txId)
    return TX

def AddresByNumber(PhoneNum):
    (Caddress, abiKYC, byteKYC) = GetContractInfo()
    if Caddress == None:
        return {'status': -2}
    try:
        contract_by_address =  web3.eth.contract(address = Caddress, abi = abiKYC)
    except:
        return {'status': -3}

    TX = {'status': 1, 'result': ''}
    TX['result'] = contract_by_address.functions.GetAddress(PhoneNum).call()
    if TX['result'] == '0x0000000000000000000000000000000000000000':
        TX['status'] = -1
    return TX

def GetListAdds():
    (Caddress, abiKYC, byteKYC) = GetContractInfo()

    if Caddress == None:
        return {'status': -2}
    try:
        contract_by_address =  web3.eth.contract(address = Caddress, abi = abiKYC)
    except:
        return {'status': -3}
    adds = contract_by_address.events.RegistrationRequest().createFilter(fromBlock='latest').get_new_entries()

    return adds

args = (sys.argv)[1:]
sizeM = len(args)

with open('network.json') as file:
    infor = json.load(file)
    privateKey = infor["privKey"]
    RecURL = infor["rpcUrl"]
    GasURL = infor["gasPriceUrl"]
    defGas = infor["defaultGasPrice"]

web3 = Web3(HTTPProvider(RecURL))
person = GetAdress(privateKey)

if args[0] == '--confirm':
    addres = args[1]
    TX = ApproveRequest(person, addres, GasURL, defGas)

    if TX['status'] == -3:
        print("Seems that the contract address is not the registrar contract")
    if TX['status'] == -2:
        print("No contract address")
    if TX['status'] == 0:
        print("Failed but included in", TX['transactionHash'].hex())
    if TX['status'] == 1:
        print("Confirmed by", TX['transactionHash'].hex())

if args[0] == '--get':
    PhoneNum = args[1]
    TX = AddresByNumber(PhoneNum)

    if TX['status'] == -3:
        print("Seems that the contract address is not the registrar contract")
    if TX['status'] == -2:
        print("No contract address")
    if TX['status'] == -1:
        print("Correspondence not found")
    if TX['status'] == 1:
        print("Registered correspondence:", TX['result'])

if args[0] == '--list':
    if args[1] == 'add':
        adds = GetListAdds()
        print(adds)
