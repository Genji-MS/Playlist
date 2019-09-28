from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    """Return homepage"""
    return render_template('home.html', msg='flask flask baby~')

if app.name == '__main__':
    app.run(debug=True)