import os

def convert_avi_to_mp4(avi_file_path, output_name):
    os.popen("ffmpeg -i '{input}' -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 './static/{output}.mp4'".format(input = avi_file_path, output = output_name))
    os.popen("taskkill /im ffmpeg.exe")
    return True

convert_avi_to_mp4("fast-speed.avi", "converted")