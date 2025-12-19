from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)

BASE_UPLOAD = "uploads/libros"
CATEGORIAS = ["Geologia", "Perforacion", "Voladura"]

# Crear carpetas
for cat in CATEGORIAS:
    os.makedirs(os.path.join(BASE_UPLOAD, cat), exist_ok=True)

@app.route("/")
def index():
    biblioteca = {}
    for cat in CATEGORIAS:
        ruta = os.path.join(BASE_UPLOAD, cat)
        biblioteca[cat] = os.listdir(ruta)
    return render_template("index.html", biblioteca=biblioteca)

@app.route("/subir", methods=["GET", "POST"])
def subir():
    if request.method == "POST":
        archivo = request.files["libro"]
        categoria = request.form["categoria"]

        if archivo and archivo.filename.endswith(".pdf"):
            ruta = os.path.join(BASE_UPLOAD, categoria, archivo.filename)
            archivo.save(ruta)
            return redirect(url_for("index"))

    return render_template("subir.html", categorias=CATEGORIAS)

@app.route("/descargar/<categoria>/<nombre>")
def descargar(categoria, nombre):
    return send_from_directory(os.path.join(BASE_UPLOAD, categoria), nombre, as_attachment=True)

@app.route("/eliminar/<categoria>/<nombre>")
def eliminar(categoria, nombre):
    os.remove(os.path.join(BASE_UPLOAD, categoria, nombre))
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
