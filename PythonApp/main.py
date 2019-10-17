import numpy as np
import math
import sqlite3
import matplotlib.pyplot as plt
import random
import globals
import SQL_db
import Mass
import display

def menu():
    print("""
    1. Start new database.
    2. Continue simulation.
    3. Display animation.
    4. Quit.
    """)
    option = input("Enter a number: ")
    if option == '1':
        # Create mass objects
        globals.mass_list = Mass.create_mass_list(globals.mass_list)
        # Create database with mass names
        SQL_db.create_mass_names_db(globals.mass_list)
        # Create solar database or empty existing one
        SQL_db.create_solar_db()
        # Run simulation
        dens_iter = int(input("Enter a value for database density parameter (integer, minimum 1): "))
        Mass.run_simulation(dens_iter)
        # Return to menu
        menu()
    elif option == '2':
        menu()
    elif option == '3':
        anim_speed = int(input("Enter an animation speed (integer, minimum 1): "))
        display.display(anim_speed)
        menu()
    elif option == '4':
        pass
    else:
        print("Choose from 1 to 4.")
        menu()

menu()

#TODO
#1. Changing globals at the beginning of the program
#2. Create detailed simulation but save only every tenth row (user should be able to choose).
