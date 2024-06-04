import functions as f
import pandas as pd
import os


cwd = os.path.dirname(os.path.abspath(__file__))

# Find x, y coordinates from RGB values
x_raw,y_raw,img = f.imageProcess( cwd + "/Lydd_Track.png")

# Find the race line for the track 
x, y = f.calculate_race_line(x_raw,y_raw)

# Take every frame x, y = N 
N = 15
x_f,y_f = f.filter_data(x,y,N)

# Shift to find start line
f.shift_left(x_f,4)
f.shift_left(y_f,4)

# Append start point to end of vectors
x_f = x_f + [x_f[0]]
y_f = y_f + [y_f[0]]

# Find cumulative distance between each set of points
distance = f.find_cumulative_diff(x_f,y_f)



# --------------------- Set up simulation -----------------------
data = pd.read_csv(cwd + "/Lydd_Laptimes.csv")
driver_names = data.columns.values.tolist()
lap_distance = 1040
res = 3   # Higher is more frames
num_of_laps = 34 # Max is 34

lap_times = []

# extract lap times
for name in driver_names:
    lap_times.append(data[name][:num_of_laps])
    pass

# # Set up distance vector based on speed and resolution
x_driver = [[] for _ in range(len(driver_names))]
y_driver = [[] for _ in range(len(driver_names))]

num_points_counter= [[] for _ in range(len(driver_names))]
temp = 0

for i in range(len(lap_times)):
    for lap_time in lap_times[i]:
        if str(lap_time) != 'nan':
            speed = lap_distance/lap_time
            t_vec = [t/res for t in range(0,round(lap_time*res))]
            d_vec = [speed*t for t in t_vec]
            
            temp_x,temp_y = f.find_xy_for_d_vec(d_vec,distance,x_f,y_f)
            
            x_driver[i].extend(temp_x)
            y_driver[i].extend(temp_y)
            
            num_points_counter[i].append(len(temp_x))

   

            
        
# Transpose lists for plotting
x_driver = list(map(list, zip(*x_driver)))
y_driver = list(map(list, zip(*y_driver)))

# Define dictionary of colours for plotting 
c = {'red':'#df4717','orange':'#ea8f8f', 'green':'#8feab6','blue': '#95d9ff','purple':'#9b1bc7'}


# --------------------- Save Frames -----------------------
# Uncomment this section to generate and save the frames generated
# import matplotlib.pyplot as plt
# f.removeFrames()           
# frames =[]
# for i in range(len(x_driver)): 
    
#     plt.figure(figsize=(6, 4))
#     plt.axes().set_aspect('equal', 'box')
#     plt.ylim(-50,250)
#     plt.axis('off')
#     plt.scatter(x_raw,y_raw,color='black')
    
#     x = x_driver[i]
#     y = y_driver[i]
    
#     # Plot points id=ndividualy to allow color control
#     for j in range(len(x)):
#         plt.scatter(x[j],y[j])#,\
#                     #color=list(c.values())[j])      #['^','p','D','s','*']
    
#     plt.legend(['Alan','Taylor','Ben','Bailey','Jake'])
    
#     temp = 'frame_' + str(i)
#     frames.append(temp)
#     plt.savefig('frames/'+temp,bbox_inches='tight')
#     plt.cla()



# Create animation
input_folder = cwd + "/frames"  
output_mp4_path = cwd + "/sim.mp4"
fps = 120
# f.create_mp4_from_images(input_folder,output_mp4_path,fps)



#-----------------------------------
# Plotting track image, track coordinates/race line
# fig, axs = plt.subplots(4)
# axs[0].imshow(img)

# axs[1].scatter(x_raw,y_raw,color = 'black')
# axs[1].scatter(x_driver1[0:num_points1[0]],y_driver1[0:num_points1[0]],color=c.get('white'),s=2)

# axs[2].scatter(x_raw,y_raw,color = 'black')
# axs[2].scatter(x_driver2[0:num_points2[0]],y_driver2[0:num_points2[0]],color=c.get('orange'),s=2)

# axs[3].scatter(x_raw,y_raw,color = 'black')
# axs[3].scatter(x_driver2[0:num_points2[0]],y_driver2[0:num_points2[0]],color=c.get('green'),s=2)

# plt.show()



''' Legacy code

# for i,lap_time in enumerate(lap_times):
#     speed = lap_distance/lap_time
#     t_vec = [t/res for t in range(0,(lap_time*res))]
#     d_vec = [speed*t for t in t_vec]
    
#     temp_x,temp_y = f.find_xy_for_d_vec(d_vec,distance,x_f,y_f)
    
#     x_driver.extend(temp_x)
#     y_driver.extend(temp_y)



# propagate forward the lap times
# max_len = len(max(lap_times_raw,key=len))
# lap_times =[]

# for lap_time in lap_times_raw:
    
#     temp = [x for x in lap_time if str(x) != 'nan']
#     len_to_append = max_len - len(temp)
#     final_val = temp[-1]
#     temp.extend([final_val]*len_to_append)
#     lap_times.append(temp)


    '''