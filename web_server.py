#!/usr/local/bin/python3
import sys
from bottle import route, run
from bottle import template

@route('/hello')
def hello():
    return "Hello World!"

@route('/')
@route('/hello/<name>')
def greet(name='Stranger'):
    return template('Hello {{name}}, how are you?', name=name)



@route('/test/<pagename>')            # matches /wiki/Learning_Python
def show_wiki_page(pagename):
    print(f"Pagename is {pagename}")

@route('/<action>/<user>')            # matches /follow/defnull
def user_api(action, user):
    print(f"Action: {action}, User: {user}")


def main():
    print("Running webserver")
    run(host='localhost', port=8080, debug=True)


if __name__ == '__main__':

    main()
