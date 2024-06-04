import math
import matplotlib.pyplot as plt


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


# def find_distance_idx(d_vec,distance):
#     idx = []
#     for i in range(len(d_vec)):
#         for j in range(len(distance)-1):
#             if distance[j] <= d_vec[i] < distance[j+1]:
#                 idx.append(j)
#                 pass
#             pass
#         pass
                
#     return idx



# Find x and y value for each distance point
def find_x_y_for_d_vec(d_vec,distance,x_data,y_data):
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
                
                xd = d * math.cos(pheta)
                yd = d * math.sin(pheta)
                
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
            


x = [5,7,10,13,10,7,5]
y = [5,7,7,5,3,3,5]

# Cumulative diff fro x y points
distance = find_cumulative_diff(x,y)

# distance vector based on avergare speed
d_vec = [0, 2.1, 3.9, 6, 10,13,15,17]


x_driver,y_driver = find_x_y_for_d_vec(d_vec,distance,x,y)

print('distance = ' + str(distance))
print('d_vec = ' + str(d_vec))
print('x = ' + str(x_driver))
print('y = ' + str(y_driver))

# Plotting track image, track coordinates/race line

plt.plot(x,y)
plt.scatter(x,y)
plt.scatter(x_driver,y_driver,color = 'black')  
plt.show()




            
