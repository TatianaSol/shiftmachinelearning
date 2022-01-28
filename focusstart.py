import os
from flask import Flask, flash, request, redirect
from werkzeug.utils import secure_filename
from pydub import AudioSegment
import librosa
import librosa.display
import matplotlib.pyplot as plt


UPLOAD_FOLDER = "C:/Users/Home/PycharmProjects/Geekbrains/focusstart/"
ALLOWED_EXTENSIONS = {'mp3'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            plt.figure(figsize=(14, 5))
            dst = "test.wav"
            sound = AudioSegment.from_mp3(filename)
            sound.export(dst, format="wav")
            out, samples = librosa.load(dst)
            stft_array = librosa.stft(out)
            stft_array_db = librosa.amplitude_to_db(abs(stft_array))
            librosa.display.specshow(stft_array_db, sr=samples, x_axis='time', y_axis='hz')
            plt.colorbar()
            plt.show()

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
