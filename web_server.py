#!/usr/local/bin/python3
import socket

from bottle import route, run, request, template, HTTPResponse, redirect

import smbus
import time

# Define some device parameters

I2C_ADDR = 0x27  # I2C device address
LCD_WIDTH = 20   # Maximum characters per line

# Define some device constants
LCD_CHR = 1  # Mode - Sending data
LCD_CMD = 0  # Mode - Sending command

LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94  # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4  # LCD RAM address for the 4th line

LCD_BACKLIGHT = 0x08  # On
# LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100  # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

# Open I2C interface
# bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1)    # Rev 2 Pi uses 1


def lcd_init():
    # Initialise display
    lcd_byte(0x33, LCD_CMD)  # 110011 Initialise
    lcd_byte(0x32, LCD_CMD)  # 110010 Initialise
    lcd_byte(0x06, LCD_CMD)  # 000110 Cursor move direction
    lcd_byte(0x0C, LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
    lcd_byte(0x28, LCD_CMD)  # 101000 Data length, number of lines, font size
    lcd_byte(0x01, LCD_CMD)  # 000001 Clear display
    time.sleep(E_DELAY)


def lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = the data
    # mode = 1 for data
    #        0 for command

    bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
    bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

    # High bits
    bus.write_byte(I2C_ADDR, bits_high)
    lcd_toggle_enable(bits_high)

    # Low bits
    bus.write_byte(I2C_ADDR, bits_low)
    lcd_toggle_enable(bits_low)


def lcd_toggle_enable(bits):
    # Toggle enable
    time.sleep(E_DELAY)
    bus.write_byte(I2C_ADDR, (bits | ENABLE))
    time.sleep(E_PULSE)
    bus.write_byte(I2C_ADDR, (bits & ~ENABLE))
    time.sleep(E_DELAY)


def lcd_string(message, line):
    # Send string to display

    message = message.ljust(LCD_WIDTH, " ")

    lcd_byte(line, LCD_CMD)

    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)


# ####################################

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


lcd = {'msg': ["default msg line 1",
               "default msg line 2",
               "default msg line 3",
               "default msg line 4"
               ],
       'backlight': 1}

# ########################
# backend
# ########################


def lcd_clear():
    return lcd_set(backlight=None)


def lcd_msg():
    return lcd


def lcd_set(line1="", line2="", line3="", line4="", backlight=None):
    lcd['msg'][0] = line1
    lcd_string(lcd['msg'][0], LCD_LINE_1)

    lcd['msg'][1] = line2
    lcd_string(lcd['msg'][1], LCD_LINE_2)

    lcd['msg'][2] = line3
    lcd_string(lcd['msg'][2], LCD_LINE_3)

    lcd['msg'][3] = line4
    lcd_string(lcd['msg'][3], LCD_LINE_4)

    if backlight is not None:
        lcd['backlight'] = backlight

    print("Setting LCD")

    return lcd


# ########################
# UI
# ########################

@route('/lcd')
@route('/lcd/msg')
def ui_lcd_msg():

    print(f"Backlight is set to {lcd_msg()['backlight']}")
    print(f"Message is {lcd_msg()['msg']}")
    return template("message", lcd=lcd_msg())


@route('/lcd/clear')
def ui_lcd_clear():
    lcd_clear()
    # redirect("/lcd/msg")
    return HTTPResponse(status=303,
                        body='',
                        Location='http://10.0.0.78:8080/lcd/msg')


@route('/lcd/set', method='GET')
def ui_lcd_set_display_form():
    return template("set_msg", form_name='/lcd/set')


@route('/lcd/set', method='POST')
def ui_lcd_set():
    line1 = request.forms.get('line1')
    line2 = request.forms.get('line2')
    line3 = request.forms.get('line3')
    line4 = request.forms.get('line4')

    lcd_set(line1, line2, line3, line4)
    redirect("/lcd/msg")


# ########################
# API
# ########################

@route('/api/0/lcd/msg')
def api_lcd_msg():
    print(f"Backlight is set to {lcd['backlight']}")
    print(f"Message is {lcd['msg']}")
    # return template("Current message is: {{ msg }}", msg=lcd['msg'])
    return template("message", lcd=lcd, state='success', action='get_msg')


@route('/api/0/lcd/clear')
def api_lcd_clear():
    lcd['msg'] = ["", "", "", ""]
    # return template("message has been cleared\nCurrent message is: {{msg}}", msg=lcd['msg'])
    return template("message", lcd=lcd, state='success', action='clear')


@route('/api/0/lcd/set')
def api_lcd_set():

    allowed_keys = ('line1', 'line2', 'line3', 'line4')

    for key in request.query.keys():
        if key not in allowed_keys:
            return template('bad key {{key}}', key=key)

    line1 = request.query.line1 or ""
    line2 = request.query.line2 or ""
    line3 = request.query.line3 or ""
    line4 = request.query.line4 or ""

    print(str(request.query.keys()))

    lcd_set(line1, line2, line3, line4)

    return template("message", lcd=lcd, state='success', action='set')


@route('/login')
def login():
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>
'''


@route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    # if check_login(username, password):
    return template("<p>Your login information was correct. {{username}}:{{password}}</p>", username=username, password=password)
    # else:
    #     return "<p>Login failed.</p>"


@route('/')
def greet(name='Stranger'):
    return template('Hello {{name}}, how are you?', name=name)


@route('/test/<pagename>')            # matches /wiki/Learning_Python
def show_wiki_page(pagename):
    return template("Pagename is {{pagename}}", pagename=pagename)


@route('/<action>/<user>')            # matches /follow/defnull
def user_api(action, user):
    return template("Action: {{action}}, User: {{user}}", action=action, user=user)


@route('/foruma')
def display_forum():
    forum_id = request.query.id
    page = request.query.page or '1'
    return template('Forum ID: {{id}} (page {{page}})', id=forum_id, page=page)


def main():
    print("Initializing LCD")
    lcd_init()
    lcd_set(line1="starting web server")

    print("Running webserver")
    run(host=get_ip_address(), port=8080, debug=True, reloader=True)

    # while True:
    #     # # Send some test
    #     lcd_string("RPiSpy         <", LCD_LINE_1)
    #     lcd_string("I2C LCD        <", LCD_LINE_2)
    #
    #     time.sleep(3)
    #
    #     # Send some more text
    #     lcd_string(">         RPiSpy", LCD_LINE_1)
    #     lcd_string(">        I2C LCD", LCD_LINE_2)
    #
    #     time.sleep(3)


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(0x01, LCD_CMD)
