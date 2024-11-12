import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask_toastr import Toastr

app = Flask(__name__, static_url_path='/static')
toastr = Toastr(app)
UPLOAD_FOLDER = 'temp/files_xml'
ALLOWED_EXTENSIONS = {'xml', 'XML'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    main = render_template('index.html')
    return main

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an

        # empty file without a filename.
        if file.filename == '':
            flash({'title': "ERROR", 
                   'message': "Sin archivo seleccionado",
                   'TOASTR_POSITION_CLASS': "toast-top-center"}, 'error',)
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file', name=filename))

if __name__ == '__main__':
    app.secret_key = "SECRET KEY"
    app.run(host="127.0.0.1", port="5000",debug=True)