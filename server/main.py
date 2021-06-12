import json
import os
import posixpath

from flask import Flask, render_template, url_for, request

from gray import ImgWorker

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

last_img = None
data = {}

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


@app.route('/info', methods=['POST'])
def info():
    path = request.data.decode('utf-8')


@app.route('/handler_image', methods=['POST'])
def handler_image():
    global last_img, data
    resp = request.json
    angle = 10 if resp['angle'] is None else resp['angle']
    img_path = resp['path'][1:]
    if last_img is None or img_path != last_img.img_name:
        print('new img')
        img = ImgWorker(resp['path'][1:], angle)
        img.create_B_matrix()
        img.work_with_b()
        img_name = img.test()
        last_img = img
        data = {
            'B': {str(key): val.tolist() for key, val in img.B.items()},
            'C': {str(key): val.tolist() for key, val in img.C.items()},
            'h': {str(key): val for key, val in img.h.items()},
            'coord': img.coord,
            'z': img.zero,
            'l_max': {str(key): val for key, val in img.l_max_f.items()}
        }
    else:
        print('already have')
        last_img.angle = angle
        img_name = last_img.test()

    handler_img = url_for('static', filename=posixpath.join('img', img_name))
    return json.dumps({'status': 'ok', 'handler_img': handler_img, 'data': data})

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if __name__ == "__main__":
    img = None
    app.run()
