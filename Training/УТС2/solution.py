
from web3 import Web3, HTTPProvider
import json
import sys
import urllib
from eth_account import Account

#bytecode
byte = "608060405234801561001057600080fd5b506109c7806100206000396000f3fe608060405234801561001057600080fd5b50600436106100625760003560e01c806301984892146100675780635bcbcf9614610124578063a191247214610180578063a5440fa01461018a578063c18c749d146101e9578063d3a72ea1146102a4575b600080fd5b6100a96004803603602081101561007d57600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050610361565b6040518080602001828103825283818151815260200191508051906020019080838360005b838110156100e95780820151818401526020810190506100ce565b50505050905090810190601f1680156101165780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b6101666004803603602081101561013a57600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050610411565b604051808215151515815260200191505060405180910390f35b610188610467565b005b61019261057b565b6040518080602001828103825283818151815260200191508051906020019060200280838360005b838110156101d55780820151818401526020810190506101ba565b505050509050019250505060405180910390f35b6102a2600480360360208110156101ff57600080fd5b810190808035906020019064010000000081111561021c57600080fd5b82018360208201111561022e57600080fd5b8035906020019184600183028401116401000000008311171561025057600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f820116905080830192505050505050509192919290505050610609565b005b6102e6600480360360208110156102ba57600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050610816565b6040518080602001828103825283818151815260200191508051906020019080838360005b8381101561032657808201518184015260208101905061030b565b50505050905090810190601f1680156103535780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b60006020528060005260406000206000915090508054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156104095780601f106103de57610100808354040283529160200191610409565b820191906000526020600020905b8154815290600101906020018083116103ec57829003601f168201915b505050505081565b6000600160008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff169050919050565b600160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff1615156104bf57600080fd5b6000600160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff021916908315150217905550604051806020016040528060008152506000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002090805190602001906105789291906108f6565b50565b606060048054806020026020016040519081016040528092919081815260200182805480156105ff57602002820191906000526020600020905b8160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190600101908083116105b5575b5050505050905090565b600160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff1615151561066257600080fd5b806000803373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002090805190602001906106b49291906108f6565b5060018060003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff0219169083151502179055506000600260003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002054141561081357600360008154809291906001019190505550600354600260003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000208190555060043390806001815401808255809150509060018203906000526020600020016000909192909190916101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550505b50565b60606000808373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000208054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156108ea5780601f106108bf576101008083540402835291602001916108ea565b820191906000526020600020905b8154815290600101906020018083116108cd57829003601f168201915b50505050509050919050565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f1061093757805160ff1916838001178555610965565b82800160010185558215610965579182015b82811115610964578251825591602001919060010190610949565b5b5090506109729190610976565b5090565b61099891905b8082111561099457600081600090555060010161097c565b5090565b9056fea165627a7a72305820297ceb5aadc6f0f8df8d9bc614deb048b02fc18f2b11141e5f359239d256a9020029"

#abi code
abi = json.loads("""[
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
	TX = {'status': 0, 'transactionHash': 0}
	state = contract_by_address.functions.GetStatus(person.address).call()
	if state == False:
		try:
			txId = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
			TX = web3.eth.waitForTransactionReceipt(txId)
		except:
			return {'status': -1, 'transactionHash': 0}
	return TX

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
	TX = {'status': 0, 'transactionHash': 0}
	state = contract_by_address.functions.GetStatus(person.address).call()
	if state:
		try:
			txId = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
			TX = web3.eth.waitForTransactionReceipt(txId)
		except:
			return {'status': -1, 'transactionHash': 0}
	print(TX)
	return TX

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
			try:
				list[name].append(i)
			except:
				list[name] = [i]
	return list

def GetAcc(Caddres, abi, name):
	RawList = GetList(Caddres, abi)
	for i in RawList:
		if i == name:
			return RawList[i]


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
		for j in range(len(list[i])):
			print('"',i,'"',': ', list[i][j], sep ='')

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
