from flask import Flask, flash, render_template, redirect, request, send_from_directory
from PIL import Image
import base64
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

from os import path, listdir, makedirs

from backend.masker import Masker
from backend.visualization import plot_image
from backend.atlas import WaxholmAtlas


UPLOADS_FOLDER = "uploads"
OUTPUTS_FOLDER = "outputs"
ATLAS_PATH = "../Waxholm-v4"

makedirs(UPLOADS_FOLDER, exist_ok=True)
makedirs(OUTPUTS_FOLDER, exist_ok=True)


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = OUTPUTS_FOLDER

@app.route("/")
def index():
    
    test_image = Image.open("static/resources/Render_Placeholder.png")
    data = io.BytesIO()
    test_image.save(data, "PNG")
    encoded_img_data = base64.b64encode(data.getvalue())

    return render_template("index.html", image_data=encoded_img_data.decode('utf-8'))

@app.route("/upload", methods = ["POST", "GET"])
def upload_files():
    image_file = request.files["image_file"]
    mask_file = request.files["mask_file"]

    labels = []

    if "whole_hypothalamus" in request.form:
        labels.append(request.form["whole_hypothalamus"])

    if "amygdala" in request.form:
        labels.append(request.form["amygdala"])

    if "ventral_tegmental_area" in request.form:
        labels.append(request.form["ventral_tegmental_area"])
    '''Quarantine END'''

    if image_file.filename == "" or mask_file.filename == "":
        flash("Please select a mask and image file.")
        return redirect(request.url)

    image_file_path = path.join(UPLOADS_FOLDER, "image.nii.gz")
    mask_file_path = path.join(UPLOADS_FOLDER, "mask.nii.gz")
    aligned_image_path = path.join(OUTPUTS_FOLDER, "aligned_img.nii.gz")

    roi_mask_path = path.join(OUTPUTS_FOLDER, "roi_mask.nii.gz")
    roi_masked_image_path = path.join(OUTPUTS_FOLDER, "roi_masked_img.nii.gz")

    image_file.save(image_file_path)
    mask_file.save(mask_file_path)

    masker = Masker(image_path=image_file_path, image_mask_path=mask_file_path, atlas_path=ATLAS_PATH)
    masker.alignToAtlas()\
        .exportAlignedImage(path = aligned_image_path)\
        .exportROIMask(roi_labels = labels, path = roi_mask_path)\
        .exportROIMaskedImage(mask_path = roi_mask_path, result_path = roi_masked_image_path)

    fig = Figure(figsize=(10,10))
    plt = plot_image(aligned_image_path, overlay_path = masker.atlas.map_path, figure = fig)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)

    encoded_img_data = base64.b64encode(output.getvalue())

    return render_template("index.html", image_data=encoded_img_data.decode('utf-8'))

@app.route("/export/aligned_img.nii.gz")
def export_aligned():
    return send_from_directory(path.join(app.root_path, OUTPUTS_FOLDER), "aligned_img.nii.gz")

@app.route("/export/roi_mask.nii.gz")
def export_roi_mask():
    return send_from_directory(path.join(app.root_path, OUTPUTS_FOLDER, "roi_mask.nii.gz"))

@app.route("/export/roi_masked_img.nii.gz")
def export_roi_masked():
    return send_from_directory(path.join(app.root_path, OUTPUTS_FOLDER, "roi_masked_img.nii.gz"), "aligned_img.nii.gz")

@app.route("/export")
def export_file():
    return send_from_directory(path.join(app.root_path, OUTPUTS_FOLDER), "aligned_img.nii.gz")

if __name__ == "__main__":
    app.run()