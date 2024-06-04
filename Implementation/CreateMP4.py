from Functions import create_mp4_from_images
import os

# This file needs the frames folder to be populated first via the GenerateFrames script

cwd = os.path.dirname(os.path.abspath(__file__))

output_filename = cwd + "/output/150.mp4"
frames_folder = cwd + "/frames" 
fps = 150

try:
    create_mp4_from_images(frames_folder, output_filename, fps)

except Exception as e:
    print(f"MP4 could not be created, please check there are .png files in the 'frames' folder\n {e}" )

