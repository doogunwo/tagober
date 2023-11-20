import pickle
from os import listdir
from os.path import isdir, isfile, join
from tqdm import tqdm
import mtcnn
from sklearn.preprocessing import LabelEncoder
import numpy as np
from flask import Flask, request, jsonify, Response
import mysql.connector
import cv2
import time
from PIL import Image
import os

app = Flask(__name__)
detector = mtcnn.MTCNN()
face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
label_encoder = LabelEncoder()

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234',
    database='sys'
)

models = {}

def get_images_and_labels(name, imagepath):
    images = []
    labels = []
    img = cv2.imread(imagepath, cv2.IMREAD_GRAYSCALE)
   
    # train img = np.asarray(image, dtype=np.uint8)
    # train label = name
   
    faces = face_classifier.detectMultiScale(img, scaleFactor=1.3, minNeighbors=5)

    for (x,y,w,h,) in faces:
        face_roi = img[y:y+h, x:x+w]
        images.append(face_roi)

    labels.append(name)
   
    return images, labels

def trainmodel(name, imagepath):
    images, labels = get_images_and_labels(name, imagepath)

    if len(images) != 0 and len(labels) != 0:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        labels = label_encoder.fit_transform(labels)
        recognizer.train(images, np.array(labels, dtype=np.int32))

        # 모델 저장
        print(name+" train complete\n")
        return recognizer
    else:
        print(f"얼굴 감지 실패. (사용자: {name})\n")
        return None
     
def trains():

    cursor = conn.cursor()
    sql = "select username, imagePath from sys.faceregister"
    cursor.execute(sql)
    
    result = cursor.fetchall()
    print("model load...\n")

    for i in tqdm(result, desc='Processing', unit='item', ncols=100):
        print(i[0]+" train... \n")
        model = trainmodel(i[0],i[1])
        models[i[0]] = model

    print("model train complete\n")
    cursor.close()
    conn.close()
    
     
def face_detector(img, size=0.5):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    if not faces:
        return img, []
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
        roi = img[y:y + h, x:x + w]
        roi = cv2.resize(roi, (200, 200))
    return img, roi

def payment(name,pee,time):
    
    cursor = conn.cursor()
    query = "insert into payment(name,pee,time) values(%s,%s,%s)"
    val = (name,pee,time)
    cursor.execute(query,val)
    conn.commit()
    conn.close()

def run(models,frame):
    # 카메라 열기

        # 얼굴 검출 시도
        image, face = face_detector(frame)
        try:
            min_score = 999  # 가장 낮은 점수로 예측된 사람의 점수
            min_score_name = ""  # 가장 높은 점수로 예측된 사람의 이름

            # 검출된 사진을 흑백으로 변환
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

            # 위에서 학습한 모델로 예측시도
            for key, model in models.items():
                result = model.predict(face)

                if min_score > result[1]:
                    min_score = result[1]
                    min_score_name = key

        except:
            pass

        return min_score_name

@app.route('/start', methods=['POST'])

def start():
    res = "client connect"
    # 결과 전송
    response = {'result': res}
    return Response(response=pickle.dumps(response), status=200, mimetype='application/octet-stream')

@app.route('/update', methods=['POST'])

def update():

    conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234',
    database='sys'
    )
    
    cursor =conn.cursor()
    data = request.json
    who = data.get('who')
    sql = "SELECT username, imagePath FROM sys.faceregister WHERE username=%s"
    cursor.execute(sql, (who,))
    result = cursor.fetchall()

    for i in tqdm(result):
        print(i[0]+" train... \n")
        model = trainmodel(i[0],i[1])
        models[i[0]] = model
    
    print("model train complete\n")
    
    conn.commit()
    conn.close()
    response_data = {'message': 'Update successful'}
    return jsonify(response_data)


@app.route('/video_feed', methods=['POST'])
def video_feed():
        start_time = time.time()
        while(1):
            time.sleep(0.3)
            img_encoded = pickle.loads(request.data)
            img = cv2.imdecode(np.frombuffer(img_encoded, np.uint8), -1)
            # 얼굴 검출 수행
            res=run(models,img)
            current_time = time.time()
            print(res)
            payment(res,"1300",current_time)

            response = {'result': res}
            return Response(response=pickle.dumps(response), status=200, mimetype='application/octet-stream')

if __name__ == '__main__':
    trains()
    app.run(host='192.168.1.192', port=5000,debug=True)


