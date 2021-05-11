import json
import os
import posixpath

from flask import Flask, render_template, url_for, request

from gray import ImgWorker

app = Flask(__name__)


@app.route('/')
def index():
    names = os.listdir(os.path.join(app.static_folder, 'img'))
    d = {'data': [], 'path': {}}
    for name in names:
        if name.startswith('.') or 'response' in name:
            continue
        d['data'].append(name)
        d['path'][name] = url_for('static', filename=posixpath.join('img', name))
    return render_template('index.html', **d)


@app.route('/handler_image', methods=['POST'])
def handler_image():
    path = request.data.decode('utf-8')
    img = ImgWorker(path[1:])
    img.create_B_matrix()
    img.work_with_b()
    img_name = img.test()

    data = {
        'B': {str(key): val.tolist() for key, val in img.B.items()},
        'C': {str(key): val.tolist() for key, val in img.C.items()},
        'coord': img.coord,
        'h': {str(key): val for key, val in img.h.items()},
        'z': img.zero
    }
    handler_img = url_for('static', filename=posixpath.join('img', img_name))

    return json.dumps({'status': 'ok', 'handler_img': handler_img, 'data': data})


@app.route('/info', methods=['POST'])
def info():
    path = request.data.decode('utf-8')

if __name__ == "__main__":
    img = None
    app.run()
