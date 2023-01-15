import cv2

import cv2
import numpy as np
from keras.models import model_from_json
emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
emotions_output=[]

# load json and create model
json_file = open('model/emotion_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
emotion_model = model_from_json(loaded_model_json)

# load weights into new model
emotion_model.load_weights("model/emotion_model.h5")
print("Loaded model from disk")



class Video(object):
    def __init__(self):


        self.video=cv2.VideoCapture(0)



    def __del__(self):
        self.video.release()
    
    
    
    def get_frame(self):
        ret,frame=self.video.read()
        

        frame = cv2.resize(frame, (1280, 720))
        face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)



        # detect faces available on camera
        num_faces = face_detector.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        # take each face available on the camera and Preprocess it
        for (x, y, w, h) in num_faces:
            cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (0, 255, 0), 4)
            roi_gray_frame = gray_frame[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)

            # predict the emotions
            emotion_prediction = emotion_model.predict(cropped_img)
            maxindex = int(np.argmax(emotion_prediction))
            cv2.putText(frame, emotion_dict[maxindex], (x+5, y-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            emotions_output.append(emotion_dict[maxindex])
        # faces=faceDetect.detectMultiScale(frame, 1.3, 5)


        # for x,y,w,h in faces:
        #     x1,y1=x+w, y+h
        #     cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,255), 1)
        #     cv2.line(frame, (x,y), (x+30, y),(255,0,255), 6) #Top Left
        #     cv2.line(frame, (x,y), (x, y+30),(255,0,255), 6)

        #     cv2.line(frame, (x1,y), (x1-30, y),(255,0,255), 6) #Top Right
        #     cv2.line(frame, (x1,y), (x1, y+30),(255,0,255), 6)

        #     cv2.line(frame, (x,y1), (x+30, y1),(255,0,255), 6) #Bottom Left
        #     cv2.line(frame, (x,y1), (x, y1-30),(255,0,255), 6)

        #     cv2.line(frame, (x1,y1), (x1-30, y1),(255,0,255), 6) #Bottom right
        #     cv2.line(frame, (x1,y1), (x1, y1-30),(255,0,255), 6)


        
    
        ret,jpg=cv2.imencode('.jpg',frame)
        # row, column, depth = jpg.tobytes().shape
        # print([row,column,depth])
        out=[]
        out.append(jpg.tobytes())
        out.append(emotions_output)
        
        return out
        return jpg.tobytes()