from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads/libros"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    libros = os.listdir(UPLOAD_FOLDER)
    return render_template("index.html", libros=libros)

@app.route("/subir", methods=["GET", "POST"])
def subir():
    if request.method == "POST":
        archivo = request.files.get("libro")
        if archivo and archivo.filename.endswith(".pdf"):
            archivo.save(os.path.join(app.config["UPLOAD_FOLDER"], archivo.filename))
            return redirect(url_for("index"))
    return render_template("subir.html")

@app.route("/descargar/<nombre>")
def descargar(nombre):
    return send_from_directory(app.config["UPLOAD_FOLDER"], nombre, as_attachment=True)

# ❌ NO uses app.run() en Render
# Render usa Gunicorn

