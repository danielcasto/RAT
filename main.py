from flask import Flask, render_template
from flask import request
import time
from PIL import Image
import base64
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

@app.route("/")
def index():
    
    test_image = Image.open("static/resources/Render_Placeholder.png")
    data = io.BytesIO()
    test_image.save(data, "PNG")
    encoded_img_data = base64.b64encode(data.getvalue())

    return render_template("index.html", image_data=encoded_img_data.decode('utf-8'))

@app.route("/upload", methods = ["POST"])
def upload_files():
    # Define Image File
    # Define Mask File

    # Return matplot image for html

    # TEST Return same image file #
    image_file = request.files['input_1']
    mask_file = request.files.get('input_2', '')

    # Change this to appropriate time
    time.sleep(1)

    
    fig = Figure()
    #bg_img = plt.imread("static/resources/Render_Placeholder.png")
    axis = fig.add_subplot(1, 1, 1)
    xs = np.random.rand(100)
    ys = np.random.rand(100)
    axis.plot(xs, ys)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)

    # Use this line for matplot
    encoded_img_data = base64.b64encode(output.getvalue())

    # Use these lines for image - Does not work
    #image_test = Image.open(image_file.stream)
    #data = io.BytesIO()
    #image_test.save(data, "PNG")
    #encoded_img_data = base64.b64encode(data.getvalue())
    # ^^^^

    return render_template("index.html", image_data=encoded_img_data.decode('utf-8'))

@app.route("/export")
def export_file():
    # Define exported file
    return

if __name__ == "__main__":
    app.run()