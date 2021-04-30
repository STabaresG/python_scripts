import numpy as np
import matplotlib.pyplot as plt
import random
from random import uniform
from numpy import linalg


# Define class with their instances, position, velocity and status

class people:


  def __init__(self, x, y, vx, vy, r, H, S, D):

    # Status
    
    self.healthy = H
    self.sick = S
    self.recovered = D

    # Position
    
    self.X = x
    self.Y = y

    # Velocity
    self.VX = vx
    self.VY = vy

    # Radio
    self.R = r

 #  Function for position evolution  
    
  def position(self, dt):
    
    self.X = self.X + self.VX*dt
    self.Y = self.Y + self.VY*dt

 # Function for collision between persons
    
  def collision(self,Vr,distance):

    if (self.VX == 0 and self.VY == 0):

        self.VX = 0
        self.VY = 0

    else:
        
        overlap = 2*self.R - distance     
        
        self.VX = uniform(-2,2)
      
        self.X = self.X + overlap*Vr[0]

        self.VY = random.choice([-1,1])*np.sqrt((2)**(2) - self.VX**(2))
        
        self.Y = self.Y + overlap*Vr[1]


  # Function for collision with the walls
    
  def wall_collision(self, w):

    
    if (w == 1):                          # left wall
      
      overlap = -self.X + self.R          
      
      self.VX = self.VX - 2*self.VX       # Collision reflection
      
      self.X = self.X + overlap           # Overlap increase 
      
      
    if (w == 2):                          #right wall
      
      overlap = l -self.X - self.R
      self.VX = self.VX - 2*self.VX
      self.X = self.X + overlap
      
    if (w == 3):                          #top wall
      
      overlap = l -self.Y - self.R
      self.VY = self.VY - 2*self.VY
      self.Y = self.Y + overlap
      
    if (w == 4):                          #bottom wall
      
      overlap = -self.Y + self.R
      self.VY = self.VY - 2*self.VY
      self.Y = self.Y + overlap
      

  # Function to change the status of persons from healthy to sick
  
  def positive_test(self):

    if (self.recovered != True):
                
      self.sick = True
      self.healthy = False
      
  # Function to change the status of persons from sick to recovered in a determinated period of 18 
  
  def recovered_test(self,cont):

    if (self.sick == True ):

      
      cont = cont + dt
      
      if (cont >= 15 ):
        
        self.recovered = True
        self.sick = False

    return cont


# Initial conditions

n = 200    # number of persons
dt = 0.1   # time scale 
l = np.sqrt(n) # lenght of the box  
r = 0.1        # radio
T = np.arange(0,50,dt)  # Time 


persons= []                       # list in which each entry is a person, representing them as a particle

#Initialization

for i in range(n):

    if (i%4 == 0):
      
        vx = uniform(-2,2)         # initial Velocity and postion are choosen randomly, keeping velocity magnitude fixed 
        vy = random.choice([-1,1])*np.sqrt(2**(2) - vx**(2))

        if (i == 4):                  # One person is sick 

            person = people(uniform(0,l),uniform(0,l), vx, vy, r, False, True, False)
            persons.append(person)
    
        else:

            person = people(uniform(0,l),uniform(0,l), vx, vy, r, True, False, False)
            persons.append(person)

    else:

        person = people(uniform(0,l),uniform(0,l), 0, 0, r, True, False, False)
        persons.append(person)

        
    
cont= np.zeros(n)

data = np.zeros((len(T),3))


# Figure for the simulation
plt.figure(figsize=(l+10,l+10))        # make figure
lim = l               # wall
plt.xlim(0, lim)              # x limit 
plt.ylim(0, lim)              # y limit

plots = [None]*n


# Start simulation

for k in range(len(T)):     # Loop for the time 
  
  for i in range(n):          # Loop for each person

    for j in range(n):        # Loop for interaction between persons
      
      if (i != j):
        
        VR = [persons[i].X - persons[j].X, persons[i].Y - persons[j].Y]
        distance = linalg.norm(VR)

        if distance <= (persons[i].R + persons[j].R ) :    # Collision condition

          if (persons[i].sick == True):                    # Infected condition

            persons[j].positive_test()
            
          Vr = VR/(linalg.norm(VR))
          
          persons[i].collision(Vr,distance)
           
    if (persons[i].X  - persons[i].R <= 0   ):     # conditions for wall collision
  
      persons[i].wall_collision(1)
  
    if (persons[i].X + persons[i].R >= l ):
  
      persons[i].wall_collision(2)
  
	
    if (persons[i].Y + persons[i].R >= l ):
  
      persons[i].wall_collision(3)
  

    if (persons[i].Y - persons[i].R <= 0 ):
  
      persons[i].wall_collision(4)

        
    cont[i] = persons[i].recovered_test(cont[i])    # Counts the time it takes for a person to recover
      
    persons[i].position(dt)		#  Position evolution

    # Data for statistics
    
    if (persons[i].healthy == True):
      
      data[k,0] = data[k,0] +1
      color1 = 'b'
      
    elif (persons[i].sick == True):
      
      data[k,1] = data[k,1] +1
      color1 = 'r'

    elif (persons[i].recovered == True):
      
      color1 = 'g'
      data[k,2] = data[k,2] +1

    # Visual simulation 

    plots[i], = plt.plot(persons[i].X,persons[i].Y,'ko',ms=6,color = color1)     # particle plot


    if i == n-1:

      plt.savefig("Simulation{}.png".format(k), bbox_inches='tight')
      plt.pause(1e-4)

      for s in range(n):

         plots[s].remove()
        
    

plt.close('all')

datos = np.column_stack((data, T))

np.savetxt("Data2.txt",datos, fmt='%s')
