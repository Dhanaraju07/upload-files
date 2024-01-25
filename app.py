from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

app.config["UPLOAD_FOLDER_MEDIA"] = 'static/mediaFiles'
app.config["ALLOWED_EXTENSIONS"] = {'png', 'mp3', 'mp4'}

upload_file = None

def allowed_file_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

def get_uploaded_files():
    upload_folder = app.config["UPLOAD_FOLDER_MEDIA"]
    file_list = []
    for file_name in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, file_name)
        if os.path.isfile(file_path):
            file_list.append(file_name)
    return file_list

@app.route('/', methods=["GET", "POST"])
def home():
    global upload_file

    if request.method == "POST":
        file = request.files['file']
        
        if file and allowed_file_extension(file.filename):
            file.save(os.path.join(app.config["UPLOAD_FOLDER_MEDIA"], file.filename))
            upload_file = file.filename
            return redirect(url_for('home'))

        return render_template("index.html", msg="Invalid file extension. Please upload a .png, .mp3, or .mp4 file.")

    files = get_uploaded_files()
    return render_template('index.html', msg="Please Choose a File", files=files, upload_file=upload_file)

@app.route('/files')
def show_files():
    files = get_uploaded_files()
    return render_template('files.html', files=files)

if __name__ == "__main__":
    app.run(debug=True)
