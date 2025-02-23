import math
import board
import os
import wifi
import socketpool
import time
import adafruit_ntp
import displayio
import terminalio
import digitalio
import ssl
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from adafruit_bitmap_font import bitmap_font
from displayio import Bitmap
from adafruit_display_text import label

wifi.radio.connect(os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD"))

test = board.I2C()
##test.try_lock()
##print("I2C addresses found:", [hex(device_address) for device_address in test.scan()])
test.unlock()

pool = socketpool.SocketPool(wifi.radio)
ntp = adafruit_ntp.NTP(pool)
utc = time.mktime(ntp.datetime)
starttime = int(time.monotonic())

my_mqtt_topic_hello = "me/feeds/hello"  # the topic we send on
my_mqtt_topic_light = "me/feeds/light"  # the topic we receive on (could be the same)

# Set up a MiniMQTT Client
mqtt_client = MQTT.MQTT(
    broker=os.getenv("mqtt_broker"),
    port=int(os.getenv("mqtt_port")),
    username=os.getenv("mqtt_username"),
    password=os.getenv("mqtt_password"),
    socket_pool=socketpool.SocketPool(wifi.radio),
    ssl_context=ssl.create_default_context(),
)

# Called when the client is connected successfully to the broker
def connected(client, userdata, flags, rc):
    print("Connected to MQTT broker!")
    
    client.subscribe( my_mqtt_topic_light) # say I want to listen to this topic
        
# Called when the client is disconnected
def disconnected(client, userdata, rc):
    print("Disconnected from MQTT broker!")

# Called when a topic the client is subscribed to has a new message
def message(client, topic, message):
    print("New message on topic {0}: {1}".format(topic, message))
    val = 0
    try: 
        val = int(message)  # attempt to parse it as a number
    except ValueError:
        pass
    print("setting LED to color:",val)
    # led.fill(val)  # if we had leds
    
# Set the callback methods defined above
mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected
mqtt_client.on_message = message

print("Connecting to MQTT broker...")
mqtt_client.connect()

last_msg_send_time = 0

##Display is 240x135
##spleen = 4 Lines x 20 Characters at 12x24
display = board.DISPLAY
fontlgr = bitmap_font.load_font("fonts/LeagueGothic-Regular-36.bdf")
fontlsb = bitmap_font.load_font("fonts/LeagueSpartan-Bold-16.bdf")
fontlb = bitmap_font.load_font("fonts/LibreBodoniv2002-Bold-27.bdf")
spleen = bitmap_font.load_font("fonts/spleen-12x24.bdf")

# Button setup
button0 = digitalio.DigitalInOut(board.D0)
button0.switch_to_input(pull=digitalio.Pull.UP)

button1 = digitalio.DigitalInOut(board.D1)
button1.switch_to_input(pull=digitalio.Pull.DOWN)

button2 = digitalio.DigitalInOut(board.D2)
button2.switch_to_input(pull=digitalio.Pull.DOWN)

pumptime = 0
gpm = 10
dpg = 3.50
gallons = 0
price = 0

line1 = str(f'Select Grade\n')
line2 = str(f'D0 93 $5.02\n')
line3 = str(f'D1 89 $4.20\n')
line4 = str(f'D2 87 $3.50\n')


##  87  89  93  Diesel

while 0 < 1:
    runtime = int(time.monotonic())
    utctime = int(utc - starttime + runtime) % 86400
    if not button0.value:
        dpg = 5.02
        pumptime += 0.2
        gallons += gpm / 300
        price += dpg * gpm /300
    if button1.value:
        dpg = 4.20
        pumptime += 0.2
        gallons += gpm / 300
        price += dpg * gpm /300
    if button2.value:
        dpg = 3.50
        pumptime += 0.2
        gallons += gpm / 300
        price += dpg * gpm /300
    #gallons = pumptime / 60 * gpm
    #price = gallons * dpg
    if pumptime > 0:
        line1 = str(f'Current Time: {utctime // 3600:2}:{utctime % 3600 // 60:2}\n')
        line2 = '\n'
        line3 = str(f'      {gallons:.2f} Gal\n')
        line4 = str(f'    S {price:.2f}\n')
    disptext = line1 + line2 + line3 + line4
    text_area = label.Label(spleen, text = disptext, y = 15)
    display.root_group = text_area
    #mqtt_client.loop(timeout=1)  # see if any messages to me
    
    if time.monotonic() - last_msg_send_time > 3.0:  # send a message every 3 secs
        last_msg_send_time = time.monotonic()
        msg = "hi there! time is "+str(time.monotonic())
        print("sending MQTT msg..", msg)
        mqtt_client.publish( my_mqtt_topic_hello, msg )
    time.sleep(0.2)
