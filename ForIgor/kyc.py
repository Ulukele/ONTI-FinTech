#!/usr/bin/env python
import sys
import json
from eth_account import Account
from web3 import Web3, HTTPProvider
import sha3

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

    contract_by_address =  web3.eth.contract(address = Caddress, abi = abiKYC)

    statusA = contract_by_address.functions.GetPersonInfoAR(person.address).call()
    statusD = contract_by_address.functions.GetPersonInfoDR(person.address).call()
    if(not (statusA or statusD)):
        return {'status': -1}
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

with open('network.json') as file:
    infor = json.load(file)
    privateKey = infor["privKey"]
    RecURL = infor["rpcUrl"]
    GasURL = infor["gasPriceUrl"]
    defGas = infor["defaultGasPrice"]

web3 = Web3(HTTPProvider(RecURL))
address = GetAdress(privateKey)
