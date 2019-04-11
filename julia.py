#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 11:33:18 2018
This code will estimate the fractal dimension of the dendrite julia set using Monte-Carlo
methods.  It will then plot either the change in dimension over number of iterates or the boxes that cover
our fractal

This code will also create and plot the Julia set. 
@author: benjamin
"""

import numpy as np
import matplotlib.pyplot as plt


"""
Code to generate and plot the Julia Set, commented out as we have pre-made a set
using this code

"""


"""
#Function for the julia set
def julia(z,c):
    return z**2 + c



def iterator(i,c,z):
    #Iterates through values for i steps or until the value escapes
    it = 0
    val = julia(z,c)
    while it < i:
        
        if np.abs(val) > 2:
            #Value too big and not in our set
            return (False, it)
            #it =i
        else:
            val = julia(val,c)
            it += 1
            
    #if np.abs(val) >= 2:
        #Value will escape to infinity
        
    #else:
    return (val,0)


#number of iterates and the size of our plot
it = 300
size = 500
c = 1j
#Default Coordinates

#Create coordinates for which we will analyze the values for 
coordinates = [x+1j*y for x in np.linspace(-1.5,1.5,size) for y in np.linspace(-1.5,1.5,size)]
new = np.reshape(coordinates, (size,size))


plot = np.empty([size,size])

for x in range(len(new[0])):
    for y in range(len(new[0])):
        z = new[x,y]
        value = iterator(it,c,z)
        if value[0] == False:
            plot[x,y] = value[1]
            
        else:
            plot[x,y] =10
            
   
plt.xticks([])
plt.yticks([])

#Save the data to be analyzed later
#np.savetxt('julia_extra.csv',plot,delimiter=",")
#plt.imshow(plot,'inferno')
"""


#Load our pre-made Julia Set data

plot = np.loadtxt('julia.csv',delimiter=",")
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
         #Generate random coordinates
        x,y = random_coordinates(size,plot)
        
        #Check if the box with center (x,y) overlaps any of our previous boxes
        val = center_checker(x,y,centers_x,centers_y,k)
        
        #Calculate dimension at current stock
        dimension = np.append(dimension,[np.log(sum+1)/np.log(1/epsilon)])
        
        if val == 0:
            #We have an overlap
           pass
            
        else:
            #no overlap
            total_pts_used +=1 
            centers_x = np.append(centers_x,[x])
            centers_y = np.append(centers_y,[y])
            #Checking mean colour values for an array of pre-specified size
            data = plot[x-k:x+k,y-k:y+k]
            average = np.mean(data)
            if average <=15.5:
                #We are totally outside the set
                pass
                
            else:
                #Plot our box, uncomment if you want the diagram of the plot
                #rectangle = plt.Rectangle((y-k, x-k), 2*k, 2*k, linewidth=1,edgecolor='r',facecolor='none')
                #plt.gca().add_patch(rectangle)
                points_plotted += 1
                sum += 1
        
    
    #General data return    
    return np.log(sum)/np.log(1/epsilon), total_pts_used, points_plotted, dimension
    
    

N = 7500
k = 1
value = dimension_check_better(N,size,plot,k)
print ('dimension is maybe uh', value[0],'for N=',N,'percent of points used is',100*(value[1])/N)
actual = 1.2
print ('difference from the actual value is', actual - value[0])
print ('The number of points plotted is', value[2])

#This will be used to plot the fractal with the boxes covering it, uncomment this as well as the code above in the function to show this
#plt.imshow(plot)


#Plot to show change in dimension estimate over iterations, comment this part out if you want the above part to show
real_dimension = np.array([actual for i in range(0,N)])
plt.plot(value[3],label = 'Estimated dimension')
plt.plot(real_dimension, 'r--', label = 'Dimension (d = 1.2)')
plt.title('Number of iterations vs. esitmated dimension (Dendrite Julia Set)')
plt.xlabel('Number of iterations')
plt.ylabel('Dimension estimate')
plt.legend()
plt.show()























