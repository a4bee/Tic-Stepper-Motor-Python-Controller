##################################
## Author: Jakub Tomaszewski    ##
## Stepper Motor Control Class  ##
## Company: A4BEE               ##
##################################

import subprocess
import yaml
import time
from threading import Thread


class stepper_motor:
    def __init__(self, mapping_value = 1):
        self.mapping_value = mapping_value
        self.status = self.get_status()
        self.current_position = self.get_current_position()
        print("Current position {}.".format(int(self.current_position)))
        # self.desired_position = int(interp(self.current_position,[0,1000],[0,6250]))
        self.desired_position = int(self.current_position*self.mapping_value)
        
        print("Desired position {}.".format(int(self.desired_position/mapping_value)))
        self.last_desired_position = self.current_position - 1
        self.max_speed = self.status['Max speed']
        self.starting_speed = self.status['Starting speed']
        self.max_deceleration = self.status['Max deceleration']
        self.max_acceleration = self.status['Max acceleration']
        self.current_limit = self.status['Current limit']

        print("Mapping value: ", self.mapping_value)
        print("Max speed: ", self.max_speed) 
        print("Starting speed: ", self.starting_speed)
        print("Max deceleration: ", self.max_deceleration)
        print("Max acceleration: ", self.max_acceleration)
        print("Current limit", self.current_limit)
        print("\n\n")

        self.move_th = Thread(target=self.__move, daemon=True)
        self.move_th.start()

        self.heart_th = Thread(target=self.__heartbeat, daemon=True)
        self.heart_th.start()
        
    
    def __ticcmd(self, *args):
        # print("RUN: ", ['ticcmd'] + list(args))
        return subprocess.check_output(['ticcmd'] + list(args))
    
    # Return status of the motor
    def get_status(self):
        self.status = yaml.safe_load(self.__ticcmd('-s', '--full'))
        return self.status

    # Return the current position of the motor
    def get_current_position(self):
        status = yaml.safe_load(self.__ticcmd('-s', '--full'))
        position = status['Current position']
        self.current_position = int(position/self.mapping_value)
        return self.current_position
    
    # Set the new desired position
    def set_desired_position(self, desired_position):
        self.desired_position = int(desired_position*self.mapping_value)

    # Function which move the motor to the desired position 
    def __move(self):
        while True:    
            if self.last_desired_position != self.desired_position:
                self.__ticcmd('--position', str(self.desired_position))
                self.last_desired_position = self.desired_position
    
    # Hear beat of the stepper motor 
    def __heartbeat(self):
        while True:
            # self.get_status()
            self.__ticcmd('--reset-command-timeout')
            time.sleep(0.1)

    # Drive to limit switch
    def home_sequence(self, dir):
        if dir == "right":
            self.__ticcmd('--home', str('rev'))
        
        if dir == "left":
            self.__ticcmd('--home', str('fwd'))

    #  Make the controller forget its current state.
    def reset(self):
        self.__ticcmd('--reset')

    # Disable the motor driver.
    def deenergize(self):
        self.__ticcmd('--deenergize')
    
    # Stop disabling the driver.
    def energize(self):
        self.__ticcmd('--energize')
        
    # Set new max speed
    def set_max_speed(self, max_speed):
        self.max_speed = max_speed
        self.__ticcmd('--max-speed', str(self.max_speed))
        self.status = self.get_status()
        print("Max speed after changes: ", self.status['Max speed']) 
         
    # Set new starting speed
    def set_starting_speed(self, starting_speed):
        self.starting_speed = starting_speed
        self.__ticcmd('--starting-speed', str(self.starting_speed))
        self.status = self.get_status()
        print("Starting speed after changes: ", self.status['Starting speed'])

    # Set new max acceleration
    def set_max_acceleration(self, max_acceleration):
        self.max_acceleration = max_acceleration
        self.__ticcmd('--max-accel', str(self.max_acceleration))
        self.status = self.get_status()
        print("Max acceleration after changes: ", self.status['Max acceleration'])

    # Set new max deceleration
    def set_max_deceleration(self, max_decelaration):   
        self.max_deceleration = max_decelaration
        self.__ticcmd('--max-decel', str(self.max_deceleration))
        self.status = self.get_status()
        print("Max deceleration after changes: ", self.status['Max deceleration'])

    # Set new current limit 
    def set_current_limit(self, current_limit):
        self.cuurent_limit = current_limit
        self.__ticcmd('--current', str(current_limit))
        self.status = self.get_status()
        print("Current limit after changes", self.status['Current limit'])

            



