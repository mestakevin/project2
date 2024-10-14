#module for particles in simulation
import math
import numpy as np

class Particle:
        def __init__(self, pos, vel):
            self.pos = pos
            self.vel = vel 
            self.mass = 1
            self.radius = 0
            self.eng = self.getEng()

        def move(self, drag_coeff, dt):
            drag_force = 0.5 * drag_coeff * np.square(self.vel)
          
            accel = drag_force / self.mass
           

            new_vel = self.vel - accel * dt
           
    
            self.updVel(new_vel)
            self.updEng(self.getEng())

            new_pos = self.pos + new_vel * dt
           
            self.pos = new_pos
           

        def getEng(self):
            return  0.5 * self.mass * self.getSpeed() ** 2
        
        def updEng(self, new_eng):
            self.eng = new_eng
        
        def getVel(self):
            return self.vel

        def getSpeed(self):
            return np.linalg.norm(self.getVel())

        def updVel(self, new_vel):
            self.vel = new_vel

        def getPos(self):
            return self.pos
        
        def getRadius(self):
            return self.radius

        def distanceFrom(self,other_particle):
            pos1 = self.getPos()
            
            x1,y1,z1= pos1[0], pos1[1], pos1[2]
            pos2 = other_particle.getPos()
            x2,y2,z2= pos2[0], pos2[1], pos2[2]
            dist = math.sqrt( (x1-x2)**2 + (y1 -y2)**2 +(z1-z2)**2 )  
            return dist


        def collideParticle(self, other_particle):
            min_dist = self.getRadius() + other_particle.getRadius() * 1.0e8
            if self.distanceFrom(other_particle)  <= min_dist:
                # Class names 
                
                # Case 1: Both particles are of the same type (swap velocities and scatter)
                if self.__class__.__name__ == other_particle.__class__.__name__:
                    vel_1 = self.getVel()
                    vel_2 = other_particle.getVel()

                    # Swap velocities
                    self.updVel(vel_2)
                    other_particle.updVel(vel_1)

                    # Scatter in random directions (apply random rotation to velocity vectors)
                    self.scatterRandomly()
                    other_particle.scatterRandomly()

                # Case 2: Neutron and Uranium collision (fission event)
                elif (self.__class__.__name__ == 'Neutron' and other_particle.__class__.__name__ == 'Uranium') or (self.__class__.__name__ == 'Uranium' and other_particle.__class__.__name__ == 'Neutron'):
                    self.fissionReaction()

                # Case 3: Elastic collision with scattering for other types
                else:
                    self.elasticCollision(other_particle)
        
        def collideWall(self,box_dim):
                cur_vel = self.getVel()
                if self.getRadius() * self.getPos()[0] > abs(box_dim[0]):
                    x_vel = -1 * cur_vel[0]
                else:
                     x_vel = cur_vel[0]
                if self.getRadius() * self.getPos()[1] > abs(box_dim[1]):
                    y_vel = -1 * cur_vel[1]
                else:
                    y_vel = cur_vel[1]
                if self.getRadius() * self.getPos()[2] > abs(box_dim[2]):
                    z_vel = -1 * cur_vel[2]
                else:
                    z_vel = cur_vel[2]
                new_vel = [x_vel,y_vel,z_vel]
                self.updVel(new_vel)                



class Neutron(Particle):
        def __init__(self, pos, vel):
            super().__init__(pos,vel)
            self.mass = 1 #kilograms
            self.radius = 8.0e-16 #meters


class Uranium(Particle):
        def __init__(self, pos, vel):
            super().__init__(pos,vel)
            self.mass = 235 #kilograms
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
