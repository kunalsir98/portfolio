from flask import Flask, render_template

app = Flask(__name__,static_folder='static')

@app.route('/')
def home():
    return render_template('index.html', title="Home")

@app.route('/projects')
def projects():
    return render_template('projects.html', title="Projects")

@app.route('/contact')
def contact():
    return render_template('contact.html', title="Contact")

@app.route('/resources')
def resources():
    return render_template('resources.html', title="resources")


if __name__ == "__main__":
    app.run(debug=True)
