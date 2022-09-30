import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import PyPDF2

from pymongo import MongoClient 

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def mongo_conn():
    try:
        conn = MongoClient(host='localhost',port = 27017)
        print('connected')
        return conn.grid_file
    
    except Exception as e:
        print("error",e)

db = mongo_conn()

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
            new_path = final.replace(" ","_")
            ext_path = new_path.replace("(","")
            ext_path_2 = ext_path.replace(")","")
            ext_path_3 = ext_path_2.replace(",","")
            ext_path_4 = ext_path_3.replace(":","")
            print(ext_path_4)
            

            file = open(str(ext_path_4),'rb')
            content = []
            pdf_reader = PyPDF2.PdfFileReader(file)
            totalpages = pdf_reader.numPages
            for x in range(0,totalpages):
                page = pdf_reader.getPage(x)
                #print(page.extractText(x))
                content.append(page.extractText(x))
                #print("--------------------NEXT PAGE---------------------------")
                a = ''.join(content)
            db.users.insert_one({'file name':request.form.get('filename'),'content' : a})







            return "file uploaded successfully" 
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type="text" name="filename">
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


    

