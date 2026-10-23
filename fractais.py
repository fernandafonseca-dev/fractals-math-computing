from io import BytesIO
from PIL import Image

MAX_Z_AMPLITUDE = 2.0

PALETA = [
    (10, 8, 35), (35, 12, 90), (60, 30, 150), (40, 90, 200),
    (20, 160, 190), (70, 205, 140), (220, 225, 80), (245, 145, 55),
    (220, 55, 75), (250, 220, 230),
]

def calcular_ponto(z_re, z_im, c_re, c_im, max_iter):

    for iteracao in range(max_iter):

        novo_re = z_re * z_re - z_im * z_im + c_re
        novo_im = 2 * z_re * z_im + c_im
        z_re, z_im = novo_re, novo_im

        modulo_quadrado = z_re * z_re + z_im * z_im
        if modulo_quadrado > MAX_Z_AMPLITUDE * MAX_Z_AMPLITUDE:
            return iteracao + 1, modulo_quadrado ** 0.5

    return max_iter, (z_re * z_re + z_im * z_im) ** 0.5

def cor_por_iteracao(iteracao, max_iter, divergiu):

    if not divergiu:
        return (0, 0, 0)
    indice = min(len(PALETA) - 1, int((iteracao / max_iter) * len(PALETA)))
    return PALETA[indice]

def gerar_fractal(tipo="mandelbrot", real=-0.5, imaginaria=0.0,
                  passo=0.01, max_iter=150, largura=None, altura=None):
    if tipo not in ("mandelbrot", "julia"):
        raise ValueError("Tipo de fractal inválido.")
    if passo <= 0:
        raise ValueError("O passo deve ser maior que zero.")
    if max_iter < 1:
        raise ValueError("O número de iterações deve ser positivo.")

    min_x, max_x = -3.0, 2.0
    min_y, max_y = -2.0, 2.0
    largura = largura or max(240, min(900, int((max_x - min_x) / passo) + 1))
    altura = altura or max(200, min(700, int((max_y - min_y) / passo) + 1))

    imagem = Image.new("RGB", (largura, altura), (0, 0, 0))
    pixels = imagem.load()

    for py in range(altura):
        z_im_plano = max_y - py * (max_y - min_y) / max(1, altura - 1)
        for px in range(largura):
            z_re_plano = min_x + px * (max_x - min_x) / max(1, largura - 1)

            if tipo == "mandelbrot":

                c_re = z_re_plano + (real + 0.5)
                c_im = z_im_plano + imaginaria
                z_re, z_im = 0.0, 0.0
            else:

                c_re, c_im = real, imaginaria
                z_re, z_im = z_re_plano, z_im_plano

            iteracao, modulo = calcular_ponto(z_re, z_im, c_re, c_im, max_iter)
            divergiu = modulo > MAX_Z_AMPLITUDE or iteracao < max_iter
            pixels[px, py] = cor_por_iteracao(iteracao, max_iter, divergiu)

    saida = BytesIO()
    imagem.save(saida, format="PNG")
    return saida.getvalue()
