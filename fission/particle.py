#module for particles in simulation
import math
import numpy as np
import random

class Particle:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel 
        self.mass = 1
        self.radius = 0
        self.eng = self.getEng()

    def move(self, drag_coeff, dt):
        drag_force = 0.5 * drag_coeff * np.square(self.vel)
        # Apply drag force to each component of velocity  
        accel = drag_force / self.mass
        
        # Update velocity and position
        new_vel = self.vel - (accel * dt)
        self.updVel(new_vel)
        self.updEng(self.getEng())
        new_pos = self.pos + (new_vel * dt)
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

    # Method for random scattering
    def scatterRandomly(self):
        angle1 = random.uniform(0, 2 * np.pi)  # Random angle for scattering
        angle2 = random.uniform(0, np.pi)
        speed = self.getSpeed()
        
        # Convert spherical to Cartesian coordinates
        new_vel_x = speed * np.sin(angle2) * np.cos(angle1)
        new_vel_y = speed * np.sin(angle2) * np.sin(angle1)
        new_vel_z = speed * np.cos(angle2)
        
        new_vel = [new_vel_x, new_vel_y, new_vel_z]
        self.updVel(new_vel)
            
    def collideWall(self, box_dim):
        # Check if the particle collides with the walls and scatter randomly upon collision.
        # Ensure the particle stays within the box.
        pos = self.getPos()
        vel = self.getVel()

        # Scattering upon hitting the x-wall
        if abs(pos[0]) + self.getRadius() >= box_dim[0]:
            vel[0] = -vel[0]  # Reflect the velocity along x-axis
            self.scatterRandomly()  # Scatter in a random direction
            pos[0] = np.sign(pos[0]) * (box_dim[0] - self.getRadius())  # Correct position

        # Scattering upon hitting the y-wall
        if abs(pos[1]) + self.getRadius() >= box_dim[1]:
            vel[1] = -vel[1]  # Reflect the velocity along y-axis
            self.scatterRandomly()  # Scatter in a random direction
            pos[1] = np.sign(pos[1]) * (box_dim[1] - self.getRadius())  # Correct position

        # Scattering upon hitting the z-wall
        if abs(pos[2]) + self.getRadius() >= box_dim[2]:
            vel[2] = -vel[2]  # Reflect the velocity along z-axis
            self.scatterRandomly()  # Scatter in a random direction
            pos[2] = np.sign(pos[2]) * (box_dim[2] - self.getRadius())  # Correct position

        # Update the particle's velocity and position
        self.updVel(vel)
        self.getPos(pos)


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
