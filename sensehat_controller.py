from sense_hat import SenseHat
from time import sleep
import RTIMU


class Sensehat_Controller:

    sense = SenseHat()
    # states
    ttg = [10, 7, 7, 5]  # red
    gd = [15, 10, 20, 20]  # green

    # Define colours
    black = (0, 0, 0)  # Background colour (black)
    yellow = (255, 255, 0)  # Yellow colour
    red = (255, 0, 0)  # Red colour
    green = (0, 255, 0)  # Green colour

    # Define digit patterns
    digits0_9 = [
        [2, 9, 11, 17, 19, 25, 27, 33, 35, 42],  # 0
        [2, 9, 10, 18, 26, 34, 41, 42, 43],  # 1
        [2, 9, 11, 19, 26, 33, 41, 42, 43],  # 2
        [1, 2, 11, 18, 27, 35, 41, 42],  # 3
        [3, 10, 11, 17, 19, 25, 26, 27, 35, 43],  # 4
        [1, 2, 3, 9, 17, 18, 27, 35, 41, 42],  # 5
        [2, 3, 9, 17, 18, 25, 27, 33, 35, 42],  # 6
        [1, 2, 3, 9, 11, 19, 26, 34, 42],  # 7
        [2, 9, 11, 18, 25, 27, 33, 35, 42],  # 8
        [2, 9, 11, 17, 19, 26, 27, 35, 41, 42]  # 9
    ]


    # Function to display a two-digit number
    def display_number(self, number, colour):
        str_number = str(number).zfill(2)  # Ensure the number is two digits
        digit1 = int(str_number[0])
        digit2 = int(str_number[1])

        # Create an empty display buffer
        display = [self.black] * 64

        # Set the pixels for the first digit (left-aligned)
        for pixel in self.digits0_9[digit1]:
            display[pixel] = colour

        # Set the pixels for the second digit (right-aligned)
        for pixel in self.digits0_9[digit2]:
            display[pixel + 4] = colour  # Shift by 4 to the right

        self.sense.set_pixels(display)


    # Function to clear the display
    def clear_display(self):
        self.sense.clear()


    # Function to perform the countdown
    def red_countdown(self, red_start_count, green_start_count):
        for i in range(red_start_count, -1, -1):
            self.display_number(i, self.red)
            sleep(0.9)  # display of the digits
            self.clear_display()
            sleep(0.1)  # Briefly clear the display before showing the next number

        for i in range(green_start_count, -1, -1):
            self.display_number(i, self.green)
            sleep(0.9)  # display of the digits
            self.clear_display()
            sleep(0.1)  # Briefly clear the display before showing the next number

    def start_countdown(self, state):
        self.red_countdown(self.ttg[state], self.gd[state])



