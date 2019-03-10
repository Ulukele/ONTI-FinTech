import cognitive_face as cf 
import json
from json import load
import cv2
import datetime
import sys
import os

def recognize_for_add2(file_name, group, user_id):
    face = cf.face.detect(file_name)
    persisted_face_id = cf.person.add_face(file_name, group, user_id)
    face_id = persisted_face_id['persistedFaceId']
    return face_id

def head_attrib(file_name):
    face_return = cf.face.detect(file_name, face_id=False, attributes='headPose', landmarks=True)
    upper_lip_top = face_return[0]['faceLandmarks']['upperLipTop']
    upper_lip_bottom = face_return[0]['faceLandmarks']['upperLipBottom']
    under_lip_top = face_return[0]['faceLandmarks']['underLipTop']
    under_lip_bottom = face_return[0]['faceLandmarks']['underLipBottom']
    pupil_left = face_return[0]['faceLandmarks']['pupilLeft']
    pupil_right = face_return[0]['faceLandmarks']['pupilRight']
    roll = face_return[0]['faceAttributes']['headPose']['roll']
    yaw = face_return[0]['faceAttributes']['headPose']['yaw']
    return pupil_left, pupil_right
    
def add_new_person(group, name):
    user_id = cf.person.create(group, name)
    return user_id

def checker_for_find(file_name):
    vid = str(file_name)
    cap  = cv2.VideoCapture(vid)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if length < 5:
        print('The video does not follow requirements')
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
            print('The video does not follow requirements')
            sys.exit()
        else:
            k+=1
    return True

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
    e = cf.person.delete(group, person_id)
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
    candidates_person_id = []
    candidates_confidence = []

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
    try:
        for i in range(5):
            candidates_person_id.append(candidates_info[i]['candidates'][0]['personId'])
            candidates_confidence.append(candidates_info[i]['candidates'][0]['confidence'])
        if (candidates_person_id[0] == candidates_person_id[1] == candidates_person_id[2] == candidates_person_id[3] == candidates_person_id[4]) and (candidates_confidence[0] >= 0.5) and (candidates_confidence[1] >= 0.5) and (candidates_confidence[2] >= 0.5) and (candidates_confidence[3] >= 0.5) and (candidates_confidence[4] >= 0.5):
            candidate_id = candidates_person_id[0]
            d = {'id': candidate_id}
            with open("person.json","w") as f:
                json.dump(d, f)
                f.write('\n')
            print("{} identified".format(candidate_id))
        else:
            print('The person was not found')
            try:
                os.remove('person.json')
            except FileNotFoundError:
                pass
    except IndexError:
        print('The person was not found')
        try:
            os.remove('person.json')
        except FileNotFoundError:
            pass

def identification_for_simple_add(file_name, group):
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
    candidates_person_id = []
    candidates_confidence = []

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
    try:
        for i in range(5):
            candidates_person_id.append(candidates_info[i]['candidates'][0]['personId'])
            candidates_confidence.append(candidates_info[i]['candidates'][0]['confidence'])
        if (candidates_person_id[0] == candidates_person_id[1] == candidates_person_id[2] == candidates_person_id[3] == candidates_person_id[4]) and (candidates_confidence[0] >= 0.5) and (candidates_confidence[1] >= 0.5) and (candidates_confidence[2] >= 0.5) and (candidates_confidence[3] >= 0.5) and (candidates_confidence[4] >= 0.5):
            candidate_id = candidates_person_id[0]
            d = {'id': candidate_id}
            with open("person.json","w") as f:
                json.dump(d, f)
                f.write('\n')
        else:
            try:
                os.remove('person.json')
            except FileNotFoundError:
                pass
    except:
        try:
            os.remove('person.json')
        except FileNotFoundError:
            pass
