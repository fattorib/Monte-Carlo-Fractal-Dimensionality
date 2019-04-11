#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 11:33:18 2018
This code will estimate the fractal dimension of the Koch Snowflake using Monte-Carlo
methods. It will then plot either the change in dimension over number of iterates or the boxes that cover
our fractal

@author: benjamin
"""

import numpy as np
import matplotlib.pyplot as plt

#Data file we are reading from
plot = plt.imread('Koch_snowflake.png')
#plt.imshow(plot)
size = len(plot[0])

print (size)
single_step = 1/size

#Function to generate random coordinates
def random_coordinates(size,plot):
    #Size represents the size of our coordinate array
    x = np.random.randint(2,size-2)
    y = np.random.randint(2,size-2)
    return x,y

#Function to check distance between 2 pairs of (x,y) coordinates
def distance(a,b,c,d):
    return np.sqrt((a-c)**2 + (b-d)**2)

#Function to check if a square of midpoint (x,y) and side length 2k overlaps
#with any squares we have by determing the distance between their midpoints
def center_checker(x,y,centers_x,centers_y,k):
    if len(centers_x) == 0:
        return 1
    else:
        length = len(centers_x)
        x_ar = np.full(length,x)
        y_ar = np.full(length,y)
        x_vals = (centers_x - x_ar)**2
        y_vals = (centers_y - y_ar)**2
        distance = np.sqrt(x_vals + y_vals)
        if np.amin(distance) < 2*np.sqrt(2*(k**2)):
            #This will underestimate number of points
            return 0
        else:
            return 1

#This will be the main function to calculate our fractal dimension
def dimension_check_better(N,size,plot,k):
    """
    Input: N,size,plot,k
    N: number of iterations to run through
    size: size of our plot
    plot: input data set, in this case it will be the .png file read by python
    k: distance (in the array) for the box side length
    """
    
    #Array to store centers of boxes that cover our set
    centers_x = np.empty(0)
    centers_y = np.empty(0)
    
    #Stores dimension over time
    dimension = np.empty(0)
    
    #These are what we use to keep a running total of our data
    sum = 0
    points_plotted = 0
    total_pts_used = 0
    epsilon = single_step * 2*k
    
    
    for i in range(N):
        #Calculate dimension at current step
        dimension = np.append(dimension,[np.log(sum+1)/np.log(1/epsilon)])
        
        #Generate random coordinates
        x,y = random_coordinates(size,plot)
        
        #Check if the box with center (x,y) overlaps any of our previous boxes
        val = center_checker(x,y,centers_x,centers_y,k)
        
        if val == 0:
            #We have an overlap
           pass
            
        else:
            #no overlap
            total_pts_used +=1 
            #Append to list of good centers
            
            centers_x = np.append(centers_x,[x])
            centers_y = np.append(centers_y,[y])
            
            #Checking mean colour values for an array of pre-specified size
            data = plot[x-k:x+k,y-k:y+k]
            average = np.mean(data)
            #print ('Average colour value is', average)
            if average == 1:
                #We are totally inside or outside
                pass
            
            else:
                #Plot our box, uncomment if you want the diagram of the plot
                #rectangle = plt.Rectangle((y-k, x-k), 2*k, 2*k, linewidth=1,edgecolor='r',facecolor='none')
                #plt.gca().add_patch(rectangle)
                points_plotted += 1
                sum += 1
        
    
    #General Data return
    return np.log(sum)/np.log(1/epsilon), total_pts_used, points_plotted, dimension


#Parameters for calculations
N = 7500
k = 1
value = dimension_check_better(N,size,plot,k)
print ('Dimension is', value[0],'for N=',N,'percent of points used is',100*(value[1])/N)
actual = 1.261859507
print ('difference from the actual value is', actual - value[0])
print ('The number of points plotted is', value[2])

#This will be used to plot the fractal with the boxes covering it, uncomment this as well as the code above in the function to show this
#plt.imshow(plot)



#Plot to show change in dimension estimate over iterations, comment this part out if you want the above part to show
real_dimension = np.array([actual for i in range(0,N)])
plt.plot(value[3],label = 'Estimated dimension')
plt.plot(real_dimension, 'r--', label = 'Dimension (d = 1.2618)')
plt.title('Number of iterations vs. esitmated dimension (Koch Snowflake)')
plt.xlabel('Number of iterations')
plt.ylabel('Dimension estimate')
plt.legend()
plt.show()














