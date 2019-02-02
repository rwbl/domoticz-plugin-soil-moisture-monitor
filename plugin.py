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
        # The Domoticz heartbeat is set to every 60 seconds. Do not use a higher value as Domoticz message "Error: hardware (N) thread seems to have ended unexpectedly"
        # The Soil Moisture Monitor is read every Parameter.Mode5 seconds. This is determined by using a hearbeatcounter which is triggered by:
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
