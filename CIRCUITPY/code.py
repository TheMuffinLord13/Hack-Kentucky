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

localoffset = int( 300 * float(os.getenv("LONGITUDE_OFFSET")))
localname = os.getenv("LONGITUDE_NAME")
locallong = os.getenv("LONGITUDE_OFFSET")

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
    time.sleep(0.2)
