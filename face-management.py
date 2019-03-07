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
cf.Key.set(key)

def add_new_person(group, name):
    user_id = cf.person.create(group, name)
    return user_id

def delete_person(group, user_id):
    cf.person.delete(group, user_id)
    return user_id

def recognize(fileName, group, name):
    vid = str(fileName)
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
            try:
                cf.person_group.create(group)
            except:
                pass
            ID = add_new_person(group, name)
            persisted_face_id = cf.person.add_face(path, group, ID['personId'])
            face_ids.append(persisted_face_id['persistedFaceId'])
            k += 1
            cap.release()
    return face_ids, ID

args = (sys.argv)[1:]
datetime_object = datetime.datetime.now()
name = hash(datetime_object)

if args[0] == '--simple-add':
    file_name = args[1]
    ids, user_id = recognize(file_name, group, name)
    print("5 frames extracted")
    print("PersonId:", user_id['personId'])
    print("FaceIds\n=======")
    for i in ids:
        print(i)