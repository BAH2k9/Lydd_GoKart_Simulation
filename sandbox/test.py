import functions as f
import matplotlib.pyplot as plt
import pandas as pd
import os


# Find x, y coordinates from RGB values
x_raw,y_raw,img = f.imageProcess("Lydd_Track.png")

# Find the race line for the track 
x, y = f.calculate_race_line(x_raw,y_raw)

# Take every frame x =15
x_f,y_f = f.filter_data(x,y,15)

# Shift to find start line
f.shift_left(x_f,4)
f.shift_left(y_f,4)

# Append start point to end of vectors
x_f = x_f + [x_f[0]]
y_f = y_f + [y_f[0]]

# Find cumulative distance between each set of points
distance = f.find_cumulative_diff(x_f,y_f)



# --------------------- Set up simulation -----------------------
data = pd.read_csv("Lydd_Laptimes.csv")
driver_names = data.columns.values.tolist()
lap_distance = 1040
res = 3    # Higher is more frames
num_of_laps = 3 # Max is 34

lap_times = []

# extract lap times
for name in driver_names:
    lap_times.append(data[name][:num_of_laps])
    pass

# # Set up distance vector based on speed and resolution
x_driver = [[] for _ in range(len(driver_names))]
y_driver = [[] for _ in range(len(driver_names))]


for i in range(len(lap_times)):
    for lap_time in lap_times[i]:
        if str(lap_time) != 'nan':
            speed = lap_distance/lap_time
            t_vec = [t/res for t in range(0,round(lap_time*res))]
            d_vec = [speed*t for t in t_vec]
            
            temp_x,temp_y = f.find_xy_for_d_vec(d_vec,distance,x_f,y_f)
            
            x_driver[i].extend(temp_x)
            y_driver[i].extend(temp_y)
            
        
# Transpose lists for plotting
x_driver = list(map(list, zip(*x_driver)))
y_driver = list(map(list, zip(*y_driver)))

# Define dictionary of colours for plotting 
c = {'red':'#df4717','orange':'#ea8f8f', 'green':'#8feab6','blue': '#1bb2c7','purple':'#9b1bc7'}

frames =[]
for i in range(10,11):#len(x_driver)): 
    
    plt.figure(figsize=(6, 4))
    plt.axes().set_aspect('equal', 'box')
    plt.ylim(-50,250)
    plt.axis('off')
    
    plt.scatter(x_raw,y_raw,color='black')
    
    
    plt.scatter(x_driver[i],y_driver[i],color=list(c.values()))

    if i == 10:
        plt.legend(['D1','D2','D3','D4','D5'])
    plt.pause(0.5)
pass

plt.show()





# for i in range(1):#len(x_driver)): 
    
#     plt.figure(figsize=(6, 4))
#     plt.axes().set_aspect('equal', 'box')
#     plt.ylim(-50,250)
#     plt.axis('off')
    
#     plt.scatter(x_raw,y_raw,color='black')
    
    
#     x = x_driver[i]
#     y = y_driver[i]
    
#     for j in range(0,len(x)-1):
#         plt.scatter(x[j],y[j],color=list(c.values())[j])

    
#     plt.legend(['D1','D2','D3','D4','D5'])
#     plt.pause(0.5)
# pass