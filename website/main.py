from flask import Flask
from requests_html import HTMLSession
from datetime import datetime


app = Flask(__name__)


def get_word():
    try:
        f = open("word.txt", "r")
        text = f.read()
        f.close()
        date = datetime.strptime(text.split("=")[0], "%d/%m/%Y").date()
        if date >= datetime.now().date():
            return text.split("=")[1]
    except:
        pass

    session = HTMLSession()
    headers = {'User-Agent': 'Defined', 'referer': 'https://www.nytimes.com/', 'authority': 'pnytimes.chartbeat.net', 'Content-Type': 'application/json', 'accept': 'application/json'}
    r = session.get("https://www.nytimes.com/games/wordle/index.html", headers = headers)
    word = str.upper(r.html.render(script="(new window.wordle.bundle.GameApp).solution"))

    f = open("word.txt", "w+")
    f.write(datetime.today().strftime("%d/%m/%Y") + "=" + word)
    f.close()

    return word


@app.route('/')
def display_word():
    return "<h1>" + get_word() + "</h1>"