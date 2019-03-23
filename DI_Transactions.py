import web3
from web3 import Web3, HTTPProvider
import json
import sys
import urllib
from eth_account import Account

#connecting
with open("network.json") as file:
    rpc_url = json.loads(file.read())['rpcUrl']
web3 = Web3(HTTPProvider(rpc_url))

def get_adress(private_key):
    adress = Account.privateKeyToAccount("0x"+private_key)
    return adress

def balance_all(balance):
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

def contract_info(file_name):
    with open(file_name+'Byte.txt') as file:
        byte = str(file.read())
        if byte[-1] == '\n':
            byte = byte[:-1]
    with open(file_name+'ABI.txt') as file:
        abi = file.read()
        abi = json.loads(abi)

def get_gas_price(url='', def_gas=1000000000):
    try:
        response = requests.get(URL).text
        gasinfo = json.loads(response)['fast']
    except:
        return def_gas
    return int(gasinfo * 1000000000)

def deploy_contract(person, to, value, file_name="KYC_Registrar", gas_price=get_gas_price()):
    #contract preparation
    (abi, byte) = contract_info(file_name)
    contract = web3.eth.contract(abi=abi, bytecode=byte)
    #sign
    signed_tx = contract.constructor().buildTransaction({
    'from': person.address,
    'nonce': web3.eth.getTransactionCount(person.address),
    'gasPrice': get_gas_price()
    })
    signed_tx = person.signTransaction(signed_tx)
    #deploying
    raw_tx = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    TX = web3.eth.waitForTransactionReceipt(raw_tx)

    return TX

def call_contract():
    print("Do it later")

def send_to(person, to, value, print_info=False):
    #check balance
    if web3.eth.getBalance(person.address) < val:
        print("No enough funds for payment")
        return {'status': -1}
    #sign
    signed_tx = {'to': to, 'value': value, 'gasPrice': get_gas_price(), 'nonce': web3.eth.getTransactionCount(person.address)}
    signed_tx = person.signTransaction(signed_tx)
    #sending transaction
    raw_tx = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    TX = web3.eth.waitForTransactionReceipt(raw_tx)
    #optional
    #printing info
    if print_info:
        balance = balance_all(value)
        print("Payment of {0} {1} from {2} to {3} scheduled".format(balance[0], balance[1], person.address, '"'+web3.toChecksumAddress(to)[2:]+'"'))
        print("Transaction Hash: {0}".format(TX['transactionHash'].hex()))
    return TX
