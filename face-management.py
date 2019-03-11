import cognitive_face as cf
import json
from json import load
import cv2
import datetime
import sys
import os
from face_lib import add_new_person, checker, recognize, delete_person, list_of_users, train, update_user_data, identification, head_attrib, identification_for_simple_add, recognize_for_add2
import math
from imutils.video import VideoStream, FileVideoStream
from imutils import face_utils
import imutils

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
    try:
        identification_for_simple_add(file_name, group)
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
