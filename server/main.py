import os

from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
def index():
    names = os.listdir(os.path.join(app.static_folder, 'img'))
    d = {'data': [], 'path': {}}
    for name in names:
        if name.startswith('.'):
            continue
        d['data'].append(name)
        d['path'][name] = url_for('static', filename=os.path.join('img', name))
    return render_template('index.html', **d)


if __name__ == "__main__":
    app.run()
