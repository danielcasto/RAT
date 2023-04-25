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
from download_waxholm import download_waxholm_v4


UPLOADS_FOLDER = "uploads"
OUTPUTS_FOLDER = "outputs"
ATLAS_PATH = "Waxholm-v4"

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
    print("\n/upload request received.")

    image_file = request.files["image_file"]
    mask_file = request.files["mask_file"]

    labels = []

    if "whole_hypothalamus" in request.form:
        labels.append(request.form["whole_hypothalamus"])

    if "amygdala" in request.form:
        labels.append(request.form["amygdala"])

    if "ventral_tegmental_area" in request.form:
        labels.append(request.form["ventral_tegmental_area"])

    print("\nROI Labels: ", labels)

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

    print("Running pipeline... (This will take a while)")
    print("Step 1: align to atlas...")
    masker.alignToAtlas()

    print("Step 2: export aligned image...")
    masker.exportAlignedImage(path = aligned_image_path)

    print("Step 3: export ROI mask...")
    masker.exportROIMask(roi_labels = labels, path = roi_mask_path)

    print("Step 4: export ROI masked image...")
    masker.exportROIMaskedImage(mask_path = roi_mask_path, result_path = roi_masked_image_path)

    print("Pipeline finished. Files saved to output directory")

    print("Making figure... (This will take a while)")
    fig = Figure(figsize=(10,10))
    plt = plot_image(aligned_image_path, overlay_path = masker.atlas.map_path, figure = fig)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)

    encoded_img_data = base64.b64encode(output.getvalue())

    print("Returning figure...")
    return render_template("index.html", image_data=encoded_img_data.decode('utf-8'))

@app.route("/export/aligned_img.nii.gz",  methods = ["GET"])
def export_aligned_img():
    print("/export/aligned_img.nii.gz request received. Sending back file.")
    return send_from_directory(path.join(app.root_path, OUTPUTS_FOLDER), "aligned_img.nii.gz")

@app.route("/export/roi_mask.nii.gz", methods = ["GET"])
def export_roi_mask():
    print("/export/roi_mask.nii.gz request received. Sending back file.")
    return send_from_directory(path.join(app.root_path, OUTPUTS_FOLDER), "roi_mask.nii.gz")

@app.route("/export/roi_masked_img.nii.gz", methods = ["GET"])
def export_roi_masked_img():
    print("/export/roi_masked_img.nii.gz request received. Sending back file.")
    return send_from_directory(path.join(app.root_path, OUTPUTS_FOLDER), "roi_masked_img.nii.gz")

@app.route("/export") # TODO consider deleting
def export_file():
    return send_from_directory(path.join(app.root_path, OUTPUTS_FOLDER), "aligned_img.nii.gz")

if __name__ == "__main__":
    download_waxholm_v4()
    app.run()