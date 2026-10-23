from flask import Flask, render_template, request, send_file
from io import BytesIO
import base64
from fractais import gerar_fractal

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    imagem = None
    erro = None
    valores = {
        "tipo": "mandelbrot",
        "real": "-0.5",
        "imaginaria": "0",
        "passo": "0.01",
        "iteracoes": "150",
    }

    if request.method == "POST":
        valores["tipo"] = request.form.get("tipo", "mandelbrot")
        valores["real"] = request.form.get("real", "-0.5")
        valores["imaginaria"] = request.form.get("imaginaria", "0")
        valores["passo"] = request.form.get("passo", "0.01")
        valores["iteracoes"] = request.form.get("iteracoes", "150")

        try:
            real = float(valores["real"].replace(",", "."))
            imaginaria = float(valores["imaginaria"].replace(",", "."))
            passo = float(valores["passo"].replace(",", "."))
            iteracoes = int(valores["iteracoes"])

            if valores["tipo"] not in ("mandelbrot", "julia"):
                raise ValueError("Selecione Mandelbrot ou Julia.")
            if not (0.002 <= passo <= 0.05):
                raise ValueError("O passo deve estar entre 0,002 e 0,05.")
            if not (20 <= iteracoes <= 500):
                raise ValueError("As iterações devem ficar entre 20 e 500.")

            png = gerar_fractal(
                tipo=valores["tipo"],
                real=real,
                imaginaria=imaginaria,
                passo=passo,
                max_iter=iteracoes,
            )
            imagem = base64.b64encode(png).decode("ascii")
        except (ValueError, OverflowError) as exc:
            erro = str(exc) or "Confira os valores informados."

    return render_template("index.html", imagem=imagem, erro=erro, valores=valores)

@app.route("/fractal.png", methods=["POST"])
def fractal_png():
    try:
        tipo = request.form.get("tipo", "mandelbrot")
        real = float(request.form.get("real", "-0.5").replace(",", "."))
        imaginaria = float(request.form.get("imaginaria", "0").replace(",", "."))
        passo = float(request.form.get("passo", "0.01").replace(",", "."))
        iteracoes = int(request.form.get("iteracoes", "150"))
        if tipo not in ("mandelbrot", "julia") or not (0.002 <= passo <= 0.05) or not (20 <= iteracoes <= 500):
            raise ValueError
        return send_file(BytesIO(gerar_fractal(tipo, real, imaginaria, passo, iteracoes)),
                         mimetype="image/png", download_name="fractal.png")
    except (ValueError, OverflowError):
        return "Parâmetros inválidos.", 400

if __name__ == "__main__":
    app.run(debug=True)
