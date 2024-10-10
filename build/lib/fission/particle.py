#module for particles in simulation
import numpy as np

class Particle:
        def __init__(self, pos, vel):
            self.pos = pos
            self.vel = vel 
            self.mass = 1
            self.eng = self.getEng()

        def move(self, drag_coeff, dt):
            drag_force = 0.5 * drag_coeff * self.vel ** 2
            accel = drag_force / self.mass
            new_vel = self.vel - accel * dt
            self.updVel(new_vel)
            self.pos += self.vel * dt
           

        def getEng(self):
            return  0.5 * self.mass * self.getSpeed()
        
        def updEng(self):
            self.eng = 0.5 * self.mass * self.getSpeed()
        
        def getVel(self):
            return self.vel

        def getSpeed(self):
            return np.sqrt(self.vel.dot(self.vel))

        def updVel(self, new_vel):
            self.vel = new_vel

        def getPos(self):
            return self.pos
            
