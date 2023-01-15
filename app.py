from flask import Flask,render_template,Response
from camera import Video
from PIL import Image as im
app = Flask(__name__)
emotions=[0]
test_list=[['1']]


@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while(emotions[0]<=20):
        frame=camera.get_frame()
        # print(frame)
        # frame1=im.frombytes(frame[0])
        # print(frame[0])
        emotions[0]+=len(frame[1])
        test_list[0].append(frame[1])
        print(frame[1])
        yield(b'--frame\r\n'
       b'Content-Type:  image/jpeg\r\n\r\n' + frame[0] +
         b'\r\n\r\n')
        
        
def show_res():   
    print(test_list)     
    max = 0
    res = [0]
    if(len(test_list)==0):
        for i in test_list[0]:
            freq = test_list[0].count(i)
            if freq > max:
                max = freq
                res = i
        print("result : "+res)
        link="https://spotify.com"
        return res
    else:
        print(test_list)
        return "----"
        
    # yield(b'--frame\r\n'
    #    b'Content-Type:  text/html\r\n\r\n<a>' +res+
    #      b'</a>\r\n\r\n')
    # out = bytes(res, 'utf-8')
    # yield(b'--frame\r\n'
    #    b'Content-Type:  text/html\r\n\r\n' +out+
    #      b'\r\n\r\n')
    

    
       


@app.route('/video')

def video():
    # out = Video()
    # emotions[0]+=out[0]
    # print(emotions)
    
    print('Hello!!! ')
    print(Video())
    return Response(gen(Video()),
    mimetype='multipart/x-mixed-replace; boundary=frame')

# def video():
#     return emotion_testing()

@app.route('/result')

def result():
    return render_template('results.html',result=show_res())




app.run(debug = True)
