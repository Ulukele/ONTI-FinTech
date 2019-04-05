import sys
import json
from eth_account import Account
from web3 import Web3, HTTPProvider
import sha3
import requests
import DI_Transactions as dit

def ApproveRequest(person, addres):
    (Caddress, abiKYC, byteKYC) = dit.contract_info('KYC_Registrar')

    if Caddress == None:
        return {'status': -2}
    try:
        contract_by_address =  web3.eth.contract(address=Caddress, abi=abiKYC, bytecode=byteKYC)
    except:
        return {'status': -3}


    statusA = contract_by_address.functions.GetPersonInfoAR(addres).call()
    statusD = contract_by_address.functions.GetPersonInfoDR(addres).call()

    if not (statusA or statusD):
        return {'status': -1}

    tx_wo_sign = contract_by_address.functions.Confirm(addres).buildTransaction({
        'from': person.address,
        'nonce': web3.eth.getTransactionCount(person.address),
        'gas': 8000000,
        'gasPrice': dit.get_gas_price()
    })

    signed_tx = person.signTransaction(tx_wo_sign)
    txId = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    TX = web3.eth.waitForTransactionReceipt(txId)
    return TX

def AddresByNumber(PhoneNum):
    (Caddress, abiKYC, byteKYC) = dit.contract_info('KYC_Registrar')
    if Caddress == None:
        return {'status': -2}
    try:
        contract_by_address =  web3.eth.contract(address=Caddress, abi=abiKYC, bytecode=byteKYC)
    except:
        return {'status': -3}

    TX = {'status': 1, 'result': ''}
    TX['result'] = contract_by_address.functions.GetAddress(PhoneNum).call()
    if TX['result'] == '0x0000000000000000000000000000000000000000':
        TX['status'] = -1
    return TX

def GetListAdds():
    (Caddress, abiKYC, byteKYC) = dit.contract_info('KYC_Registrar')

    if Caddress == None:
        return {'status': -2}
    try:
        contract_by_address =  web3.eth.contract(address=Caddress, abi=abiKYC, bytecode=byteKYC)
    except:
        return {'status': -3}
    adds = contract_by_address.events.RegistrationRequest().createFilter(fromBlock='latest').get_new_entries()

    return adds

args = (sys.argv)[1:]
sizeM = len(args)

with open('network.json') as file:
    infor = json.load(file)
    privateKey = infor["privKey"]
    rpc_url = infor["rpcUrl"]

web3 = Web3(HTTPProvider(rpc_url))
person = dit.get_adress(privateKey)

if args[0] == '--confirm':
    addres = args[1]
    TX = ApproveRequest(person, addres)

    if TX['status'] == -3:
        print("Seems that the contract address is not the registrar contract")
    if TX['status'] == -2:
        print("No contract address")
    if TX['status'] == -1:
        print("No requests")
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
