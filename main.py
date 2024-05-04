from flask import Flask, Response, flash, redirect, request, session, url_for
from htpy import Element, body, div, form, h1, head, html
from htpy import input as inpt
from htpy import label, link, script, title

from db import get_db

app = Flask(__name__)
app.secret_key = "ooga booga secret key"


def head_template(*, title_arg: str) -> Element:
    htmx_script = script(
        src="https://unpkg.com/htmx.org@1.9.12",
        integrity="sha384-ujb1lZYygJmzgSwoxRggbCHcjc0rB2XoQrxeTUQyRjrOnlCoYta87iKBWq3EsdM2",
        crossorigin="anonymous",
    )
    return head[
        title[title_arg],
        htmx_script,
        link(href=url_for("static", filename="output.css"), rel="stylesheet"),
    ]


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
            head_template(title_arg="Login"),
            body[
                form(
                    class_="h-screen flex flex-col justify-center items-center",
                    hx_post="/login",
                    hx_target="#error",
                )[
                    h1(class_="text-4xl m-4")["Login"],
                    label["Username"],
                    inpt(
                        class_="border-2 border-blue-600 m-1",
                        type_="text",
                        name="username",
                    ),
                    label["Password"],
                    inpt(
                        class_="border-2 border-blue-600 m-1",
                        type_="text",
                        name="password",
                    ),
                    inpt(class_="border-2 border-blue-500 m-1 p-1", type_="submit"),
                    div(id="error", class_="text-red-400"),
                ],
            ],
        ]
        return str(page)
    else:
        db = get_db()
        c = db.cursor()
        username = request.form["username"]
        password = request.form["password"]
        user = c.execute(
            """
        SELECT * FROM users
        WHERE username=?;
                  """,
            [username],
        ).fetchone()
        db.close()
        print(user)
        users = ["Sovereign"]
        passwords = ["1234"]
        if user == None:
            return "User not registered"
        else:
            if user[1] == password:
                session["username"] = username
                resp = Response("redirect")
                resp.headers["HX-Redirect"] = "/todo"
                return resp
            else:
                return "Incorrect password"
        return


@app.route("/todo")
def todo():
    username = session["username"]
    page = html[head_template(title_arg="Todo"), body[h1[f"Hello {username}"]]]
    return str(page)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
