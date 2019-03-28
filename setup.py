#!/usr/bin/env python
from web3 import Web3, HTTPProvider
import json
import sys
import requests
from eth_account import Account
import DI_Transactions as dit

args = (sys.argv)[1:]

with open('network.json') as file:
    infor = json.load(file)
    privateKey = infor["privKey"]
    rpc_url = infor["rpcUrl"]

adres = dit.get_adress(privateKey)

web3 = Web3(HTTPProvider(rpc_url))

def GetOwner():
    (Caddress, abi, byte) = dit.contract_info("KYC_Registrar")
    contract_by_address = web3.eth.contract(address = Caddress, abi=abi, bytecode=byte)
    return contract_by_address.functions.GetOwner().call()

def ChangeOwner(person, new_owner):
    (Caddress, abi, byte) = dit.contract_info("KYC_Registrar")
    contract_by_address = web3.eth.contract(address = Caddress, abi=abi, bytecode=byte)
    new_address = web3.toChecksumAddress(new_owner[2:])
    if(GetOwner() != person.address):
        return {'status': -1}

    else:
        tx_wo_sign = contract_by_address.functions.RedactOwner(new_address).buildTransaction({
    		'from': person.address,
    		'nonce': web3.eth.getTransactionCount(person.address),
    		'gas': 8000000,
    		'gasPrice': dit.get_gas_price()
        })
        signed_tx = senderAddress.signTransaction(tx_wo_sign)

        txId = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        TX = web3.eth.waitForTransactionReceipt(txId)
        return TX

if args[0] == '--deploy':
    TX1 = dit.deploy_contract(person=adres, file_name="KYC_Registrar")
    TX2 = dit.deploy_contract(person=adres, file_name="Payment_Handler")
    print("KYC Registrar:", TX1['contractAddress'])
    print("Payment Handler:", TX2['contractAddress'])
    with open('registrar.json', 'w') as file:
        file.write(json.dumps({"registrar": {"address": TX1['contractAddress'], "startBlock": TX1['blockNumber']}, "payments": {"address": TX2['contractAddress'], "startBlock": TX2['blockNumber']}}))

if args[0] == '--owner' and args[1] == 'registrar':
    print("Admin account:", GetOwner())

if args[0] == '--chown' and args[1] == 'registrar' and len(args) == 3:
    new_owner = args[2]
    TX = ChangeOwner(addres, new_owner)
    if TX['status'] == -1:
        print("Request cannot be executed")
    if TX['status'] == 1:
        print("New admin account:", new_owner)
