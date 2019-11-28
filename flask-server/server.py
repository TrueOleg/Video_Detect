# Create API of ML model using flask

'''
This code takes the JSON data while POST request an performs the prediction using loaded model and returns
the results in JSON format.
'''

# Import libraries
import numpy as np
from flask import Flask, request, jsonify, send_file, make_response
import pickle
from flask_cors import CORS
import base64
from PIL import Image
from io import BytesIO
import re, time, base64  
import json
from imageai.Detection import VideoObjectDetection
import os
import cv2
import pandas as pd

 
execution_path = os.getcwd()

app = Flask(__name__)
CORS(app)

objects = 2
# Load the model
# model = pickle.load(open('model.pkl','rb'))
def getI420FromBase64(codec, image_path=""):
    base64_data = re.sub('^data:video/.+;base64,', '', codec)
    byte_data = base64.b64decode(base64_data)
    video_data = BytesIO(byte_data)
    video = Image.open(video_data)
    t = time.time()
    video.save('1' + '.mp4', "MP4V")
    
@app.route('/api/video',methods=['POST'])
def predict():
    
    data = request.get_json(force=True)
    body = data.get('data')
    filew = body.get('file')
    
    print(filew)
    decoded_string = base64.b64decode(filew)
    with open('1.mp4', 'wb') as wfile:
      wfile.write(decoded_string)

    video = cv2.VideoCapture("1.mp4")

    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    fps = 0

    if int(major_ver)  < 3 :
        fps = round(video.get(cv2.cv.CV_CAP_PROP_FPS))
        print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
    else :
        fps = round(video.get(cv2.CAP_PROP_FPS))
        print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

    video.release();   


    # def incr():
    #     global varib
    #     varib = 'bbbbbbbb'
    
    

    # incr()

    # print("varib", varib)

    def forSeconds(second_number, output_arrays, count_arrays, average_output_count):
        print("SECOND : ", second_number)
        # print("Array for the outputs of each frame ", output_arrays)
        # print("Array for output count for unique objects in each frame : ", count_arrays)
        # print("Output average count for unique objects in the last second: ", average_output_count)
        # print("------------END OF A SECOND --------------")

    def forFull(output_arrays, count_arrays, average_output_count):
        #Perform action on the 3 parameters returned into the function
        # print("Array for the outputs of each frame ", output_arrays)
        # print("Array for output count for unique objects in each frame : ", count_arrays)
        # print("Output average count for unique objects in the last second: ", average_output_count)
        global objects
        objects = output_arrays
        

    video_detector = VideoObjectDetection()
    video_detector.setModelTypeAsYOLOv3()
    video_detector.setModelPath(os.path.join(execution_path, "yolo.h5"))
    video_detector.loadModel()

    video_detector.detectObjectsFromVideo(
        input_file_path=os.path.join(execution_path, "1.mp4"),
        output_file_path=os.path.join(execution_path, "traffic_detected"),
        frames_per_second=fps,
        per_second_function=forSeconds,
        video_complete_function=forFull,
        minimum_percentage_probability=30
    )

    
    def convert_avi_to_mp4(avi_file_path, output_name):
        os.popen("ffmpeg -i '{input}' -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 './static/{output}.mp4'".format(input = avi_file_path, output = output_name))
        return True

    convert_avi_to_mp4("traffic_detected.avi", "converted")
     

    
    json_dump = pd.Series(objects).to_json(orient='values')

    print("==============", json_dump)

    return json_dump
    

if __name__ == '__main__':
    app.run(port=5000, debug=True)
