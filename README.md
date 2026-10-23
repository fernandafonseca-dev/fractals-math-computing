# PRJ.3 — Fractais de Julia e Mandelbrot

## Requisitos
- Python 3.10 ou superior
- Flask
- Pillow

## Executar no Windows
1. Extraia a pasta do projeto.
2. Abra o terminal nessa pasta.
3. (Opcional) Crie um ambiente virtual: `python -m venv .venv`
4. Ative: `.venv\Scripts\activate`
5. Instale as dependências: `pip install -r requirements.txt`
6. Inicie: `python app.py`
7. Abra o endereço indicado no terminal, normalmente http://127.0.0.1:5000

## Parâmetros
- Tipo: Mandelbrot ou Julia.
- Parte real e imaginária: em Julia, definem o parâmetro complexo fixo c. Em Mandelbrot, deslocam a região visualizada.
- Passo: controla a resolução amostrada do plano; passos menores geram mais pontos e levam mais tempo.
- Iterações: máximo de repetições para avaliar se um ponto diverge.

## Algoritmo
A recorrência é z(n+1) = z(n)^2 + c. O ponto é considerado divergente quando |z| > 2. Para Mandelbrot, z inicial é 0 e cada ponto fornece c. Para Julia, c é fixo e cada ponto fornece z inicial. A imagem utiliza uma paleta de dez cores por iteração, deixando pretos os pontos que não divergiram até o limite.

## Observação para a entrega
O projeto é uma adaptação em Python da ideia matemática do exemplo fornecido pelo professor. Teste a aplicação no computador em que será apresentada e confirme com o docente se ele exige limites específicos para a região do plano ou um formato particular de entrega.
