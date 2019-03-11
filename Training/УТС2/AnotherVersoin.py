from web3 import Web3, HTTPProvider
import json
import sys
import urllib
from eth_account import Account

#bytecode
byte = "608060405234801561001057600080fd5b5061068e806100206000396000f3fe608060405234801561001057600080fd5b506004361061007e577c010000000000000000000000000000000000000000000000000000000060003504630198489281146100835780635bcbcf961461012b578063a191247214610172578063a5440fa01461017c578063c18c749d146101d4578063d3a72ea11461027a575b600080fd5b6100b66004803603602081101561009957600080fd5b503573ffffffffffffffffffffffffffffffffffffffff166102ad565b6040805160208082528351818301528351919283929083019185019080838360005b838110156100f05781810151838201526020016100d8565b50505050905090810190601f16801561011d5780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b61015e6004803603602081101561014157600080fd5b503573ffffffffffffffffffffffffffffffffffffffff16610347565b604080519115158252519081900360200190f35b61017a610372565b005b6101846103ce565b60408051602080825283518183015283519192839290830191858101910280838360005b838110156101c05781810151838201526020016101a8565b505050509050019250505060405180910390f35b61017a600480360360208110156101ea57600080fd5b81019060208101813564010000000081111561020557600080fd5b82018360208201111561021757600080fd5b8035906020019184600183028401116401000000008311171561023957600080fd5b91908080601f01602080910402602001604051908101604052809392919081815260200183838082843760009201919091525092955061043e945050505050565b6100b66004803603602081101561029057600080fd5b503573ffffffffffffffffffffffffffffffffffffffff16610514565b600060208181529181526040908190208054825160026001831615610100026000190190921691909104601f81018590048502820185019093528281529290919083018282801561033f5780601f106103145761010080835404028352916020019161033f565b820191906000526020600020905b81548152906001019060200180831161032257829003601f168201915b505050505081565b73ffffffffffffffffffffffffffffffffffffffff1660009081526001602052604090205460ff1690565b3360009081526001602052604090205460ff16151561039057600080fd5b336000818152600160209081526040808320805460ff1916905580518083018083528482529484529183905290912090516103cb92906105ca565b50565b6060600480548060200260200160405190810160405280929190818152602001828054801561043357602002820191906000526020600020905b815473ffffffffffffffffffffffffffffffffffffffff168152600190910190602001808311610408575b505050505090505b90565b3360009081526001602052604090205460ff161561045b57600080fd5b336000908152602081815260409091208251610479928401906105ca565b50336000908152600160208181526040808420805460ff19169093179092556002905290205415156103cb5760038054600190810191829055336000818152600260205260408120939093556004805492830181559092527f8a35acfbc15ff81a39ae7d344fd709f28e8600b4aa8c65c6b64bfe7fe36bd19b01805473ffffffffffffffffffffffffffffffffffffffff1916909117905550565b73ffffffffffffffffffffffffffffffffffffffff81166000908152602081815260409182902080548351601f60026000196101006001861615020190931692909204918201849004840281018401909452808452606093928301828280156105be5780601f10610593576101008083540402835291602001916105be565b820191906000526020600020905b8154815290600101906020018083116105a157829003601f168201915b50505050509050919050565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f1061060b57805160ff1916838001178555610638565b82800160010185558215610638579182015b8281111561063857825182559160200191906001019061061d565b50610644929150610648565b5090565b61043b91905b80821115610644576000815560010161064e56fea165627a7a72305820d3b67ba8604b24e091f2291b438be5da9236d253d2f6bf1f397f65589e0b608a0029"

#abi code
abi = json.loads("""[
	{
		"constant": true,
		"inputs": [
			{
				"name": "",
				"type": "address"
			}
		],
		"name": "name",
		"outputs": [
			{
				"name": "",
				"type": "string"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_person",
				"type": "address"
			}
		],
		"name": "GetStatus",
		"outputs": [
			{
				"name": "",
				"type": "bool"
			}
		],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [],
		"name": "RemoveName",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [],
		"name": "GetAll",
		"outputs": [
			{
				"name": "",
				"type": "address[]"
			}
		],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_name",
				"type": "string"
			}
		],
		"name": "AddName",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_person",
				"type": "address"
			}
		],
		"name": "GetName",
		"outputs": [
			{
				"name": "",
				"type": "string"
			}
		],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	}
]""")

def GetGas():
    f = urllib.request.urlopen("https://gasprice.poa.network")
    gasinfo = json.loads(f.read().decode('utf-8'))['fast']
    return int(gasinfo * 1000000000)

def GetAdres(privateKey):
    adress = Account.privateKeyToAccount("0x"+privateKey)
    return adress

def SetTransaction(abi, byte, person):

	#create transaction
	contract = web3.eth.contract(abi=abi, bytecode=byte)
	SignedTX = contract.constructor().buildTransaction({
	'from': person.address,
	'nonce': web3.eth.getTransactionCount(person.address),
	'gasPrice': GetGas()
	})
	SignedTX = person.signTransaction(SignedTX)
	RawTX = web3.eth.sendRawTransaction(SignedTX.rawTransaction)
	TXReceipt = web3.eth.waitForTransactionReceipt(RawTX)
	#write transaction info
	f = open('database.json', 'w')
	f.close()
	with open('database.json', 'w') as file:
		file.write(json.dumps({'registrar': TXReceipt['contractAddress'], 'startBlock': TXReceipt['blockNumber']}))
	return {'registrar': TXReceipt['contractAddress'], 'startBlock': TXReceipt['blockNumber']}

def AddName(Caddres, abi, byte, person, name):
	#create transaction
	contract_by_address =  web3.eth.contract(address = Caddres, abi = abi)
	tx_wo_sign = contract_by_address.functions.AddName(name).buildTransaction({
		'from': person.address,
		'nonce': web3.eth.getTransactionCount(person.address),
		'gas': 8000000,
		'gasPrice': GetGas()
    })
	signed_tx = person.signTransaction(tx_wo_sign)
	#sending transaction
	try:
		txId = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
	except:
		return {'status': -1}

	txReceipt = web3.eth.waitForTransactionReceipt(txId)
	return txReceipt

def RemoveName(person, abi):
	#create transaction
	contract_by_address =  web3.eth.contract(address = Caddres, abi = abi)
	tx_wo_sign = contract_by_address.functions.RemoveName().buildTransaction({
    	'from': person.address,
    	'gas': 8000000,
    	'nonce': web3.eth.getTransactionCount(person.address),
    	'gasPrice': GetGas()
	})
	signed_tx = person.signTransaction(tx_wo_sign)
	#sending transaction
	try:
		txId = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
	except:
		return {'status': -1}

	txReceipt = web3.eth.waitForTransactionReceipt(txId)
	return txReceipt

def GetName(Caddres, abi, person):
    contract_by_address = web3.eth.contract(address = Caddres, abi = abi)
    return contract_by_address.functions.GetName(person).call()

def GetList(Caddres, abi):
	contract_by_address = web3.eth.contract(address = Caddres, abi = abi)
	RawList = contract_by_address.functions.GetAll().call()
	list = {}
	for i in RawList:
		name = GetName(Caddres, abi, i)
		if name != '':
			list[name] = i
	return list

def GetAcc(Caddres, abi, name):
	RawList = GetList(Caddres, abi)
	list = []
	for i in RawList:
		if i == name:
			list.append(RawList[i])
	return list



#Connection
web3 = Web3(HTTPProvider('https://sokol.poa.network'))

#Get account info
with open('account.json') as file:
    privateKey = json.load(file)['account']
address = GetAdres(privateKey)

#get arguments
args = (sys.argv)[1:]
if(len(args) > 2):
	for i in range(2, len(args)):
		args[1] = args[1] + " " + args[i]



if args[0] == '--deploy':
	TRInfo = SetTransaction(abi, byte, address)
	print("Contract address:", TRInfo['registrar'])
    #print(TRInfo)

#Get transaction info
with open('database.json') as file:
    Caddres = json.load(file)['registrar']

if args[0] == '--add':
	TRInfo = AddName(Caddres, abi, byte, address, args[1])
	if(TRInfo['status'] == 0):
		print("One account must correspond one name")
	if(TRInfo['status'] == -1):
		print("No enough funds to add name")
	if(TRInfo['status'] == 1):
		print("Successfully added by", (TRInfo["transactionHash"]).hex())
	#print(TRInfo)

if args[0] == '--del':
	TRInfo = RemoveName(address, abi)
	if(TRInfo['status'] == 0):
		print("No name found for your account")
	if(TRInfo['status'] == -1):
		print("No enough funds to delete name")
	if(TRInfo['status'] == 1):
		print("Successfully deleted by",  TRInfo["transactionHash"].hex())
	#print(TRInfo)

if args[0] == '--getname':
	name = GetName(Caddres, abi, web3.toChecksumAddress(args[1]))
	if(name == ''):
		print("No name registered for this account")
	else:
		print("Registered account is ",'"', name, '"', sep='')

if args[0] == '--list':
	list = GetList(Caddres, abi)
	for i in list:
		print('"',i,'"',': ', list[i], sep ='')

if args[0] == '--getacc':
	list = GetAcc(Caddres, abi, args[1])
	if(len(list) == 0):
		print("No account registered for this name")
	if(len(list) == 1):
		print("Registered account is", list[0])
	if(len(list) > 1):
		print("Registered accounts are:")
		for i in list:
			print(i)


"""
print("\nFile Info:\n")
print(privateKey)
"""
