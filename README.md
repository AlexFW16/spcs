# Safety Pedestrian Crosswalk System (SPCS)

## Project Overview

Welcome to the Safety Pedestrian Crosswalk System (SPCS) repository. This project was developed by Group 20 as part of the Embedded & Pervasive Systems 24S course. The main goal of this project is to increase pedestrian safety in road traffic by adapting the pedestrian traffic light timings based on weather and light conditions.

## System Description

The SPCS is designed to enhance pedestrian safety by adjusting the green light duration and waiting time based on weather and light conditions:

- **Rainy Conditions:** Shorter waiting time and longer green light duration.
- **Dark Conditions:** Adjusted timings for better visibility and safety.

### Components Used

- **Raspberry Pi 5 (P1)**
  - SenseHAT (Humidity sensor, joystick button, 8x8 display)
- **Raspberry Pi 4 (P2)**
  - Breadboard with Red and Green LEDs, 100Ω resistors
  - Breadboard with Photocell light sensor, 10kΩ resistor
- **Control Unit**
  - Laptop
