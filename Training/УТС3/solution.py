import json
import sys
import cognitive_face as cf

def Recognize(fileName):
    #Recognize face by video
    #returns person Id
    #example: 419e345a-e6d6-4d9c-953d-667787b8d52e
    print()

def GetAllId(group):
    #get all id from GROUP
    #returns list of ID's
    return ()

def AddToGroup(group, name, id):
    #add person with id: ID, with name: NAME into GROUP
    #returns id
    result = {'result': 1, 'id': "419e345a-e6d6-4d9c-953d-667787b8d52e"}
    return result

def RemoveFromGroup(group, name):
    #remove person with name: NAME from GROUP
    #returns id
    result = {'result': 1, 'id': "419e345a-e6d6-4d9c-953d-667787b8d52e"}
    return result

def Train():
    #Train
    print()

def TryIdentify(fileName):
    #try to identify person by video
    #returns name
    name = {'result': 1, 'name': ""}
    return name




#start here:
args = (sys.argv)[1:]

#read files:
with open('msfaceapi.json') as file:
    key = json.load(file)['key']

with open('faceid.json') as file:
    group = json.load(file)['groupId']

#call functions:
if args[0] == '--name':
    id = AddToGroup(group, args[1], args[2])

    if id['result'] == 0:
        print("Video does not contain any face")
    if id['result'] == 1:
        print("5 frames extracted")
        print("PersonId:", id['id'])
        print("FaceIds\n=======")
        FaceGroup = GetAllId(group)
        for i in FaceGroup:
            print(i)


if args[0] == '--del':
    id = RemoveFromGroup(group, args[1])

    if id['result'] == 0:
        print("No person with name {}".format('"'+args[1]+'"'))
    if id['result'] == 1:
        print("Person with id {} deleted".format(id['id']))


if args[0] == '--train':
    Train()


if args[0] == '--identify':
    name = TryIdentify()

    if name['result'] == 1:
        print("The person is {}".format('"'+name['name']+'"'))
    if name['result'] == 0:
        print("The person cannot be identified")
    if name['result'] == -1:
        print("The system is not ready yet")
