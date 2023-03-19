# Poppy Social Robotics SDK Legs
___
#### Team Members: Nathan Borrego, Miranda Goelz, Aleksander Thompson, James Gray, Helen Guerrero 
This is a continuation of the Poppy Social Robotics SDK by Colin Henson, Sydney Awid and Hannah Stent. This version contains functionality for legs. To see documentation concerning the head and face tracking please visit this [link](https://github.com/chenson399/poppy-sdk).
<br/>

While this project used the Poppy Social Robotics SDK code, this documentation will focus on the changes and updates made for the legs portion of the SDK.

## Project Overview
The purpose of this project was to modify the Poppy Social Robotics SDK to include functionality for a set of legs to work alongside the face tracking and gesturing of the upper torso completed by the Poppy Social Robotics SDK. Like the project before it, this project is based on the Poppy Project's Poppy robot. This project has made substitutions and changes to the materials and designs used in the original Poppy project. This project has been made for the University of Colorado at Colorado Springs.

## User Guide
This section will outline what tools were used and how they were used to work on this project. This is intended to help anyone who intends to use this code or will be working on Poppy in the future. 
### 0. Getting Started
To start, you will need the following software:<br/>

[Dynamixel Wizard 2.0](https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_wizard2/)

A Python 3 capable IDE (PyCharm was used for this project).

This software allows the user to scan and configure Dynamixel Motors from Robotis.

You will also need the following hardware (which should still be with Poppy...).

[Dynamixel MX28T]()

[Dynamixel MX64T]()

[Robotis U2D2](https://www.robotis.us/u2d2/)

[12V 5A 60W Power Suppy](https://www.robotis.us/smps-12v-5a-ps-10-us-110v/)

[U2D2 Power Hub Board Set](https://www.robotis.us/u2d2-power-hub-board-set/) or [What we used]()

[TTL Cables](https://www.robotis.us/robot-cable-xl320-convertible-130mm-10pcs/) 

[TTL Cables Convertible](https://www.robotis.us/robot-cable-x3p-180mm-convertible-10pcs/) (Please note that the U2D2 and Power Hub have white connectors while the servos have beige connectors. Beige TTL connectors ***will not*** fit white TTL connectors. You will need beige TTL to white TTL cables for these instances)

[TTL Hubs](https://www.robotis.us/3p-extension-pcb/)

And of course, you should have Poppy itself.

All this hardware is what was used during this project.

### 1. Using Dynamixel Wizard
The Dynamixel Wizard allows you to scan for servos on a USB COM port. To start, make sure you have the [Robotis U2D2](https://www.robotis.us/u2d2/) connected to your computer via USB. From here, connect a TTL cable from the U2D2 to a servo. Also, connect the power brick to the [U2D2 Power Hub Board Set](https://www.robotis.us/u2d2-power-hub-board-set/) and connect the U2D2 Power Hub Board Set TTL to the servo as well. With the U2D2 and the Power Hub both connected by TTL to the servo, you will be able to scan the servo on the Wizard.

First, click scan on the Wizard. The Wizard will scan all servo IDs and all baud rates to start with. You can change what IDs and baud rates to scan under Options > Scan. If you have a servo connected, once the scan is complete, you will see the servo and its ID show up on the left on the Wizard. You can click on the servo to see all the information and options for that servo. It is important to remember that each servo has an ID and a baud rate.

It is important to note that servos with the *same* ID **cannot** be displayed in the Wizard at the same time. All servo IDs **must** be unique to be scan-able and usable. **If you are integrating new servos into the system, you *MUST* scan in each new servo individually into the Wizard and change its ID to a new and unique ID before trying to use these servos together with existing or other new servos. All servos start with an ID of 1, so set it to something else and do not set it to an existing ID. A list of all used IDs for this project can be found below. Note that this can be tedious to do, and you may have to set temporary IDs on a servo in order to get it to what you want especially when swapping the IDs of servos.**
<br/><br/>
#### 1.1 Important Notes about Dynamixel Wizard and Servos
It is important to understand how the Dynamixel Wizard controls the servos so here are a few notes to be aware of. 

The servos in the Wizard operate on a 0&deg; to 360&deg; system. 

The middle and right pane of Dynamixel Wizard are interactable and allow you to change some values if you so desire. This can be unclear when first starting to use the Wizard. When interacting with a servo in joint mode, the red line is the goal position of the servo, while the green line is the actual position of the servo. The backing grey "circle" is the allowed limits on the angles of the servo. These angle limits can be changed, you will see them listed in the middle pane of the Wizard. It may prove useful to set angle limits so that you can more readily see where the servo can be, but be warned that they can also be misleading based to how the actual physical system works.

The servos ***will not*** cross the 360&deg; -> 0&deg; boundary and vice versus. This means that a servo trying to go from a postion of 26&deg; to 354&deg; ***will not*** take the short path by crossing 0&deg;. This can cause erratic behavior in the physical system if you are not careful with the initial positioning of servos when the system is built. It is important to make sure that the servos will never cross this boundary on their desired swinging path.

When the torque on a joint servo is **on**, the servo is locked and cannot free swing. Click the torque **off** will alow the servo to freely swing. This can be controlled by code which will be covered.

### 2. Controlling Servos with Python
This project uses the [pypot.dynamixel library](https://github.com/poppy-project/pypot) to control the Dynamixel servos. 


## Documentation


