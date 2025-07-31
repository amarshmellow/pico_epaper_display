from epd_driver import EPD_2in13_V4_Landscape, EPD_2in13_V4_Portrait
import network
import time
import ntptime
import machine

epd = EPD_2in13_V4_Landscape()

epd.Clear()
epd.fill(0xff)

ssid = "VM657945"
password = "fourwordsalluppercase1A"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

print('Connecting to network...')
wlan.connect(ssid, password)

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('Waiting for connection...')
    time.sleep(1)

# googled wifi connection script

if wlan.status() != 3:
    raise RuntimeError('Network connection failed')
else:
    print("Connected.")
    epd.fill_rect(0, 0, epd.width, epd.height, 0xff)
    epd.text('Connected to Wi-Fi!', 10, 10, 0x00)
    epd.display(epd.buffer)
    print('IP address: {}'.format(wlan.ifconfig()[0]))
time.sleep(1)
epd.fill_rect(0, 0, epd.width, epd.height, 0xff)
epd.display(epd.buffer)

# end

rtc = machine.RTC()

# Year, Month, Day, Weekday, Hour, Minute, Second, Millisecond
rtc.datetime((2000, 1, 1, 0, 0, 0, 0, 0))

print(time.localtime())

print("Synchronizing time with NTP...")
try:
    ntptime.settime()
    print("Time synchronized.")
except OSError as e:
    print(f"Error synchronizing time: {e}. Check network connection or NTP server.")

time.sleep(2)

dstadjust = 1

while True:
    current_time = time.localtime()
    timesec = current_time[5]
    timemin = current_time[4]
    timehourpre = current_time[3]
    
    timehourpost = (timehourpre + dstadjust) % 24
    
    timesec = str(timesec)
    timemin = str(timemin)
    timehourpost = str(timehourpost)
    
    timefin = timehourpost + ":" + timemin + ":" + timesec
    
    epd.fill_rect(0, 10, epd.width, 20, 0xff)
    
    epd.text(timefin, 0, 10, 0x00)
    
    epd.displayPartial(epd.buffer) 
    
    time.sleep(1)