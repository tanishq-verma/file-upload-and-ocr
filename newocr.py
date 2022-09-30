import os
from pprint import pprint
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import PyPDF2


UPLOAD_FOLDER = '/Users/tanishq/flask/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "no file added"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "no file added"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            final = os.path.join(UPLOAD_FOLDER,file.filename)
            print(final)

            newfinal = final.replace(" ","_")
            newfinal = newfinal.replace("(","")
            newfinal = newfinal.replace(")","")

            file = open(str(newfinal),'rb')
            content = []
            pdf_reader = PyPDF2.PdfFileReader(file)
            totalpages = pdf_reader.numPages
            for x in range(0,totalpages):
                page = pdf_reader.getPage(x)
                print(page.extractText(x))
                content.append(page.extractText(x))
                print("--------------------NEXT PAGE---------------------------")
                a = ''.join(content)







            return "file uploaded successfully ||| OCR CONTENT --> " + a 
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''