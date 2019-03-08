#!/usr/bin/env python
import sys
import json
from eth_account import Account
from web3 import Web3, HTTPProvider
import sha3

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

def GetPerson():
    try:
        with open('person.json') as file:
            infor = json.load(file)
            return (infor['id'])
    except:
        return None

def KeyCreate(ident, pin):
    ident = (ident[:8] + ident[9:13] + ident[14:18] + ident[19:23] + ident[24:])

    pin = str(pin)
    pin = [('0'+pin[0]), ('0'+pin[1]), ('0'+pin[2]), ('0'+pin[3])]

    #Calculate privateKey
    data = b''
    for i in range(4):
        data = sha3.keccak_256(data).hexdigest()
        data = data + ident + pin[i]
        data = bytes.fromhex(data)
    data = sha3.keccak_256(data).hexdigest()
    privateKey = data
    return privateKey

def GenerateKey(PINcode):
    personInfo = GetPerson()
    if personInfo == None:
        return None
    key = KeyCreate(personInfo, PINcode)
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

def AddNumberRequest(PINcode, Key, PhoneNum, GasURL, defGas):
    (Caddress, abiKYC, byteKYC) = GetContractInfo()
    if Caddress == None:
        return {'status': -2}
    person = GetAdress(Key)
    try:
        contract_by_address =  web3.eth.contract(address = Caddress, abi = abiKYC)
    except:
        return {'status': -3}

    status = contract_by_address.functions.GetPersonInfo(person.address).call()

    if status:
        return {'status': -1}

    tx_wo_sign = contract_by_address.functions.RequestAddNumber(PhoneNum).buildTransaction({
        'from': person.address,
        'nonce': web3.eth.getTransactionCount(person.address),
        'gas': 8000000,
        'gasPrice': GetGas(GasURL, defGas)
    })
    try:
        signed_tx = person.signTransaction(tx_wo_sign)
        txId = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    except:
        return {'status': -4}
    TX = web3.eth.waitForTransactionReceipt(txId)
    return TX

def DelNumberRequest(PINcode, Key, GasURL, defGas):
    (Caddress, abiKYC, byteKYC) = GetContractInfo()
    if Caddress == None:
        return {'status': -2}
    person = GetAdress(Key)
    try:
        contract_by_address =  web3.eth.contract(address = Caddress, abi = abiKYC)
    except:
        return {'status': -3}

    status = contract_by_address.functions.GetPersonInfo(person.address).call()

    
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
        Key = GenerateKey(PINcode)
        if Key == None:
            print("ID is not found")
        else:
            PrintBalance(Key)

if args[0] == '--add':
    if sizeM > 1:
        PINcode = args[1]
        if sizeM > 2:
            PhoneNum = str(args[2])
        else:
            PhoneNum = '1'
        if len(PhoneNum) != 12 or PhoneNum[0] != '+':
            print("Incorrect phone number")
            sys.exit()
        Key = GenerateKey(PINcode)
        if Key == None:
            print("ID is not found")
        TX = AddNumberRequest(PINcode, Key, PhoneNum, GasURL, defGas)

        if TX['status'] == -4:
            print("No funds to send the request")
        if TX['status'] == -3:
            print("Seems that the contract address is not the registrar contract")
        if TX['status'] == -2:
            print("No contract address")
        if TX['status'] == -1:
            print("Registration request already sent")
        if TX['status'] == 1:
            print('Registration request sent by',TX['transactionHash'].hex())
