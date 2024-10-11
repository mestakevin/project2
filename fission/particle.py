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
            self.updEng(self.getEng())
            self.pos += self.vel * dt
           

        def getEng(self):
            return  0.5 * self.mass * self.getSpeed() ** 2
        
        def updEng(self, new_eng):
            self.eng = new_eng
        
        def getVel(self):
            return self.vel

        def getSpeed(self):
            return np.sqrt(self.vel.dot(self.vel))

        def updVel(self, new_vel):
            self.vel = new_vel

        def getPos(self):
            return self.pos

        def collide(self,other_particle):


class Neutron(Particle):
        def __init__(self, pos, vel):
            super().__init__(pos,vel)
            self.mass = 1.674927e-27 #kilograms
            self.radius = 8.0e-16 #meters


class Uranium(Particle):
        def __init__(self, pos, vel):
            super().__init__(pos,vel)
            self.mass = 3.9029e-25 #kilograms
            self.radius = 2.4e-10 #meters


class Barium(Particle):
        def __init__(self, pos, vel):
            super().__init__(pos,vel)
            self.mass = 2.3396e-25 #kilograms
            self.radius = 2.68e-10 #meters


class Krypton(Particle):
        def __init__(self, pos, vel):
            super().__init__(pos,vel)
            self.mass = 1.52579e-27 #kilograms
            self.radius = 2.02e-10 #meters
