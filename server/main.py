import json
import os
from flask import Flask, render_template, url_for, request
from gray import ImgWorker


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
        print(d)
    return render_template('index.html', **d)


@app.route('/handler_image', methods=['POST'])
def handler_image():
    path = request.data.decode('utf-8')
    img = ImgWorker('server' + path)
    img.create_B_matrix()
    img.work_with_b()
    img.test()

    print(path)
    return json.dumps({'status': 'ok'})

if __name__ == "__main__":
    img = None
    app.run()
