from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

images_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static', 'images'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))


@app.route("/")
def index():
    a1 = os.listdir(f"{images_dir}/Assignment1")
    a2 = os.listdir(f"{images_dir}/Assignment2")
    return render_template("index.html", images_a1=a1, images_a2=a2)


@app.route('/download/<filename>')
def show_static_pdf(filename):
    return send_from_directory(directory=static_dir,
                               filename=f'{filename}.pdf',
                               mimetype='application/pdf')
