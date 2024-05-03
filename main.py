from flask import Flask
from htpy import body, h1, head, html, title

app = Flask(__name__)
app.secret_key = "ooga booga secret key"


@app.route("/")
def index():
    page = html[head[title["Hello World"]], body[h1["Hello World"]]]
    return str(page)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8080")
