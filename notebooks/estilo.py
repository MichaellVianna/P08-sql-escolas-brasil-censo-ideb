"""Tema visual dos gráficos do P08.

Só aparência: cores, fontes, eixo de tempo, título com subtítulo e o salvamento das figuras.
A análise fica no notebook. Paleta categórica validada para daltonismo (azul, laranja, verde-água).
"""
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager
import matplotlib.ticker as mticker

SUPERFICIE = "#fcfcfb"
TINTA = "#0b0b0b"          # texto principal e linha do alvo
TINTA_2 = "#52514e"        # subtítulos, rótulos de eixo
TINTA_3 = "#898781"        # números dos eixos
GRADE = "#e1e0d9"
EIXO = "#c3c2b7"

AZUL = "#2a78d6"
LARANJA = "#eb6834"
VERDE_AGUA = "#1baf7a"
CRITICO = "#d03b3b"        # só para o que é alarme (pontos fora dos limites, zeros)
AZUL_FAIXA = "#cde2fb"     # trecho de referência e faixa de ±3σ
CINZA_FORA = "#c3c2b7"     # o que ficou de fora da análise

SERIES = [AZUL, LARANJA, VERDE_AGUA]

PASTA_IMAGENS = Path("../images")


def _fonte():
    # primeira fonte sans disponível na máquina, para não gerar aviso de fonte ausente
    instaladas = {f.name for f in font_manager.fontManager.ttflist}
    for nome in ("Segoe UI", "Helvetica Neue", "Arial", "DejaVu Sans"):
        if nome in instaladas:
            return nome
    return "sans-serif"


def aplica_tema():
    mpl.rcParams.update({
        "figure.facecolor": SUPERFICIE,
        "axes.facecolor": SUPERFICIE,
        "savefig.facecolor": SUPERFICIE,
        "figure.dpi": 110,
        "font.family": _fonte(),
        "font.size": 10,
        "text.color": TINTA,
        "axes.edgecolor": EIXO,
        "axes.linewidth": 1,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.labelcolor": TINTA_2,
        "axes.labelsize": 10,
        "axes.labelpad": 8,
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": GRADE,
        "grid.linewidth": 1,
        "xtick.color": TINTA_3,
        "ytick.color": TINTA_3,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "xtick.major.size": 0,
        "ytick.major.size": 0,
        "xtick.major.pad": 6,
        "ytick.major.pad": 6,
        "lines.solid_capstyle": "round",
        "lines.solid_joinstyle": "round",
        "legend.frameon": False,
        "legend.fontsize": 9.5,
        "legend.labelcolor": TINTA_2,
        "legend.handlelength": 1.6,
    })


def titulo(fig, texto, subtitulo=None, topo=1.15):
    """Título à esquerda, dizendo o achado, com um subtítulo mais discreto.

    `topo` é a altura, em polegadas, reservada no alto da figura para o cabeçalho.
    """
    altura = fig.get_figheight()
    fig.subplots_adjust(top=1 - topo / altura)
    fig.text(0.005, 1 - 0.10 / altura, texto, fontsize=14, fontweight="bold",
             color=TINTA, ha="left", va="top")
    if subtitulo:
        fig.text(0.005, 1 - 0.42 / altura, subtitulo, fontsize=10, color=TINTA_2,
                 ha="left", va="top")


def legenda_figura(fig, handles, y=0.78, ncol=4):
    """Legenda do cabeçalho de figuras com vários painéis, logo abaixo do subtítulo."""
    altura = fig.get_figheight()
    return fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.0, 1 - y / altura),
                      ncol=ncol, frameon=False, columnspacing=1.6, handletextpad=0.6,
                      borderaxespad=0)


def legenda(ax, **kwargs):
    """Legenda sem moldura, em uma linha, acima do gráfico."""
    padrao = dict(loc="lower left", bbox_to_anchor=(0, 1.0), ncol=6, borderaxespad=0.2,
                  columnspacing=1.6, handletextpad=0.6)
    padrao.update(kwargs)
    return ax.legend(**padrao)


def anota(ax, texto, xy, xytext, ha="left", va="center", **kwargs):
    """Anotação com seta fina, em tinta secundária."""
    ax.annotate(texto, xy=xy, xytext=xytext, ha=ha, va=va, fontsize=9, color=TINTA_2,
                arrowprops=dict(arrowstyle="-", color=TINTA_3, lw=0.8, shrinkA=2, shrinkB=2),
                **kwargs)


def num(x, casas=2):
    """Número no formato brasileiro (vírgula decimal, ponto de milhar, sinal de menos)."""
    texto = f"{x:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return texto.replace("-", "−")


def formato_br(ax, eixo="y", casas=2):
    """Números dos eixos no formato brasileiro, para combinar com os textos do gráfico."""
    formato = mticker.FuncFormatter(lambda v, _: num(v, casas))
    (ax.yaxis if eixo == "y" else ax.xaxis).set_major_formatter(formato)


def salva(fig, nome):
    """Salva a figura em ../images para usar no README."""
    PASTA_IMAGENS.mkdir(exist_ok=True)
    fig.savefig(PASTA_IMAGENS / f"{nome}.png", dpi=200, bbox_inches="tight", pad_inches=0.25)
