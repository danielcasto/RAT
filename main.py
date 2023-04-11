from flask import Flask, render_template
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
    data = "Hello from RAT!"
    return render_template("index.html", data = data)

@app.route("/upload", methods = ["POST"])
def upload_files():
    # Define Image File
    # Define Mask File

    # Return matplot image for html

    # TEST Return same image file #
    image_file = request.form["input_1"]
    mask_file = request.form["input_2"]

    return image_file

@app.route("/export")
def export_file():
    # Define exported file
    return

if __name__ == "__main__":
    app.run()