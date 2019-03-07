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

try:
    cf.large_person_group.create(group)
except:
    pass

def add_new_person(group, name):
    user_id = cf.large_person_group_person.create(group, name)
    return user_id

def recognize(fileName, group, user_id):
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
            persisted_face_id = cf.large_person_group_person_face.add(path, group, user_id['personId'])
            face_ids.append(persisted_face_id['persistedFaceId'])
            k += 1
            cap.release()
    return face_ids

args = (sys.argv)[1:]
datetime_object = datetime.datetime.now()
name = hash(datetime_object)

if args[0] == '--simple-add':
    user_id = add_new_person(group, name)
    file_name = args[1]
    ids = recognize(file_name, group, user_id)
    print("5 frames extracted")
    print("PersonId:", user_id['personId'])
    print("FaceIds\n=======")
    for i in ids:
        print(i)

