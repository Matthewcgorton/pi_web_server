#!/usr/local/bin/python3
import socket

from bottle import route, run, request, template,    HTTPResponse, redirect


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
    lcd['msg'][1] = line2
    lcd['msg'][2] = line3
    lcd['msg'][3] = line4

    if backlight is not None:
        lcd['backlight'] = backlight

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
    print("Running webserver")
    run(host=get_ip_address(), port=8080, debug=True, reloader=True)


if __name__ == '__main__':

    main()
