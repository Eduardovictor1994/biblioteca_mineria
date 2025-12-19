from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads/libros"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Categorías permitidas
CATEGORIAS = ["Geología", "Perforación", "Voladura"]

@app.route("/")
def index():
    categoria = request.args.get("categoria")
    libros = []

    for archivo in os.listdir(UPLOAD_FOLDER):
        if archivo.endswith(".pdf"):
            partes = archivo.split("__")
            cat = partes[0] if len(partes) > 1 else "Sin categoría"

            if not categoria or categoria == cat:
                libros.append({
                    "nombre": archivo,
                    "categoria": cat
                })

    return render_template("index.html", libros=libros, categorias=CATEGORIAS, categoria_actual=categoria)


@app.route("/subir", methods=["GET", "POST"])
def subir():
    if request.method == "POST":
        archivo = request.files["libro"]
        categoria = request.form["categoria"]

        if archivo and archivo.filename.endswith(".pdf"):
            nombre = f"{categoria}__{archivo.filename}"
            archivo.save(os.path.join(app.config["UPLOAD_FOLDER"], nombre))
            return redirect(url_for("index"))

    return render_template("subir.html", categorias=CATEGORIAS)


@app.route("/eliminar/<nombre>")
def eliminar(nombre):
    ruta = os.path.join(app.config["UPLOAD_FOLDER"], nombre)
    if os.path.exists(ruta):
        os.remove(ruta)
    return redirect(url_for("index"))


@app.route("/descargar/<nombre>")
def descargar(nombre):
    return send_from_directory(app.config["UPLOAD_FOLDER"], nombre, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
