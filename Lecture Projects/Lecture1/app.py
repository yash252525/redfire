from flask import Flask ,render_template, url_for

app= Flask(__name__)

@app.route("/")
def index():
    return f'''
    <html>
        <head>
        <title>New App</title>
        </head>
        <body>
            <h1>Hello World</h1>
            <p>
            <a href="{url_for('newpage')}">Ref to index.html</a> <br>
            <a href="{url_for('webpage')}">Ref to test.html</a>
            </p>
        </body>
    </html>
    '''


@app.route("/users/<name>")
def user(name):
    return f'Hello, {name}'


@app.route("/newpage1")
def newpage():
    return render_template("index.html")


@app.route("/test")

def webpage():
    return render_template("test.html")


if __name__ in "__main__":
    app.run(debug=True)