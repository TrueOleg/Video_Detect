from imageai.Detection import VideoObjectDetection
import os
import cv2

execution_path = os.getcwd()

video = cv2.VideoCapture("video.mp4")

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
# def forFrame(frame_number, output_array, output_count):
#     # print("FOR FRAME " , frame_number)
#     # print("Output for each object : ", output_array)
#     # print("Output count for unique objects : ", output_count)
#     # print("------------END OF A FRAME --------------")

def forSeconds(second_number, output_arrays, count_arrays, average_output_count):
    print("SECOND : ", second_number)
    # print("Array for the outputs of each frame ", output_arrays)
    # print("Array for output count for unique objects in each frame : ", count_arrays)
    # print("Output average count for unique objects in the last second: ", average_output_count)
    # print("------------END OF A SECOND --------------")

def forFull(output_arrays, count_arrays, average_output_count):
    #Perform action on the 3 parameters returned into the function
    print("Array for the outputs of each frame ", output_arrays)
    print("Array for output count for unique objects in each frame : ", count_arrays)
    print("Output average count for unique objects in the last second: ", average_output_count)

video_detector = VideoObjectDetection()
video_detector.setModelTypeAsYOLOv3()
video_detector.setModelPath(os.path.join(execution_path, "yolo.h5"))
video_detector.loadModel()

video_detector.detectObjectsFromVideo(
    input_file_path=os.path.join(execution_path, "video.mp4"),
    output_file_path=os.path.join(execution_path, "traffic_detected"),
    frames_per_second=fps,
    frame_detection_interval=fps/2,
    per_second_function=forSeconds,
    video_complete_function=forFull,
    minimum_percentage_probability=30
)