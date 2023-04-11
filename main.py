from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    data = "Hello from RAT!"
    return render_template("index.html", data = data)

@app.route("/upload", methods = ["POST"])
def upload_image():
    # Define Image File
    return
def upload_mask():
    # Define Mask File
    return

@app.route("/export")
def export_file():
    # Define exported file
    return

if __name__ == "__main__":
    app.run()