from keras.models import load_model
from keras.preprocessing import image
import numpy as np
from flask import Flask, render_template, request, make_response, session, redirect, url_for, flash, abort, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'randomterserah'

model = load_model('model.h5')

# upload gambar
ALLOWED_EXTENSION = set(['png','jpeg','jpg'])
app.config['UPLOAD_FOLDER'] = 'static'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSION

@app.route('/', methods=['GET','POST'])
def uploadFile():
    if request.method == 'POST':
        
        file = request.files['file']
        
        if 'file' not in request.files:
            return redirect(request.url)
        
        if file.filename == '':
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            _path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            raw_img = image.load_img(_path, target_size=(64, 64))
            raw_img = image.img_to_array(raw_img)
            raw_img = np.expand_dims(raw_img, axis=0)
            raw_img = raw_img/255
            prediction = model.predict_classes(raw_img)[0][0]
            if (prediction):
                return render_template('index.html', awan="Awan Cumulus", show=None, path=_path)
            else:
                return render_template('index.html', awan="Awan Cumulonimbus", show=None, path=_path)
            
            # print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return 'file berhasil disave di ...' + filename
                
    return render_template('index.html', show="d-none", path=None)

@app.route('/post', methods=['POST'])
def post_img():
    file = request.files['file']
        
    if 'file' not in request.files:
        return redirect(request.url)
        
    if file.filename == '':
        return redirect(request.url)
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        _path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        raw_img = image.load_img(_path, target_size=(64, 64))
        raw_img = image.img_to_array(raw_img)
        raw_img = np.expand_dims(raw_img, axis=0)
        raw_img = raw_img/255
        prediction = model.predict_classes(raw_img)[0][0]
        if (prediction):
            resp = jsonify({
                "prediksi":"Cumulus",
            })
            resp.status_code = 202
            return resp
        else:
            resp = jsonify({
                "prediksi":"Cumulonimbus",
            })
            resp.status_code = 202
            return resp

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status':404,
        'message': 'Not Found ' + request.url 
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

if __name__ == "__main__":
    app.run(debug=True)