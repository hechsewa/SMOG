from __future__ import division 
from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg as LA
from matplotlib.animation import FuncAnimation



#algorytm SimpleKriging
#zrodło: https://sourceforge.net/p/geoms2/wiki/Kriging/

#1) Check the distance between node and samples.
#2) Check the angle between node and sample.
#3) Calculate the M array for variogram values between node and sample.
#4) Get the K matrix with the variogram values of all points envolved.
#5) Solve the system K*w=M. This will give you the weights.
#6) Multiply the weights by the result beetween values minus the mean of values (it could be an user input). Sum the result.
#7) Subtract the mean of values to that sum and you have the value for the node.
#8) Repeat the steps for all nodes.

def SimpleKriging(x,y,v,variogram,grid):

    cov_angles = np.zeros((x.shape[0],x.shape[0]))
    cov_distances = np.zeros((x.shape[0],x.shape[0]))
    K = np.zeros((x.shape[0],x.shape[0]))
    for i in range(x.shape[0]-1):
        cov_angles[i,i:]=np.arctan2((y[i:]-y[i]),(x[i:]-x[i]))
        cov_distances[i,i:]=np.sqrt((x[i:]-x[i])**2+(y[i:]-y[i])**2)
    for i in range(x.shape[0]):
        for j in range(x.shape[0]):
            if cov_distances[i,j]!=0:
                amp=np.sqrt((variogram[1]*np.cos(cov_angles[i,j]))**2+(variogram[0]*np.sin(cov_angles[i,j]))**2)
                K[i,j]=v[:].var()*(1-np.e**(-3*cov_distances[i,j]/amp))
    K = K + K.T

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
             distances = np.sqrt((i-x[:])**2+(j-y[:])**2)
             angles = np.arctan2(i-y[:],j-x[:])
             amplitudes = np.sqrt((variogram[1]*np.cos(angles[:]))**2+(variogram[0]*np.sin(angles[:]))**2)
             M = v[:].var()*(1-np.e**(-3*distances[:]/amplitudes[:]))
             W = LA.solve(K,M)
             grid[i,j] = np.sum(W*(v[:]-v[:].mean()))+v[:].mean()
    return grid

def retX(): #Zwraca punkty pomiarowe na osi x (przyblizone wartosci)
    x = array([58, 58, 57, 47, 50, 40, 43, 34, 20, 24, 17])
    return x
def retY(): #Zwraca punkty pomiarowe  a osi y
    y = array([50, 42, 25, 24, 20, 21, 17, 33, 34, 38, 25])
    return y

def updateV(): #updatuje nowe wartosci smogu
    #v = array([94, 61, 81, 70, 76, 78, 97, 70, 74, 63, 67]) #PM10 20.11 g.21.00
    v = np.random.randint(0,100,11)  #dla losowych
    return v  
    
def update(aC): #Pobiera nową wartość smogu, ponownie stosuje algorytm Kriging i rysuje nowy wykres
    x=retX()
    y=retY()
    v = updateV()
    grid = np.zeros((75,60),dtype='float32') 
    grid = SimpleKriging(x,y,v,(50,30),grid)
    plt.imshow(grid.T,origin='lower',interpolation='gaussian',cmap='jet')
    plt.scatter(x,y,c=v,cmap='jet',s=120)
    plt.xlim(0,grid.shape[0])
    plt.ylim(0,grid.shape[1])
    plt.grid()
    


def main():
    fig = plt.figure()
    ani = FuncAnimation(fig, update, interval=3, save_count=3) #uruchomienie animacji
    #jak zrobic zeby nie byla powtarzana w nieskonczonosc?
    plt.show()
        


if __name__ == "__main__":
    main()
