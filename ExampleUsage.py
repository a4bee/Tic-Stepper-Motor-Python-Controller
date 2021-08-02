##########################################
## Author: Jakub Tomaszewski            ##
## Example Stepper motor Manual Control ##
## Company: A4BEE                       ##
##########################################

from StepperMotor import stepper_motor
import argparse
import time

def main():
    from StepperMotor import stepper_motor

    ap = argparse.ArgumentParser()
    ap.add_argument("-mv", "--mapping_value", default=1, required=False,
    help="new mapping value")

    ap.add_argument("-ss", "--starting_speed", default=0, required=False,
    help="new starting speed value")

    ap.add_argument("-cl", "--current_limit", default=400, required=False,
    help="new current limit value")

    ap.add_argument("-ms", "--max_speed", default=6000000, required=False,
    help="new max speed value")

    ap.add_argument("-ma", "--max_acceleration", default=80000, required=False,
    help="new max acceleration value")

    ap.add_argument("-md", "--max_deceleration", default=80000, required=False,
    help="new max deceleration value")
   

    args = vars(ap.parse_args())

    mapping_value = float(args["mapping_value"])
    starting_speed = int(args["starting_speed"])
    current_limit = int(args["current_limit"])
    max_speed = int(args["max_speed"])
    max_acceleration = int(args["max_acceleration"])
    max_deceleration = int(args["max_deceleration"])

    # The default mapping value is equal 1
    stepper_motor = stepper_motor(mapping_value=mapping_value)

    # The default starting speed is equal 0
    stepper_motor.set_starting_speed(starting_speed)

    # The default current limit is equal 400
    stepper_motor.set_current_limit(current_limit)
    
    # The default max speed is equal 6000000 
    stepper_motor.set_max_speed(max_speed)

    # The default max acceleration is equal 80000 
    stepper_motor.set_max_acceleration(max_acceleration)

    # The default max acceleration is equal 80000 
    stepper_motor.set_max_deceleration(max_deceleration)  
    
    print("\n\ncommand could be:")
    print("Float desired position, or")
    print("home - to make home sequence, or")
    print("d - to degenerize the motor, or")
    print("e - to energize the engine, or")
    print("r - to reset the controller")
    print("status -  to print the status")
    print("position -  to print the current position of the motor")
    print("\n")

    while True:
        command = input("New command: ")
        if (command == "home"):
            stepper_motor.home_sequence("right")
        elif (command == "d"):
            stepper_motor.deenergize()
        elif (command == "e"):
            stepper_motor.energize()
        elif (command == "r"):
            stepper_motor.reset()
        elif (command == "status"):
            print("Status: ", stepper_motor.get_status())
        elif (command == "position"):
            print("The current position of the motor is equal: ", stepper_motor.get_current_position())
        else:
            stepper_motor.set_desired_position(int(command))

   
if __name__ == "__main__":
    main()

        