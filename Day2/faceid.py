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
    with open('registrar.json') as file:
        infor = json.load(file)
        Caddress = infor['registrar']['address']
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
    person = GetAdress(Key)
    contract_by_address =  web3.eth.contract(address = Caddress, abi = abiKYC)
    tx_wo_sign = contract_by_address.functions.RequestAddNumber(PhoneNum).buildTransaction({
        'from': person.address,
        'nonce': web3.eth.getTransactionCount(person.address),
        'gas': 8000000,
        'gasPrice': GetGas(GasURL, defGas)
    })
    signed_tx = person.signTransaction(tx_wo_sign)
    txId = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    TX = web3.eth.waitForTransactionReceipt(txId)
    return TX['transactionHash'].hex()

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
    if sizeM > 2:
        PINcode = args[1]
        PhoneNum = int(args[2])
        Key = GenerateKey(PINcode)
        if Key == None:
            print("None")
        TX = AddNumberRequest(PINcode, Key, PhoneNum, GasURL, defGas)
        print(TX)
