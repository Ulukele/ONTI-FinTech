#!/usr/bin/env python
import sys
import json
from eth_account import Account
from web3 import Web3, HTTPProvider
import sha3
import cognitive_face as cf
import os
from face_lib import add_new_person, checker, recognize, delete_person, list_of_users, train, update_user_data, identification, checker_for_find

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

def checkNumber(phoneNum):
    phoneNum = str(phoneNum)
    if(phoneNum[0] == '+' and len(phoneNum) == 12):
        for i in range(1, 12):
            if(phoneNum[i] < '0' and phoneNum[i] > '9'):
                return False
        return True
    else:
        return False

def AddNumberRequest(PINcode, Key, PhoneNum, GasURL, defGas):
    (Caddress, abiKYC, byteKYC) = GetContractInfo()
    if Caddress == None:
        return {'status': -2}
    person = GetAdress(Key)
    try:
        contract_by_address =  web3.eth.contract(address = Caddress, abi = abiKYC)
    except:
        return {'status': -3}

    status = contract_by_address.functions.GetPersonInfoAR(person.address).call()

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

    status = contract_by_address.functions.GetPersonInfoEST(person.address).call()
    if status == False:
        return {'status': -5}
    status = contract_by_address.functions.GetPersonInfoDR(person.address).call()
    if status:
        return {'status': -1}
    tx_wo_sign = contract_by_address.functions.RequestDelNumber().buildTransaction({
        'from': person.address,
        'nonce': web3.eth.getTransactionCount(person.address),
        'gas': 8000000,
        'gasPrice': GetGas(GasURL, defGas)
    })

    try:
        signed_tx = person.signTransaction(tx_wo_sign)
        txId = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    except:
         {'status': -4}
    TX = web3.eth.waitForTransactionReceipt(txId)
    return TX


def GetAddressWithPhone(phoneNum):
        contract_by_address = web3.eth.contract(address = GetContractAddress(), abi = abiKYC)
        return contract_by_address.functions.GetAddress(phoneNum).call()

def Transaction(privateKey, adres2, val):
    adres1 = GetAdres(privateKey)
    adres2 = web3.toChecksumAddress("0x"+adres2)

    nonce = 0
    nonce = web3.eth.getTransactionCount(adres1)

    transaction = {'to': adres2, 'value': val, 'gas': 8000000, 'gasPrice': GetGas(GasURL, defGas), 'nonce': nonce}
    signed = web3.eth.account.signTransaction(transaction, "0x"+privateKey)

    TransactionHex = web3.eth.sendRawTransaction(signed.rawTransaction).hex()
    balance = BalanceAll(val)
    print("Payment of {0} {1} to {2} scheduled".format(balance[0], balance[1], '"'+web3.toChecksumAddress(adres2NCS)[2:]+'"'))
    print("Transaction Hash: {0}".format(TransactionHex))

def sendFunds(pinCode, phoneNum, value):
    addressFrom = GenerateKey(pinCode)
    if(web3.eth.getBalance(addressFrom) < value):
        print("No funds to send the payment")
        return False
    if(not checkNumber(phoneNum)):
        print("Incorrect phone number")
        return False
    address2 = GetAddressWithPhone(phoneNum)
    if(len(address2) == 0):
        print("No account with the phone number", phoneNum)
        return False
    Transaction(addressFrom, address2, value)

args = (sys.argv)[1:]
sizeM = len(args)

with open('faceapi.json') as file:
    json2 = json.load(file)
    key = json2['key']
    BASE_URL = json2['serviceUrl']
    group = json2['groupId']

cf.BaseUrl.set(BASE_URL)

try:
    e = cf.Key.set(key)
except:
    print( "Incorrect subscription key")
    sys.exit()

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
            PhoneNum = '+1'
        if not checkNumber(PhoneNum):
            print("Incorrect phone number")
            sys.exit()
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

if args[0] == '--del':
    if sizeM > 1:
        PINcode = args[1]
        Key = GenerateKey(PINcode)
        if Key == None:
            print("ID is not found")
        TX = DelNumberRequest(PINcode, Key, GasURL, defGas)
        if TX['status'] == -5:
            print("Account is not registered yet")
        if TX['status'] == -4:
            print("No funds to send the request")
        if TX['status'] == -3:
            print("Seems that the contract address is not the registrar contract")
        if TX['status'] == -2:
            print("No contract address")
        if TX['status'] == -1:
            print("Unregistration request already sent")
        if TX['status'] == 1:
            print("Unregistration request sent by", TX['transactionHash'].hex())

if args[0] == "--send" and len(args) == 4: # <pin code> <phone number> <value>
    pinCode = str(args[1])
    phoneNum = str(args[2])
    value = int(args[3])
    sendFunds(pinCode, phoneNum, value)

if args[0] == '--find':
    file_name = args[1]
    checker_for_find(file_name)
    try:
       cf.person_group.get(group)
    except cf.CognitiveFaceException as err:
         if err.code == 'PersonGroupNotFound':
                print('The service is not ready')
                sys.exit()
    if cf.person_group.get(group)['userData'] == 'group_train':
        identification(file_name, group)
    elif cf.person_group.get(group)['userData'] == 'group_update':
        print('The service is not ready')
        try:
            os.remove('person.json')
        except FileNotFoundError:
            pass
        sys.exit()
    try:
        cf.person_group.get(group)
    except cf.CognitiveFaceException as err:
        if err.code == 'PersonGroupNotFound':
            print('The service is not ready')
            try:
                os.remove('person.json')
            except FileNotFoundError:
                pass
            sys.exit()
