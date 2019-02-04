# Objectives
* To measure the soil moisture of a plant, display the value in Domoticz Home Automation System, in a TinkerForge segment display 4x7 and TinkerForge RGB LED indicator.
* To learn how to write generic Python plugin(s) for the Domoticz Home Automation System communicating with [Tinkerforge](http://www.tinkerforge.com) Building Blocks.

## Solution
A Domoticz Python plugin "Soil Moisture Monitor" with a soil moisture monitor device obtaining the moisture value from a Tinkerforge moisture bricklet.
The Tinkerforge moisture bricklet is connected to a Tinkerforge master brick with WiFi extension.
The moisture value is converted to a range 0(dry) - 100(saturated) and displayed in a Tinkerforge segment display 4x7.
In addition, a Tinkerforge rgb led bricklet indicates the state red(dry), yellow(irrigation advice), green(saturated).

![domoticz-tinkerforge-soilmoisturemonitor-plugin-p](https://user-images.githubusercontent.com/47274144/52175085-8fa85300-279e-11e9-8bd5-dc5ab34cc11b.png)

## Hardware Parts
* Raspberry Pi 3B+
* Tinkerforge Master Brick
* Tinkerforge WIFI Master Extention 2.0
* Tinkerforge Moisture Bricklet 1.1
* Tinkerforge Segment Display 4X7 Bricklet 1.0
* Tinkerforge RGB LED Bricklet 1.0

### Notes about the Tinkerforge Moisture Bricklet 1.1
1) In 2018 Tinkerforge stated: The Moisture Bricklet is discontinued and is no longer sold.
An alternate solution could be a Tinkerforge Analog In Bricklet and a 3rd party Soil Moisture sensor.

2) The Tinkerforge Moisture Bricklet Documentation describes the higher the value the more wet (with range 0 - 4095), but ...
field tests show the other way around in a range 2200(wet) - 3400(dry) - this range depends probably on the device,it is used for this solution.

## Software
Versions for developing & using this plugin.
* Raspberry Pi Raspian 4.14
* Domoticz Home Automation System V4.1
* Tinkerforge Python Binding v2.1.20
* Python 3.5.3
* Thonny 3.0.8 (Python IDE)

## Quick Steps
For implementing the Plugin on the Domoticz Server running on the Raspberry Pi.
See also Appendix Python Plugin Code (well documented).

## Tinkerforge Soil Moisture Monitor Prototype
Build the prototype by connecting the Tinkerforge building blocks (see hardware).
Connect the Master Brick to a device running the Brick Deamon and Viewer.
Just in a nutshell the actions taken to setup the Tinkerforge building blocks using the Tinkerforge Brick Viewer.
* Update the devices firmware
* Set the WiFi master extension fixed IP address in client mode
* Obtain the UID's of the Tinkerforge bricklets as required by the Python plugin

After setting up the Tinkerforge building blocks, reset the master brick and check if the master brick canbe reached via WLAN:
ping tf-wifi-ext-ip-address

## Domoticz Web UI's
Open windows Domoticz Setup > Hardware, Domoticz Setup > Log, Domoticz Setup > Devices
This is required to add the new hardware with its device and monitor if the plugin code is running without errors.

## Create folder
cd /home/pi/domoticz/plugins/soilmoisturemonitor

## Create the plugin
The plugin has a mandatory filename plugin.py located in the newly created plugin folder
For Python development Thonny, running on a Windows 10 device, is used.

-Install the Tinkerforge Python API
There are two options:

### 1) sudo pip install tinkerforge
This advantage is that in case of binding updates, only a single folder must be updated.
Check if a folder tinkerforge is created in folder /usr/lib/python3/dist-packages.
If this is not the case, unzip the Tinkerforge Python Binding into the folder /usr/lib/python3/dist-packages.
Example:
  Create subfolder Tinkerforge holding the Tinkerforge Python Library
  cd /home/pi/tinkerforge
  Unpack the latest python bindings into folder /home/pi/tinkerforge
  Copy /home/pi/tinkerforge to the Python3 dist-packges
  sudo cp -r /home/pi/tinkerforge /usr/lib/python3/dist-packages/

In the Python Plugin code amend the import path to enable using the Tinkerforge libraries
from os import path
import sys
sys.path
sys.path.append('/usr/lib/python3/dist-packages')

### 2) Install the Tinkerforge Python Bindings in a subfolder of the plugin and copy the binding content.
This disadvantage is that every Python plugin using the bindings must have a subfolder tinkerforge.
In case of binding updates,each of the tinkerforge plugin folders must be updated.
/home/pi/domoticz/plugins/soilmoisturemonitor/tinkerforge

There is no need to amend the path as for option 1.

For either ways, the bindings are used like:
import tinkerforge
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_moisture import BrickletMoisture
from tinkerforge.bricklet_segment_display_4x7 import BrickletSegmentDisplay4x7
from tinkerforge.bricklet_rgb_led import BrickletRGBLED
add more depending Tinkerforge brick/bricklet used.

Ensure to update the files in case of newer Tinkerforge Python Bindings.

## Make plugin.py executable
cd /home/pi/domoticz/plugins/soilmoisturemonitor
chmod +x plugin.py

## Restart Domoticz
Restart Domoticz to find the plugin:
sudo systemctl restart domoticz.service

**Note**
When making changes to the Python plugin code, ensure to restart Domoticz and refresh any of the Domoticz Web UI's.

## Domoticz Add Hardware Soil Moisure Monitor
**IMPORTANT**
Prior adding, set in the Domoticz Settings the option to allow new hardware.
If this option is not enabled, no new soilmoisture device is created.
Check in the Domoticz log as error message Python script at the line where the new device is used
(i.e. Domoticz.Debug("Device created: "+Devices[1].Name))

In Domoticz Web UI, select tab Setup > Hardware and add the new hardware Soil Moisture Monitor.
The initial check interval is set at 60 seconds. This is a good value for testing, but for finalversion set tohigher value like once per hour (3600 seconds).

![domoticz-tinkerforge-soilmoisturemonitor-plugin-dh](https://user-images.githubusercontent.com/47274144/52175083-8fa85300-279e-11e9-953f-52f0caaf4e5d.png)

## Add Hardware - Check the Domoticz Log
After adding,ensure to check the Domoticz Log (Domoticz Web UI, select tab Setup > Log)
Example:
```
(SMM) 'HomeFolder':'/home/pi/domoticz/plugins/soilmoisturemonitor/'
(SMM) 'Mode4':'100'
(SMM) 'Port':'4223'
(SMM) 'Address':'192.168.N.NNN'
(SMM) 'Key':'SoilMoistureMonitor'
(SMM) 'Mode1':'uTP'
(SMM) 'Mode6':'Debug'
(SMM) 'Name':'SMM'
(SMM) 'DomoticzBuildTime':'2018-12-07 08:49:20'
(SMM) 'Version':'1.0.0'
(SMM) 'Author':'rwbL'
(SMM) 'Mode2':'q2G'
(SMM) 'DomoticzVersion':'4.10264'
(SMM) 'HardwareID':'14'
(SMM) Device count: 0
(SMM) Device new Soil Moisture
(SMM) Creating device 'Soil Moisture'.
(SMM) Device created: SMM - Soil Moisture
(SMM) Heartbeat set: 60
(SMM) Pushing 'PollIntervalDirective' on to queue
(SMM) Processing 'PollIntervalDirective' message
(SMM) Heartbeat interval set to: 60.
Status: (SMM) Entering work loop.
Status: (SMM) Initialized version 1.0.0, author 'rwbL'
```
## Domoticz Log Entry SMM Poll with Debug=True
The Soil Moisture Monitor (SMM) runs every 60 seconds (Heartbeat interval) which is shown in the Domoticz log.
```
(SMM) Processing 'onHeartbeatCallback' message
(SMM) Calling message handler 'onHeartbeat'.
(SMM) onHeartbeat called
(SMM) 192.168.N.NNN:NNNN
(SMM) SMM - Soil Moisture-TF value:2475
(SMM) SMM - Soil Moisture-Domoticz value:22
(SMM - Soil Moisture) Updating device from 0:'' to have values 22:'0'.
(SMM) SMM - Soil Moisture-Segment Display updated
(SMM) SMM - Soil Moisture-RGB LED updated. Brightness=100
(SMM) SMM - Soil Moisture-Update:TF=2475, Dom=22, LED=78
```

## ToDo
Exception handling for communicating with the Master Brick & WiFi extension.

Consider to replace the Tinkerforge Moisture Bricklet as not produced anymore by an alternate solution using the Tinkerforge Analog In Bricklet and a 3rd party Soil Moisture sensor.

## Version
20181206

## APPENDIX
Domoticz Python Plugin Code
```
# Domoticz Home Automation - SoilMoistureMonitor
# Get the moisture from the Tinkerforge Moisture Bricklet, display in the Segment Display 4x7 Bricklet, state in RGB LED Bricklet
# @author Robert W.B. Linn
# @version 1.0.0 (Build 20181206)
#
# NOTE: after every change run
# sudo chmod +x *.*
# sudo systemctl restart domoticz.servicepi
#
# Domoticz Python Plugin Development Documentation:
# https://www.domoticz.com/wiki/Developing_a_Python_plugin
"""
<plugin key="SoilMoistureMonitor" name="Soil Moisture Monitor" author="rwbL" version="1.0.0">
    <description>
        <h2>Soil Moisture Monitor</h2><br/>
        Get the moisture from the Tinkerforge Moisture Bricklet, display in the Segment Display 4x7 Bricklet, state in RGB LED Bricklet.
        <h3>Features</h3>
        <ul style="list-style-type:square">
            <li>Moisture value</li>
            <li>00 - 09 = saturated, 10 - 19 = adequately wet, 20 - 59 = irrigation advice, 60 - 99 = irrigation, 100-200 = Dangerously dry</li>
        </ul>
        <h3>Soil Moisture Device</h3>
        <ul style="list-style-type:square">
            <li>Displays soil moisture value (cp)</li>
            <li>Displays soil moisture value in Segment Display 4x7 with values 0(dry) - 100(wet)</li>
            <li>Indicate soil moisture level in RGB LED red(dry), yellow(irrigation advice), green(adequaly wet)</li>
        </ul>
        <h3>Configuration</h3>
        Requires the HTTP address and Port of the Master Brick WiFi Extention and the UIDs of the Tinkerforge Bricklets Moisture, Segment Display, RGB LED.
    </description>
    <params>
        <param field="Address" label="Host" width="200px" required="true" default="192.168.1.112"/>
        <param field="Port" label="Port" width="75px" required="true" default="4223"/>
        <param field="Mode1" label="UID Moisture Bricklet" width="75px" required="true" default="uTP"/>
        <param field="Mode2" label="UID Segment Bricklet" width="75px" required="true" default="q2G"/>
        <param field="Mode3" label="UID RGB LED Bricklet" width="75px" required="true" default="zMF"/>
        <param field="Mode4" label="RGB LED Brightness" width="75px" required="true" default="100"/>
        <param field="Mode5" label="Check Interval (seconds)" width="75px" required="true" default="60"/>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug" default="true"/>
                <option label="False" value="Normal"/>
            </options>
        </param>
    </params>
</plugin>
"""

## Imports
import Domoticz
import urllib
import urllib.request

# Amend the import path to enable using the Tinkerforge libraries
# Alternate (ensure to update in case newer Python API bindings):
# create folder tinkerforge and copy the binding content, i.e.
# /home/pi/domoticz/plugins/soilmoisturemonitor/tinkerforge
from os import path
import sys
sys.path
sys.path.append('/usr/lib/python3/dist-packages')

import tinkerforge
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_moisture import BrickletMoisture
from tinkerforge.bricklet_segment_display_4x7 import BrickletSegmentDisplay4x7
from tinkerforge.bricklet_rgb_led import BrickletRGBLED

# TF RGB LED digits (according datasheet)
# 0~9,A,b,C,d,E,F
DIGITS = [0x3f,0x06,0x5b,0x4f,
          0x66,0x6d,0x7d,0x07,
          0x7f,0x6f,0x77,0x7c,
          0x39,0x5e,0x79,0x71]

# Set brightness level 0(dark) - 255(brightest)
RGBBRIGHTNESSMIN = 0
RGBBRIGHTNESSMAX = 255

# TF Moisture Bricklet range according test measures
# TF documentation describes the higher the value the more wet (with range 0 - 4095), but ...
# field tests show the other way around in a range 2200(wet) - 3400(dry)
TFMOISTUREDRY = 3400
TFMOISTUREWET = 2200

DOMOTICZMOISTUREDRY = 100
DOMOTICZMOISTUREWET = 0

class BasePlugin:

    def __init__(self):
        # Soil Domoticz heartbeat is set to every 60 seconds. Donot use a higher value as Domoticz message "Error: hardware (N) thread seems to have ended unexpectedly"
        # The Soil Moisture Monitor is read every Parameter.Mode5 seconds. This is triggered by using a hearbeatcounter which is triggered by:
        # (self.HeartbeatCounter * self.HeartbeatInterval) % int(Parameter.Mode5) = 0
        self.HeartbeatInterval = 60
        self.HeartbeatCounter = 0
        return

    def onStart(self):
        Domoticz.Debug("onStart called")
        Domoticz.Debug("Debug Mode:" + Parameters["Mode6"])

        if Parameters["Mode6"] == "Debug":
            self.debug = True
            Domoticz.Debugging(1)
            DumpConfigToLog()

        if (len(Devices) == 0):
            Domoticz.Debug("Device new Soil Moisture")
            # myVar = Domoticz.Device(Name="myDevice", Unit=0, TypeName="", Type=0, Subtype=0, Switchtype=0, Image=0, Options={}, Used=1)
            # Domoticz.Device(Name="Homepage Counter", Unit=1, TypeName="Custom", Options={"Custom": "1;Hits"}).Create()
            Domoticz.Device(Name="Soil Moisture", Unit=1, TypeName="Soil Moisture").Create()
            Domoticz.Debug("Device created: "+Devices[1].Name)

        Domoticz.Debug("Heartbeat set: "+Parameters["Mode5"])
        Domoticz.Heartbeat(self.HeartbeatInterval)

    def onStop(self):
        Domoticz.Debug("Plugin is stopping.")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Debug("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Debug("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Debug("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Debug("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Debug("onDisconnect called")

    def onHeartbeat(self):
        self.HeartbeatCounter = self.HeartbeatCounter + 1
        Domoticz.Log("onHeartbeat called. Counter=" + str(self.HeartbeatCounter * self.HeartbeatInterval) + " (Heartbeat=" + Parameters["Mode5"] + ")")

        # check the heartbeatcounter against the heartbeatinterval
        if (self.HeartbeatCounter * self.HeartbeatInterval) % int(Parameters["Mode5"]) == 0:
            # Get the moisture value
            # Create IP connection
            ipcon = IPConnection()

            # Create device objects
            mb = BrickletMoisture(Parameters["Mode1"], ipcon)
            sb = BrickletSegmentDisplay4x7(Parameters["Mode2"], ipcon)
            lb = BrickletRGBLED(Parameters["Mode3"], ipcon)

            # Connect to brickd using Host and Port
            ipcon.connect(Parameters["Address"], int(Parameters["Port"]))

            # Don't use device before ipcon is connected
            # Get current moisture value
            moisturetf = mb.get_moisture_value()
            Domoticz.Debug(Devices[1].Name + "-TF value:" + str(moisturetf) )
            moisturedom = converttfvalue(moisturetf)
            Domoticz.Debug(Devices[1].Name + "-Domoticz value:" + str(moisturedom) )

            # Moisture Device
            # Update the value - only nValue is used, but mandatory to add an sValue
            Devices[1].Update( nValue=moisturedom, sValue="0")

            # Tinkerforge Bricklet Updates

            # Segment Display set the value between 0(dry) - 100(wet)
            # Inverse the Domoticz moisure value
            moistureled = DOMOTICZMOISTUREDRY - moisturedom
            l = list(str(moistureled))
            # dry
            if  len(l) == 1:
                segments = (DIGITS[0], DIGITS[0], DIGITS[0], DIGITS[int(l[0])])

            # irrigation advice
            if  len(l) == 2:
                segments = (DIGITS[0], DIGITS[0], DIGITS[int(l[0])], DIGITS[int(l[1])])

            # adequate
            if  len(l) == 3:
                segments = (DIGITS[0], DIGITS[int(l[0])], DIGITS[int(l[1])], DIGITS[int(l[2])])

            # not used
            if  len(l) == 4:
                segments = (DIGITS[int(l[0])], DIGITS[int(l[1])], DIGITS[int(l[2])], DIGITS[int(l[3])])

            # Write the moisture value to the display with full brightness without colon
            sb.set_segments(segments, 7, False)
            Domoticz.Debug(Devices[1].Name + "-Segment Display updated")

            # Set the color of the RGB LED indicator
            # The indicator uses own scheme to keep simple: dry < 20; irrigation advice 20-40; wet > 40
            Domoticz.Debug(Devices[1].Name + "-RGB LED updated. Brightness=" + Parameters["Mode4"])
            lbbrightness = int(Parameters["Mode4"])
            if lbbrightness < RGBBRIGHTNESSMIN:
                lbbrightness = RGBBRIGHTNESSMIN
            if lbbrightness > RGBBRIGHTNESSMAX:
                lbbrightness = RGBBRIGHTNESSMIN

            # Turn the LED on with color depending LED value - 0(dry) -100(wet)
            # dry
            if moistureled < 20:
                lb.set_rgb_value(lbbrightness, 0, 0)
            # irrigation advice
            if moistureled >= 20 and moistureled <= 40:
                lb.set_rgb_value(lbbrightness, lbbrightness, 0)
            # wet
            if moistureled > 40:
                lb.set_rgb_value(0, lbbrightness, 0)

            # Disconnect
            ipcon.disconnect()

            # Log Message
            Domoticz.Log(Devices[1].Name + "-Update:TF=" + str(moisturetf)+", Dom="+str(moisturedom)+", LED="+str(moistureled))

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

# Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return

# Convert TF value to Domoticz value between 0(wet) - 100(dry)
# TF: # 2200(wet) - 3400(dry)
# Domoticz: 0(wet) - 100(dry) (> 100 is not used)
# Domoticz: 00 - 09 = saturated, 10 - 19 = adequately wet, 20 - 59 = irrigation advice, 60 - 99 = irrigation, 100-200 = Dangerously dry
def converttfvalue(tfvalue):
    v = 0
    # Avoid dividing by 0
    if tfvalue > TFMOISTUREWET:
        r = TFMOISTUREDRY - TFMOISTUREWET
        # Set the domoticz value using the tf percentage factor of the tf value in the range
        f = (tfvalue - TFMOISTUREWET) / r
        v = DOMOTICZMOISTUREDRY * f
    return int(v)
```
