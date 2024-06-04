from statistics import mean 
import copy 
from PIL import Image
import os, shutil
import re
import imageio
from moviepy.editor import ImageSequenceClip
import math

def imageProcess(imgName):
        
    # Open lydd track image
    img = Image.open(imgName)

    # convert to RGB values
    img.convert('RGB')

    # Find pixel width and height
    width, height = img.size

    # set up variables
    tol = 10
    x_raw = []
    y_raw = []
    rgb = [0, 0, 0]

    # Find coordinates of track data by filtering out light pixels according to some tolerance
    for i in range(0,width):
        for j in range(0,height):   
            
            rgb = img.getpixel((i,j))
            val = sum(rgb)
            
            if val < 1020 - (20*tol):
                x_raw.append(i)
                y_raw.append((height-j))
            pass
        pass
    pass
    return x_raw,y_raw,img

def check_consec(list_x):
    range_list=list(range(min(list_x), max(list_x)+1))
    if list_x == range_list:
        return True
    else:
        return False

def calculate_race_line(x_raw,y_raw):
    
    # Find unqiue values of x
    x_set = list(set(x_raw))

    # Choose line to determine start and end point
    start_end_line = 4 # 0 < x <12 

    # defining variables
    idx=0
    temp = []
    y1_lower =[]
    y1_upper =[]
    y1_idx =[]

    y2_start =[]
    y2_end = []

    y1_start_upper = []
    y1_start_lower = []
    y1_start_idx = []

    y1_end_upper =[]
    y1_end_lower =[]
    y1_end_idx = []


        

    # Scan a list y values based on a x value, check if it is a consectuive line:
    #
    # If YES then select two lines 't' indices from the start and end index, find mean of
    # y values and save this as y2_start and y2_end.
    #
    # If NO then find where line consec breaks and use this idx to calculate the 
    # mean of the two broken lines. This case gives two y coords for every x coord,
    # an 'upper' and a 'lower' Y value. 

    for i in range(len(x_set)):
        
        # Generates a list of y0-yj for x[i]
        for j in range(len(x_raw)):
            if x_set[i] == x_raw[j]:
                temp.append(y_raw[idx])
                idx=idx+1
            pass
        pass
        
        temp.sort() # Puts y values in ascending order
        
        if check_consec(temp): # Checks if sorted y0-yj for x[i] is consecutive
            if i == start_end_line:    # Checks to see if x idx is lower threshold
                y2_start = mean(temp)  # save average y_start value   
                y2_start_idx = i       # Save index of y value
                
            elif i == len(x_set)-start_end_line-1: # Checks to see if x idx is lower threshold
                y2_end = mean(temp)          # Save average y_end value
                y2_end_idx = i               # Save idx of y value
            
            elif start_end_line < i < 12:
                y1_start_upper.append(y2_start + round((78.5-y2_start)*(i-start_end_line+1)/(13-start_end_line)))
                y1_start_lower.append(y2_start - round((y2_start-47.5)*(i-start_end_line+1)/(13-start_end_line)))
                y1_start_idx.append(i)
                
            elif len(x_set)-12 <= i < len(x_set)-start_end_line :
                y1_end_lower.append(143.5 + round((156-143.5)*(i-406-start_end_line)/(13-start_end_line)))
                y1_end_upper.append(143.5 - round((143.5-130.5)*(i-406-start_end_line)/(13-start_end_line)))
                y1_end_idx.append(i)
                
            pass
        
        else:  # if sorted y0-yj for x[i] are not consecutive  
            for i1 in range(len(temp)-1):                       # loop over the length of y0-yj   
                if temp[i1] +1 != temp[i1+1]:                   # finds the point the set is not consecutive   
                    y1_lower.append(mean(temp[0:i1]))           # average upper and lower Y sets
                    y1_upper.append(mean(temp[i1+1:len(temp)])) # append average value to y1_upper and y1_lower
                    y1_idx.append(i)                            # Keep track of idx where not consecutive
                pass
            pass
        pass
                                
        temp = []   # Reset value of temp
    pass

    # Attaching the mean Y values from the end and start to both upper and lower sets of data
    y1 = [y2_start] + y1_start_lower + y1_lower + y1_end_lower + [y2_end]
    y2 = [y2_start] + y1_start_upper + y1_upper + y1_end_upper + [y2_end]



    # Removing corresponding x value for unused y values and adding the start and end x vals
    x = x_set[y1_start_idx[0]:y1_start_idx[-1]+1]  + x_set[y1_idx[0]:y1_idx[-1]+1] + x_set[y1_end_idx[0]:y1_end_idx[-1]+1]
    x = [x_set[y2_start_idx]] + x + [x_set[y2_end_idx]]


    # concatenating top and bottom sets of data to single list
    z = copy.deepcopy(x)
    z.reverse()
    x = x + z
    z = copy.deepcopy(y1)
    z.reverse()
    y = y2 + z

    return x,y

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def create_gif_from_images(input_folder, output_gif_path, duration):
    """
    Create a GIF animation from PNG images in a folder.

    Args:
        input_folder (str): The path to the folder containing PNG images.
        output_gif_path (str): The path where the GIF animation will be saved.
        duration (int): The duration (in milliseconds) for each frame in the GIF.

    Returns:
        None
    """
    image_files = [f for f in os.listdir(input_folder) if f.endswith('.png')]
    image_files.sort(key=natural_keys)

    if not image_files:
        print("No PNG images found in the input folder.")
        return

    images = [Image.open(os.path.join(input_folder, image)) for image in image_files]

    # Save the images as a GIF animation
    images[0].save(
        output_gif_path,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=0
    )
    print(f"GIF animation saved to {output_gif_path}")




    #plotting old method with pause
    # fig, axs = plt.subplots(2)
    # axs[0].imshow(img)

    # axs[1].scatter(x_raw,y_raw,color = 'black')

    # for i in range(0,len(x)):
    #     axs[1].scatter(x[i],y[i],color = 'white',s=2)
    #     plt.pause(0.00000001)
        

        
    # plt.show()

def create_mp4_from_images(input_folder, output_mp4_path, fps=30):
    """
    Create an MP4 video from PNG images in a folder.

    Args:
        input_folder (str): The path to the folder containing PNG images.
        output_mp4_path (str): The path where the MP4 video will be saved.
        fps (int): Frames per second for the video.

    Returns:
        None
    """

    image_files = [f for f in os.listdir(input_folder) if f.endswith('.png')]
    image_files.sort(key=natural_keys)

    if not image_files:
        print("No PNG images found in the input folder.")
        return

    images = [imageio.imread(os.path.join(input_folder, image)) for image in image_files]
    clip = ImageSequenceClip(images, fps=fps)

    # Save the video as an MP4 file
    clip.write_videofile(output_mp4_path, fps=fps)
    print(f"MP4 video saved to {output_mp4_path}")
    
def filter_data(x_data,y_data,skip):
    x_filtered = []
    y_filtered = []
    for i in range(0,len(x_data),skip):
        x_filtered.append(x_data[i])
        y_filtered.append(y_data[i])
    pass 
    return x_filtered, y_filtered
    
def shift_left(lst, n):
    """Shifts the lst over by n indices

    >>> lst = [1, 2, 3, 4, 5]
    >>> shift_left(lst, 2)
    >>> lst
    [3, 4, 5, 1, 2]
    """
    if n < 0:
        raise ValueError('n must be a positive integer')
    if n > 0:
        #lst.insert(0, lst.pop()) # shift one place
        lst.append(lst.pop(0))
        shift_left(lst, n-1)  # repeat

def find_cumulative_diff(x,y):
    c_diff = []
    temp = 0
    for i  in range(len(x)-1):
        x_diff = abs(x[i+1]-x[i])
        y_diff = abs(y[i+1]-y[i])
        diff = math.sqrt(x_diff*x_diff + y_diff*y_diff)
        temp = temp + diff
        c_diff.append(temp)
        pass
    c_diff = [0] + c_diff    
    return c_diff

def find_distance_idx(d_vec,distance):
    idx = []
    for i in range(len(d_vec)):
        for j in range(len(distance)-1):
            if distance[j] <= d_vec[i] < distance[j+1]:
                idx.append(j)
                pass
            pass
        pass
                
    return idx

# Find x and y value for each distance point
def find_xy_for_d_vec(d_vec,distance,x_data,y_data):
    idx = []
    x = []
    y = []  
    for i in range(len(d_vec)):
        for j in range(len(distance)-1):
            if distance[j] <= d_vec[i] < distance[j+1]:
                x1 = x_data[j]
                y1 = y_data[j]
                x2 = x_data[j+1]
                y2 = y_data[j+1]
                
                y_diff = y2-y1
                x_diff = x2-x1
                
                pheta = math.atan(abs(y_diff)/abs(x_diff))
                d = d_vec[i] - distance[j]
                
                xd = round(d * math.cos(pheta))
                yd = round(d * math.sin(pheta))
                
                if y_diff >= 0 and x_diff >=0:
                    x.append(x1 + xd)
                    y.append(y1 + yd)
                elif y_diff < 0 and x_diff <=0:
                    x.append(x1 - xd)
                    y.append(y1 - yd)
                elif y_diff >= 0 and x_diff <=0:
                    x.append(x1 - xd)
                    y.append(y1 + yd)
                elif y_diff < 0 and x_diff >=0:
                    x.append(x1 + xd)
                    y.append(y1 - yd)
                pass
            pass
        pass
                
    return x,y

def removeFrames(folder='/home/bailey/Documents/GoKart_Sim_V2/plotting/frames'):

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
            
            
            
            