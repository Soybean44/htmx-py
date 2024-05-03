import htpy
from flask import Flask, Response, flash, redirect, request, session
from htpy import Element, body, div, form, h1, head, html, script, title

app = Flask(__name__)
app.secret_key = "ooga booga secret key"


def htmx_script() -> Element:
    return script(
        src="https://unpkg.com/htmx.org@1.9.12",
        integrity="sha384-ujb1lZYygJmzgSwoxRggbCHcjc0rB2XoQrxeTUQyRjrOnlCoYta87iKBWq3EsdM2",
        crossorigin="anonymous",
    )


@app.route("/")
def index():
    if "user" in session:
        return redirect("/greet")
    else:
        return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        page = html[
            head[title["login"], htmx_script()],
            body[
                form(hx_post="/login", hx_target="#error")[
                    htpy.input({"type": "text", "name": "user"}),
                    htpy.input({"type": "text", "name": "password"}),
                    htpy.input({"type": "submit"}),
                ],
                div("#error", style="color: red"),
            ],
        ]
        return str(page)
    else:
        user = request.form["user"]
        password = request.form["password"]
        users = ["Sovereign"]
        passwords = ["1234"]
        if user in users:
            if password in passwords:
                session["user"] = user
                resp = Response("redirect")
                resp.headers["HX-Redirect"] = "/greet"
                return resp
            else:
                return "Incorrect password"
        else:
            return "User not registered"
        return


@app.route("/greet")
def greet():
    user = session["user"]
    page = html[head[title["Greeting"]], body[h1[f"Hello {user}"]]]
    return str(page)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8080")
