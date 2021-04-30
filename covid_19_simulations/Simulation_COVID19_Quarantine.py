import numpy as np
import matplotlib.pyplot as plt
import random
from random import uniform
from numpy import linalg


class people:

  #atributos

  healthy = True
  sick = False
  recovered = False 
  

  def __init__(self, x, y, vx, vy, r, H, S, D):
    
    self.healthy = H
    self.sick = S
    self.recovered = D
    self.X = x
    self.Y = y
    self.VX = vx
    self.VY = vy
    self.R = r
    
  def position(self, dt):
    
    self.X = self.X + self.VX*dt
    self.Y = self.Y + self.VY*dt
    
  def collision(self,Vr,distance):
    

    overlap = 2*self.R - distance

    self.VX = uniform(-1,1)
      
    self.X = self.X + overlap*Vr[0]

    self.VY = random.choice([-1,1])*np.sqrt((1.5)**(2) - self.VX**(2))

    self.Y = self.Y + overlap*Vr[1]

    
  def wall_collision(self, w):

    
    if (w == 1): #left wall
      overlap = -self.X + self.R
      self.VX = self.VX - 2*self.VX  # Collision reflection 
      self.X = self.X + overlap
      
    if (w == 2): #right wall
      overlap = l - self.X - self.R
      self.VX = self.VX - 2*self.VX
      self.X = self.X + overlap
      
    if (w == 3): #top wall
      overlap = l - self.Y - self.R
      self.VY = self.VY - 2*self.VY
      self.Y = self.Y + overlap
      
    if (w == 4): #bottom wall
      overlap = -self.Y + self.R
      self.VY = self.VY - 2*self.VY
      self.Y = self.Y + overlap
		
    if (w == 5): #
      overlap = l/3. -self.X + self.R
      self.VX = self.VX - 2*self.VX
      self.X = self.X + overlap
    
    if (w == 6): #
      
      overlap = l/3. -self.X - self.R
      self.VX = self.VX - 2*self.VX
      self.X = self.X + overlap
    
  def positive_test(self):

    if (self.recovered != True):
                
      self.sick = True
      self.healthy = False
  
  def recovered_test(self,cont):

    if (self.sick == True ):

      
      cont = cont + dt
      
      if (cont >= 15 ):
        
        self.recovered = True
        self.sick = False

    return cont
  
class movil_wall:
  
  def __init__(self, x_wall,y_down, y_up):
    
    self.x_wall = x_wall 
    self.up = y_up
    self.down = y_down


  def move(self,k):
    if (k > 70 and k < 200):
    	self.x_wall = np.delete(self.x_wall,0)
    	self.up = np.delete(self.up,0)
	self.down = np.delete(self.down,-1)
   
n = 200
dt = 0.1  #time step
#l = 7.0
l = np.sqrt(n)
r = 0.1 
T = np.arange(0,50,dt)
down = np.array(np.arange(0,l/2,l/1000.))
up = np.array(np.arange(l/2,l,l/1000.))
x_wall = np.ones(len(up))*(l/3.)
wall_m = movil_wall(x_wall,down,up)
plt.figure(figsize=(l,l))        # make figure
lim = l               # wall
plt.xlim(0,lim)              # x limit 
plt.ylim(0,lim)              # y limit


persons= []                       # list in which each entry is a person, representing them as a particle

for i in range(n):

  vx = uniform(-1,1)
  vy = random.choice([-1,1])*np.sqrt(1.5**(2) - vx**(2))

  if (i == 0):

    person = people(uniform(0,l/3.),uniform(0,l), vx, vy, r, False, True, False)
    persons.append(person)
    
  else:

    person = people(uniform(0,l),uniform(0,l), vx, vy, r, True, False, False)
    persons.append(person)
    

cont= np.zeros(n)

data = np.zeros((len(T),3))

plots = [None]*n


for k in range(len(T)):     # Bucle for the time 
  
  for i in range(n):          # Bucle for each person

    for j in range(n):
      
      if (i != j):
        
        VR = [persons[i].X - persons[j].X, persons[i].Y - persons[j].Y]
        distance = linalg.norm(VR)

        if distance <= (persons[i].R + persons[j].R ) :

          if (persons[i].sick == True):

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

      #quarantine wall
      
    if (persons[i].X > l/3.):
      
      if (persons[i].X - persons[i].R <= l/3. ):
      	if (persons[i].Y <= wall_m.down[-1] or persons[i].Y >= wall_m.up[0]):
      	  persons[i].wall_collision(5)	
    
    else:
       
      if (persons[i].X + persons[i].R >= l/3. ):
	if (persons[i].Y <= wall_m.down[-1] or persons[i].Y >= wall_m.up[0]):
          persons[i].wall_collision(6)	
        
    cont[i] = persons[i].recovered_test(cont[i])
      
    persons[i].position(dt)		#  Position evolution

    if (persons[i].healthy == True):
      
      data[k,0] = data[k,0] +1
      color1 = 'b'
      
    elif (persons[i].sick == True):
      
      data[k,1] = data[k,1] +1
      color1 = 'r'

    elif (persons[i].recovered == True):
      
      color1 = 'g'
      data[k,2] = data[k,2] +1


      
    plots[i], = plt.plot(persons[i].X,persons[i].Y,'ko',ms=6,color = color1)	# particle plot

    
    if i == n-1:

      y_down, = plt.plot(wall_m.x_wall,wall_m.down ,'-', color = 'black')
      y_up, = plt.plot(wall_m.x_wall,wall_m.up ,'-',color = 'black')
      plt.savefig("simulacion{}.png".format(k))
      plt.pause(1e-4)
      y_up.remove()
      y_down.remove()    

      for s in range(n):
        plots[s].remove()


  wall_m.move(k)
 # print(up, down)
        
plt.show()

#print(up, down)

datos = np.column_stack((data, T))

np.savetxt("Data3.txt",datos, fmt='%s') 
