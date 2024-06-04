from PIL import Image

     
class Track:
    def __init__(self,file_name):
        self.imgName = file_name
        
    def imageProcess(self):
        
        # Open lydd track image
        img = Image.open(self.imgName)

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
        return x_raw,y_raw
    
    
    
    
    def check_consec(list_x):
        range_list=list(range(min(list_x), max(list_x)+1))
        if list_x == range_list:
            return True
        else:
            return False
        
        
    
def calculate_race_line(self):
    
    x_raw,y_raw = self.imageProcess()
    
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

