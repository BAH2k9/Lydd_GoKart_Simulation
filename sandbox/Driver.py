import math

class Driver:
    def __init__(self,lap_times,x_race_line,y_race_line,cumulative_distance):
        
        self.lap_times = lap_times
        
        self.lap_distance = 1040 
        
        self.x_race_line = x_race_line
        
        self.y_race_line = y_race_line
        
        self.distance = cumulative_distance
        
        
        
    def find_xy_for_d_vec(self,d_vec,distance,x_data,y_data):
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
    
    
    
    def find_position(self):
        
        x_driver = []
        y_driver = []
        num_points = []
        res = 5
        
        for i,lap_time in enumerate(self.lap_times):
            speed = self.lap_distance/lap_time
            t_vec = [t/res for t in range(0,(lap_time*res))]
            d_vec = [speed*t for t in t_vec]
            
            temp_x,temp_y = self.find_xy_for_d_vec(d_vec,self.distance,self.x_race_line,self.y_race_line)
            
         
            num_points.append(len(temp_x))
            x_driver.extend(temp_x)
            y_driver.extend(temp_y)
            
                