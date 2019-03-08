import cognitive_face as cf 
import json
from json import load
import cv2
import datetime
import sys

with open('faceapi.json') as file:
    json = json.load(file)
    key = json['key']
    BASE_URL = json['serviceUrl']
    group = json['groupId']

cf.BaseUrl.set(BASE_URL)
try:
    e = cf.Key.set(key)
except:
    print( "Incorrect subscription key")
    sys.exit()


def add_new_person(group, name):
    user_id = cf.person.create(group, name)
    return user_id

def train(group):
    cf.person_group.train(group)

def train_status(group):
    status = cf.person_group.get_status(group)
    return status

def checker(file_name):
    vid = str(file_name)
    cap  = cv2.VideoCapture(vid)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if length < 5:
        print('Video does not contain any face')
        sys.exit()
    cap.release()
    k = 0
    face_ids = []

    while k < 5:
        beg = -1
        end = length - 1
        step = length//5
        frame_num = 0
        if (k == 0):
            frame_num = beg
            cap.set(2, frame_num)
            cap  = cv2.VideoCapture(vid)
        if (k == 5):
            frame_num = end
            cap.set(2, frame_num)
            cap  = cv2.VideoCapture(vid)
        else:
            frame_num = beg + k*step
            cap.set(2, frame_num)
            cap  = cv2.VideoCapture(vid)
        ret, frame = cap.read()
        path = 'image.jpg'
        cv2.imwrite(path, frame)
        face = cf.face.detect(path)
        if face == []:
            print('Video does not contain any face')
            sys.exit()
        else:
            k+=1
    return True

def recognize(file_name, group, user_id):
    vid = str(file_name)
    cap  = cv2.VideoCapture(vid)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    k = 0
    face_ids = []

    while k < 5:
        beg = -1
        end = length - 1
        step = length//5
        frame_num = 0
        if k == 0:
            frame_num = beg
            cap.set(2, frame_num)
            cap  = cv2.VideoCapture(vid)
        if k == 5:
            frame_num = end
            cap.set(2, frame_num)
            cap  = cv2.VideoCapture(vid)
        else:
            frame_num = beg + k*step
            cap.set(2, frame_num)
            cap  = cv2.VideoCapture(vid)
        ret, frame = cap.read()
        path = 'image.jpg'
        cv2.imwrite(path, frame)
        face = cf.face.detect(path)
        if face == []:
            print('Video does not contain any face')
            sys.exit()
        else:
            persisted_face_id = cf.person.add_face(path, group, user_id)
            face_ids.append(persisted_face_id['persistedFaceId'])
            k += 1
            cap.release()
    return face_ids

def delete_person(group, person_id):
    e = cf.person.delete(group, name)
    return e

def list_of_users(group):
    list_of_users = cf.person.lists(group)
    return list_of_users

args = (sys.argv)[1:]
datetime_object = datetime.datetime.now()
name = hash(datetime_object)

if args[0] == '--simple-add':
    status = train_status(group)
    file_name = args[1]
    checker(file_name)
    try:
        cf.person_group.create(group)
    except:
        pass
    user_id = add_new_person(group, name)
    ids = recognize(file_name, group, user_id['personId'])
    print("5 frames extracted")
    print("PersonId:", user_id['personId'])
    print("FaceIds\n=======")
    for i in ids:
        print(i) 

if args[0] == '--train':
    train(group)
    status = train_status(group)
    #print('Training task for {} persons started'.format())
if args[0] == '--del':
    person_id = args[1]
    try:
       cf.person_group.get(group)
    except cf.CognitiveFaceException as err:
         if err.code == 'PersonGroupNotFound':
                print('The group does not exist')
    try:
        delete_person(group, person_id)
        print('Person deleted')
    except cf.CognitiveFaceException as err:
        if err.code == 'PersonNotFound':
            print("The person does not exist")
if args[0] == '--list':
    user_list = []
    try:
        info_from_group = list_of_users(group)
        for i in range(len(info_from_group)):
            user_list.append(info_from_group[i]['personId'])
        print('Persons IDs:')
        for i in range(len(user_list)):
            print(user_list[i])
    except cf.CognitiveFaceException as err:
        if err.code == 'PersonGroupNotFound':
            print('The group does not exist')