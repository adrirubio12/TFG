from flask import Flask, render_template, request
import algoritmo


app = Flask(__name__)


# Rutas de Flask
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/resultados", methods=["GET", "POST"])
def creacion():
    if request.method == "POST":
        edad = int(request.form.get("edad"))
        altura = float(request.form.get("altura"))
        peso = float(request.form.get("peso"))
        sexo = request.form.get("sexo")
        nivel_actividad = request.form.get("nivel_actividad")
        objetivos = request.form.get("objetivos")
        alimentos_seleccionados, ne, rutina = algoritmo.inicializar(
            edad, altura, peso, sexo, nivel_actividad, objetivos
        )
        dieta = algoritmo.generar_dieta(alimentos_seleccionados)
        ruta_imagen = algoritmo.obtener_imagen(nivel_actividad, objetivos)
        tipo_rutina = algoritmo.obtener_tipo_rutina(nivel_actividad)

        return render_template(
            "resultados.html",
            ruta_imagen=ruta_imagen,
            dieta=dieta,
            ne=ne,
            tipo_rutina=tipo_rutina,
            rutina=rutina,
        )


@app.route("/guia")
def guia():
    return render_template("guia.html")


@app.route("/psicologia")
def psi():
    return render_template("psicologia.html")


if __name__ == "__main__":
    app.run(debug=True)
