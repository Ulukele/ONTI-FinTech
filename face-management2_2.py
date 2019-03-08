import cognitive_face as cf 
import json
from json import load
import cv2
import datetime
import sys
import os

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
        path = 'add_image.jpg'
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

def train(group):
    cf.person_group.train(group)
    
def update_user_data(group, message):
    cf.person_group.update(group, user_data=message)

def identification(file_name, group):
    vid = str(file_name)
    cap  = cv2.VideoCapture(vid)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if length < 5:
        print('The video does not follow requirements')
        try:
            os.remove('person.json')
        except FileNotFoundError:
            pass
        sys.exit()
    cap.release()
    k = 0
    faceIds = []
    candidates = []

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
        path = 'id_image.jpg'
        cv2.imwrite(path, frame)
        face = cf.face.detect(path)
        if face == []:
            print('The video does not follow requirements')
            try:
                os.remove('person.json')
            except FileNotFoundError:
                pass
            sys.exit()
        else:
            faceIds.append(face[0]['faceId'])
            k += 1
            cap.release()
    candidates_info = cf.face.identify(faceIds, person_group_id=group)  

    for i in range(5):
        candidates.append(candidates_info[i]['candidates'])
    if (candidates[0]['personId'] == candidates[1]['personId'] == candidates[2]['personId'] == candidates[3]['personId'] == candidates[4]['personId']) and (candidates[0]['confidence'] >= 0.5) and (candidates[1]['confidence'] >= 0.5) and (candidates[2]['confidence'] >= 0.5) and (candidates[3]['confidence'] >= 0.5) and (candidates[4]['confidence'] >= 0.5):
        candidate_id = candidates[0]['personId']
        f= open("person.json","w+")
        f.write(json.dumps({"id": str(candidates[0]['personId'])}))
    else:
        print('The person was not found')
        try:
            os.remove('person.json')
        except FileNotFoundError:
            pass
        sys.exit()

args = (sys.argv)[1:]
datetime_object = datetime.datetime.now()
name = hash(datetime_object)

if args[0] == '--simple-add':
    file_name = args[1]
    checker(file_name)
    try:
        cf.person_group.create(group)
    except:
        pass
    user_id = add_new_person(group, name)
    ids = recognize(file_name, group, user_id['personId'])
    message = 'group_update'
    cf.person_group.update(group, user_data=message)
    print("5 frames extracted")
    print("PersonId:", user_id['personId'])
    print("FaceIds\n=======")
    for i in ids:
        print(i) 
if args[0] == '--train':
    try:
       cf.person_group.get(group)
    except cf.CognitiveFaceException as err:
         if err.code == 'PersonGroupNotFound':
                print('There is nothing to train')
                sys.exit()
    users = list_of_users(group)
    if len(users) == 0:
        print('There is nothing to train')
        sys.exit()
    data = cf.person_group.get(group)['userData']
    if data == 'group_update':
        train(group)
        print('Training successfully started')
        message = 'group_train'
        update_user_data(group, message)
    elif data == 'group_train':
        print('Already trained')
if args[0] == '--del':
    person_id = args[1]
    try:
       cf.person_group.get(group)
    except cf.CognitiveFaceException as err:
         if err.code == 'PersonGroupNotFound':
                print('The group does not exist')
                sys.exit()
    try:
        delete_person(group, person_id)
        print('Person deleted')
        message = 'group_update'
        update_user_data(group, message)
    except cf.CognitiveFaceException as err:
        if err.code == 'PersonNotFound':
            print("The person does not exist")
            sys.exit()
if args[0] == '--list':
    user_list = []
    try:
        info_from_group = list_of_users(group)
        for i in range(len(info_from_group)):
            user_list.append(info_from_group[i]['personId'])
        if len(user_list) == 0:
            print('No persons found')
        else:
            print('Persons IDs:')
            for i in range(len(user_list)):
                print(user_list[i])
    except cf.CognitiveFaceException as err:
        if err.code == 'PersonGroupNotFound':
            print('The group does not exist')
            sys.exit()
if args[0] == '--find':
    file_name = args[1]
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
