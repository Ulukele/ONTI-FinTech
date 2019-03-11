import sys
#from py_ecc import secp256k1
from web3 import Web3, HTTPProvider
from eth_account import Account

web3 = Web3(HTTPProvider('https://sokol.poa.network'))


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

def GetAdres(privateKey):
    """
    #Calculate publicKey
    privateKey1 =  bytes.fromhex(privateKey)
    publicKey = secp256k1.privtopub(privateKey1)
    publicKey = hex(publicKey[0])[2:] + hex(publicKey[1])[2:]
    #Calculate adress
    adress = web3.sha3(bytes.fromhex(publicKey))
    adress = adress.hex()[2:]
    adress = adress[len(adress) - 40:]
    adress = web3.toChecksumAddress(adress)
    """
    adress = Account.privateKeyToAccount("0x"+privateKey).address
    adress = web3.toChecksumAddress(adress[2:])
    return adress


def OutBalance(privateKey):
    adres = GetAdres(privateKey)
    balance = BalanceAll(web3.eth.getBalance(adres))
    print("Balance on {0} is {1} {2}".format('"'+ adres[2:] +'"', balance[0], balance[1]))

def Transaction(privateKey, adres2, val):
    adres1 = GetAdres(privateKey)
    adres2NCS = adres2
    adres2 = web3.toChecksumAddress("0x"+adres2)

    if web3.eth.getBalance(adres1) < val:
        print("No enough funds for payment")
        return

    nonce = 0
    nonce = web3.eth.getTransactionCount(adres1)

    transaction = {'to': adres2, 'value': val, 'gas': 21000, 'gasPrice': web3.eth.gasPrice, 'nonce': nonce}
    signed = web3.eth.account.signTransaction(transaction, "0x"+privateKey)

    TransactionHex = web3.eth.sendRawTransaction(signed.rawTransaction).hex()
    balance = BalanceAll(val)
    print("Payment of {0} {1} to {2} scheduled".format(balance[0], balance[1], '"'+web3.toChecksumAddress(adres2NCS)[2:]+'"'))
    print("Transaction Hash: {0}".format(TransactionHex))



args = (sys.argv)[1:]
sizeM = len(args)

if args[0] == "--key":
    if sizeM == 2:
        OutBalance(args[1])
    if sizeM == 6:
        Transaction(args[1], args[3], int(args[5]))

if args[0] == "--tx":
    Transacion = web3.eth.getTransaction(args[1])
    if Transacion == None:
        print("No such transaction in the chain")
    else:
        balance = BalanceAll(Transacion["value"])
        if Transacion["blockNumber"] == None:
            print("Delay in payment of {0} {1} to {2}".format(balance[0], balance[1], '"'+web3.toChecksumAddress(Transacion["to"].lower())[2:]+'"'))
        else:
            print("Payment of {0} {1} to {2} confirmed".format(balance[0], balance[1], '"'+web3.toChecksumAddress(Transacion["to"].lower())[2:]+'"'))
