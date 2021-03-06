import numpy as np
import math
import random
import globals
import sqlite3
import database

class Mass:
    """Mass (mass, xcor, ycor, xvel, yvel, xacc, yacc)"""

    def __init__(self, mass, xcor, ycor, xvel, yvel, xacc, yacc, name):
        self.mass = mass
        self.xcor = xcor
        self.ycor = ycor
        self.xvel = xvel
        self.yvel = yvel
        self.xacc = xacc
        self.yacc = yacc
        self.name = name

    def calc_radius(self, obj):
        radius_x = obj.xcor - self.xcor
        radius_y = obj.ycor - self.ycor
        radius = math.sqrt(radius_x ** 2 + radius_y ** 2)
        return [radius_x, radius_y, radius]

    def calc_force(self, obj):
        [radius_x, radius_y, radius] = self.calc_radius(obj)
        force = globals.grav_const * self.mass * obj.mass / (radius ** 2)
        force_x = force * (radius_x / radius)
        force_y = force * (radius_y / radius)
        return [force_x, force_y]

    def calc_acceleration(self, mass_list):
        sum_force_x = 0
        sum_force_y = 0
        for obj in mass_list:
            if obj is self:
                continue
            [force_x, force_y] = self.calc_force(obj)
            sum_force_x = sum_force_x + force_x
            sum_force_y = sum_force_y + force_y
        self.xacc = sum_force_x / self.mass
        self.yacc = sum_force_y / self.mass

    def update_velocity_and_coordinates(self):
        self.xvel = self.xvel + self.xacc * globals.timestamp
        self.yvel = self.yvel + self.yacc * globals.timestamp
        self.xcor = self.xcor + self.xvel * globals.timestamp
        self.ycor = self.ycor + self.yvel * globals.timestamp

def create_mass_list(new):
    """Create mass list"""

    # Make sure mass list is empty
    list = np.empty(0, dtype = object)

    if new == 1:
        sun = Mass(1.989 * (10 ** 30), 0, 0, 0, 0, 0, 0, 'Sun')
        mercury = Mass(0.330 * (10 ** 24), 57.9 * (10 ** 9), 0, 0, 47400, 0, 0, 'Mercury')
        venus = Mass(4.87 * (10 ** 24), 108.2 * (10 ** 9), 0, 0, 35000, 0, 0, 'Venus')
        earth = Mass(5.972 * (10 ** 24), 149.6 * (10 ** 9), 0, 0, 29800, 0, 0, 'Earth')
        mars = Mass(0.642 * (10 ** 24), 227.9 * (10 ** 9), 0, 0, 24100, 0, 0, 'Mars')
        jupiter = Mass(1898 * (10 ** 24), 778.6 * (10 ** 9), 0, 0, 13100, 0, 0, 'Jupiter')
        saturn = Mass(568 * (10 ** 24), 1433.5 * (10 ** 9), 0, 0, 9700, 0, 0, 'Saturn')
        uranus = Mass(86.8 * (10 ** 24), 2872.5 * (10 ** 9), 0, 0, 6800, 0, 0, 'Uranus')
        neptune = Mass(102 * (10 ** 24), 4495.1 * (10 ** 9), 0, 0, 5400, 0, 0, 'Neptune')

        # Add Sun and Earth
        list = np.append(list, [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune])

        # Add random objects
        for i in range(globals.rand_mass_num):
            list = np.append(list, Mass(random.randint(10 ** 15,10 ** 23), random.randint(-10 ** 11,10 ** 11), random.randint(-10 ** 11,10 ** 11), random.randint(-10 ** 4,10 ** 4), random.randint(-10 ** 4,10 ** 4), 0, 0, 'Object' + str(i + 1)))
        return list

    else:
        globals.iter_num = database.get_last_row('Sun')[0]
        sun = Mass(1.989 * (10 ** 30), database.get_last_row('Sun')[1], database.get_last_row('Sun')[2], database.get_last_row('Sun')[3], database.get_last_row('Sun')[4], 0, 0, 'Sun')
        mercury = Mass(0.330 * (10 ** 24), database.get_last_row('Mercury')[1], database.get_last_row('Mercury')[2], database.get_last_row('Mercury')[3], database.get_last_row('Mercury')[4], 0, 0, 'Mercury')
        venus = Mass(4.87 * (10 ** 24), database.get_last_row('Venus')[1], database.get_last_row('Venus')[2], database.get_last_row('Venus')[3], database.get_last_row('Venus')[4], 0, 0, 'Venus')
        earth = Mass(5.972 * (10 ** 24), database.get_last_row('Earth')[1], database.get_last_row('Earth')[2], database.get_last_row('Earth')[3], database.get_last_row('Earth')[4], 0, 0, 'Earth')
        mars = Mass(0.642 * (10 ** 24), database.get_last_row('Mars')[1], database.get_last_row('Mars')[2], database.get_last_row('Mars')[3], database.get_last_row('Mars')[4], 0, 0, 'Mars')
        jupiter = Mass(1898 * (10 ** 24), database.get_last_row('Jupiter')[1], database.get_last_row('Jupiter')[2], database.get_last_row('Jupiter')[3], database.get_last_row('Jupiter')[4], 0, 0, 'Jupiter')
        saturn = Mass(568 * (10 ** 24), database.get_last_row('Saturn')[1], database.get_last_row('Saturn')[2], database.get_last_row('Saturn')[3], database.get_last_row('Saturn')[4], 0, 0, 'Saturn')
        uranus = Mass(86.8 * (10 ** 24), database.get_last_row('Uranus')[1], database.get_last_row('Uranus')[2], database.get_last_row('Uranus')[3], database.get_last_row('Uranus')[4], 0, 0, 'Uranus')
        neptune = Mass(102 * (10 ** 24), database.get_last_row('Neptune')[1], database.get_last_row('Neptune')[2], database.get_last_row('Neptune')[3], database.get_last_row('Neptune')[4], 0, 0, 'Neptune')
    
        # Add Sun and Earth
        list = np.append(list, [sun, earth])

        # Add random objects
        for i in range(globals.rand_mass_num):
            list = np.append(list, Mass(float(database.get_last_row('Object' + str(i + 1))[5]), database.get_last_row('Object' + str(i + 1))[1], database.get_last_row('Object' + str(i + 1))[2], database.get_last_row('Object' + str(i + 1))[3], database.get_last_row('Object' + str(i + 1))[4], 0, 0, 'Object' + str(i + 1)))
        return list

def run_simulation(db_density):
    """Run simulation"""
    # Connect to database
    conn = sqlite3.connect('solar_system.db')
    c = conn.cursor()

    density_iter = db_density - 1
    sim_iter = globals.iter_num + 1
    for _ in range(0, globals.sim_length, globals.timestamp):
        density_iter = density_iter + 1
        for obj in globals.mass_list:
            # Calculate accelerartions
            obj.calc_acceleration(globals.mass_list)

            # Update properties of each planet
            obj.update_velocity_and_coordinates()

            # Save data in SQL database
            if density_iter == db_density:
                c.execute("INSERT INTO solar_system VALUES (?, ?, ?, ?, ?, ?, ?)", (sim_iter, obj.name, obj.xcor, obj.ycor, obj.xvel, obj.yvel, str(obj.mass),))
        if density_iter == db_density:
            sim_iter = sim_iter + 1
            density_iter = 0

    # Commit changes and close connection
    conn.commit()
    c.close()
    conn.close()
    print("Simulation finished")