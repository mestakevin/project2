# module for particles in simulation
import math
import numpy as np
import random
from .reaction import fissionReaction


class Particle:
    """
    A class representing particles in simulation
    Attributes:
        pos (list): The position(in m) of the particle within a cubic box
        vel (list): The velocity(in m/s^2) of the particle
        mass (integer): The mass(in amu) of the particle
        radius (float): The radius(in m) of the particle
        eng (float): The kinetic energy(in J) of the particle
    """

    def __init__(self, pos, vel):
        """
        Initializes a Particle object

        Parameters:
            pos (list): The position(in m) of the particle within a cubic box
            vel (list): The velocity(in m/s^2) of the particle
        """
        self.pos = pos
        self.vel = vel
        self.mass = 1
        self.radius = 0
        self.eng = self.getEng()

    def move(self, drag_coeff, dt):
        """
        Moves Particle object based on drag coefficent and time step

        Parameters:
            drag_coeff (float): The drag coefficent of spherical particles
            dt (float): The size of time step

        Returns:
            None

        Outputs:
            Particle objects's position, velocity, and energy updated
        """

        cross_sectional_area = np.pi * (self.radius**2)
        # drag_coeff = 0.47  # assuming spherical particles
        water_density = 1000  # kg/m^3 for water
        # Drag force calculation (F_drag = 0.5 * Cd * rho * A * v^2)

        drag_force = (
            0.5
            * drag_coeff
            * water_density
            * cross_sectional_area
            * np.square(self.vel)
        )

        # drag_force = 0.5 * drag_coeff * np.square(self.vel)
        # Apply drag force to each component of velocity
        accel = drag_force / self.mass

        # Update velocity and position
        new_vel = self.vel - (accel * dt)
        self.updVel(new_vel)
        self.updEng(self.getEng())
        new_pos = self.pos + (new_vel * dt)
        self.pos = new_pos

    def getEng(self):
        """
        Obtains Particle object's kinetic energy

        Returns:
            float: Particle object's kinetic energy
        """
        return 0.5 * self.mass * self.getSpeed() ** 2

    def updEng(self, new_eng):
        """
        Updates Particle object's kinetic energy

        Parameters:
            new_eng (float): The new kinetic energy of the Particle object

        Returns:
            None

        Outputs:
            Particle object's eng attribute is updated
        """
        self.eng = new_eng

    def getVel(self):
        """
        Obtains Particle object's velocity

        Returns:
            list: Particle object's velocity
        """
        return self.vel

    def getSpeed(self):
        """
        Obtains Particle object's speed

        Returns:
            float: Particle object's speed
        """
        return np.linalg.norm(self.getVel())

    def updVel(self, new_vel):
        """
        Updates Particle object's velocity

        Parameters:
            new_vel (list): The new velocity of the Particle object

        Returns:
            None

        Outputs:
            Particle object's vel attribute is updated
        """
        self.vel = new_vel

    def getPos(self):
        """
        Obtains Particle object's position

        Returns:
            list: Particle object's position
        """
        return self.pos

    def getRadius(self):
        """
        Obtains Particle object's radius

        Returns:
            float: Particle object's radius
        """
        return self.radius

    def distanceFrom(self, other_particle):
        """
        Calculates the distance between one Particle object and another

        Parameters:
            other_particle (Particle): Particle object whose distance from self is being checked

        Returns:
            float: Distance between two Particle objects
        """
        pos1 = self.getPos()

        x1, y1, z1 = pos1[0], pos1[1], pos1[2]
        pos2 = other_particle.getPos()
        x2, y2, z2 = pos2[0], pos2[1], pos2[2]
        dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
        return dist

    def collideParticle(self, other_particle):
        """
        Executes particle collision logic, either with elastic collisions or fission reaction occurring

        Parameters:
            other_particle (Particle): Particle object whose distance from self is being checked
        Returns:
            list: If fission reaction occurs, returns a list with Barium, Kyrpton and 3 Nuetron objects
        Outputs:
            Updates both Particle object's velocities accordingly and scatters them in a random direction
            If a Neutron and Uranium object collide generates and returns necessary fission products
        """
        min_dist = (self.getRadius() + other_particle.getRadius()) * 1.0e9
        if self.distanceFrom(other_particle) <= min_dist:
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
            elif (
                self.__class__.__name__ == "Neutron"
                and other_particle.__class__.__name__ == "Uranium"
            ) or (
                self.__class__.__name__ == "Uranium"
                and other_particle.__class__.__name__ == "Neutron"
            ):
                # All the generated particles' velocity are relative to the neutron particle before fission reaction.
                if self.__class__.__name__ == "Uranium":
                    fission_products = fissionReaction(
                        self.pos, Barium, Krypton, Neutron
                    )
                else:
                    fission_products = fissionReaction(
                        other_particle.pos, Barium, Krypton, Neutron
                    )
                # For now, just print the new particles for demonstration purposes
                # print("Fission products:", fission_products)
                return fission_products
            # Case 3: Elastic collision with scattering for other types
            else:
                self.elasticCollision(other_particle)

    # Method for random scattering
    def scatterRandomly(self):
        """
        Randomly scatters Particle object's velocity according to uniform random distribution

        Returns:
            None
        Oututs:
            Updates Particle object's vel attribute
        """
        angle1 = random.uniform(0, 2 * np.pi)  # Random angle for scattering
        angle2 = random.uniform(0, np.pi)
        speed = self.getSpeed()

        # Convert spherical to Cartesian coordinates
        new_vel_x = speed * np.sin(angle2) * np.cos(angle1)
        new_vel_y = speed * np.sin(angle2) * np.sin(angle1)
        new_vel_z = speed * np.cos(angle2)

        new_vel = [new_vel_x, new_vel_y, new_vel_z]
        self.updVel(new_vel)

    # Method for elastic collision (momentum conservation and scattering)
    def elasticCollision(self, other_particle):
        """
        Executes elastic particle collision logic to update the two colliding particle's velocity

        Parameters:
            other_particle (Particle): Particle object that is being elastically collided with

        Returns:
            None
        Outputs:
            Both Particle objects' vel attributes are updated in order to conserve momentum in a way to avoid
            erros in vel updating
        """
        # Convert positions to NumPy arrays to perform vector operations
        pos_1 = np.array(self.pos)
        pos_2 = np.array(other_particle.pos)

        vel_1 = np.array(self.vel)
        vel_2 = np.array(other_particle.vel)

        mass_1 = self.mass
        mass_2 = other_particle.mass

        # initial_momentum = vel_1 * mass_1 + vel_2 * mass_2
        # print("INITAL",initial_momentum)

        # Compute new velocities after elastic collision
        if (
            np.linalg.norm(pos_1 - pos_2) >= 1e-6
        ):  # Avoid division by zero or extremely small value
            new_vel_1 = vel_1 - (
                (2 * mass_2 / (mass_1 + mass_2))
                * (
                    np.dot(vel_1 - vel_2, pos_1 - pos_2)
                    / np.linalg.norm(pos_1 - pos_2) ** 2
                )
                * (pos_1 - pos_2)
            )
            new_vel_2 = vel_2 - (
                (2 * mass_1 / (mass_1 + mass_2))
                * (
                    np.dot(vel_2 - vel_1, pos_2 - pos_1)
                    / np.linalg.norm(pos_2 - pos_1) ** 2
                )
                * (pos_2 - pos_1)
            )

            # Update the velocities
            self.updVel(new_vel_1.tolist())
            other_particle.updVel(new_vel_2.tolist())

            # final_momentum = new_vel_1 * mass_1 + new_vel_2 * mass_2
            # print("FINAL",final_momentum)
        else:

            # Swap velocities
            self.updVel(vel_2)
            other_particle.updVel(vel_1)

            # print("second case")
            # final_momentum = vel_2 * mass_1 + vel_1 * mass_2
            # print("FINAL",final_momentum)

            # Scatter in random directions (apply random rotation to velocity vectors)
            self.scatterRandomly()
            other_particle.scatterRandomly()

    def collideWall(self, box_dim):
        """
        Executes logic for particles elastically colliding against walls of box

        Parameters:
            box_dim (list): List with half the length, width, and height of the box
        Returns:
            None
        Outputs:
            Updates the Particle object's vel and pos attributes to elastically collide with box walls
        """
        # Check if the particle collides with the walls and scatter randomly upon collision.
        # Ensure the particle stays within the box.
        pos = self.getPos()
        vel = self.getVel()

        # Scattering upon hitting the x-wall
        if abs(pos[0]) + self.getRadius() >= box_dim[0]:

            vel[0] = -vel[0]  # Reflect the velocity along x-axis
            # self.scatterRandomly()  # Scatter in a random direction

            pos[0] = np.sign(pos[0]) * (
                box_dim[0] - self.getRadius()
            )  # Correct position

        # Scattering upon hitting the y-wall
        if abs(pos[1]) + self.getRadius() >= box_dim[1]:
            # vel[1] = self.proposedVelocity("y")  # Reflect the velocity along y-axis
            vel[1] = -vel[1]  # Reflect the velocity along x-axis

            # self.scatterRandomly()  # Scatter in a random direction
            pos[1] = np.sign(pos[1]) * (
                box_dim[1] - self.getRadius()
            )  # Correct position

        # Scattering upon hitting the z-wall
        if abs(pos[2]) + self.getRadius() * 1e3 >= box_dim[2]:
            # vel[2] = self.proposedVelocity("z")  # Reflect the velocity along z-axis
            vel[2] = -vel[2]  # Reflect the velocity along x-axis

            # self.scatterRandomly()  # Scatter in a random direction
            pos[2] = np.sign(pos[2]) * (
                box_dim[2] - self.getRadius()
            )  # Correct position

        # Update the particle's velocity and position
        self.updVel(vel)
        self.pos = pos


class Neutron(Particle):
    """
    A subclass of Particle that has the inherent attributes of a neutron particle

    Attributes:
        pos (list): The position(in m) of the particle within a cubic box
        vel (list): The velocity(in m/s^2) of the particle
        mass (integer): The mass(in amu) of the particle
        radius (float): The radius(in m) of the particle
        eng (float): The kinetic energy(in J) of the particle
    """

    def __init__(self, pos, vel):
        """
        Initializes a Neutron object

        Parameters:
            pos (list): The position(in m) of the particle within a cubic box
            vel (list): The velocity(in m/s^2) of the particle
        """
        super().__init__(pos, vel)
        self.mass = 1  # kilograms
        self.radius = 8.0e-16  # meters


class Uranium(Particle):
    """
    A subclass of Particle that has the inherent attributes of a Uranium atom

    Attributes:
        pos (list): The position(in m) of the particle within a cubic box
        vel (list): The velocity(in m/s^2) of the particle
        mass (integer): The mass(in amu) of the particle
        radius (float): The radius(in m) of the particle
        eng (float): The kinetic energy(in J) of the particle
    """

    def __init__(self, pos, vel):
        """
        Initializes a Uranium object

        Parameters:
            pos (list): The position(in m) of the particle within a cubic box
            vel (list): The velocity(in m/s^2) of the particle
        """
        super().__init__(pos, vel)
        self.mass = 235  # kilograms
        self.radius = 2.4e-10  # meters


class Barium(Particle):
    """
    A subclass of Particle that has the inherent attributes of a Barium atom

    Attributes:
        pos (list): The position(in m) of the particle within a cubic box
        vel (list): The velocity(in m/s^2) of the particle
        mass (integer): The mass(in amu) of the particle
        radius (float): The radius(in m) of the particle
        eng (float): The kinetic energy(in J) of the particle
    """

    def __init__(self, pos, vel):
        """
        Initializes a Barium object

        Parameters:
            pos (list): The position(in m) of the particle within a cubic box
            vel (list): The velocity(in m/s^2) of the particle
        """
        super().__init__(pos, vel)
        self.mass = 141  # 2.3396e-25 #kilograms
        self.radius = 2.68e-10  # meters


class Krypton(Particle):
    """
    A subclass of Particle that has the inherent attributes of a Krypton atom

    Attributes:
        pos (list): The position(in m) of the particle within a cubic box
        vel (list): The velocity(in m/s^2) of the particle
        mass (integer): The mass(in amu) of the particle
        radius (float): The radius(in m) of the particle
        eng (float): The kinetic energy(in J) of the particle
    """

    def __init__(self, pos, vel):
        """
        Initializes a Krypton object

        Parameters:
            pos (list): The position(in m) of the particle within a cubic box
            vel (list): The velocity(in m/s^2) of the particle
        """
        super().__init__(pos, vel)
        self.mass = 92  # 1.52579e-27 #kilograms
        self.radius = 2.02e-10  # meters
