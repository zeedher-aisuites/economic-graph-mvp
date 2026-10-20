"""Render the editable executive brief to a three-page A4 PDF."""

# Long paragraph strings mirror the HTML source and are intentionally kept intact.
# ruff: noqa: E501

from html.parser import HTMLParser
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Table, TableStyle

ROOT = Path(__file__).parent
SOURCE = ROOT / "conectapyme-executive-brief.html"
OUTPUT = ROOT / "conectapyme-executive-brief.pdf"


class TextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):
        self.text.append(data)


def validate_source():
    parser = TextParser()
    parser.feed(SOURCE.read_text(encoding="utf-8"))
    source_text = " ".join(parser.text)
    required = (
        "ConectaPyME",
        "Economic Graph",
        "30 empresas",
        "83",
        "$39,000",
        "valor incremental",
    )
    missing = [value for value in required if value not in source_text]
    if missing:
        raise SystemExit(f"HTML source is missing required brief content: {missing}")


def para(text, style):
    return Paragraph(text, style)


def build():
    validate_source()
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "title",
        parent=styles["Title"],
        fontSize=25,
        leading=29,
        textColor=colors.HexColor("#092c4c"),
        spaceAfter=10,
    )
    heading = ParagraphStyle(
        "heading",
        parent=styles["Heading2"],
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#0b6e8e"),
        spaceBefore=7,
        spaceAfter=6,
    )
    body = ParagraphStyle(
        "body", parent=styles["BodyText"], fontSize=10.5, leading=14, spaceAfter=7
    )
    small = ParagraphStyle("small", parent=body, fontSize=9, textColor=colors.HexColor("#516579"))
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=17 * mm,
        bottomMargin=15 * mm,
    )
    story = [
        para("ConectaPyME", title),
        para("Brief ejecutivo · inteligencia económica para priorizar oportunidades B2B", heading),
        para(
            "Una prueba de concepto que combina un Economic Graph, datos sintéticos y reglas explicables para ayudar a un equipo comercial a decidir qué empresas investigar primero.",
            body,
        ),
        para(
            "<b>Problema de negocio</b><br/>La información de empresas, sucursales y relaciones económicas está fragmentada. El equipo necesita priorizar sin ocultar incertidumbre.",
            body,
        ),
        para(
            "<b>Propuesta</b><br/>Un Economic Graph observable, una vista temporal y una Control Tower para revisar evidencia antes de actuar.",
            body,
        ),
        para("Qué se implementó", heading),
        Table(
            [
                [
                    para("<b>30</b><br/>empresas del universo sintético", body),
                    para("<b>23</b><br/>conocidas en T2", body),
                    para("<b>21</b><br/>elegibles en T2", body),
                    para("<b>83</b><br/>observaciones en T2", body),
                ],
                [
                    para("<b>5</b><br/>plazas ilustrativas", body),
                    para("T0/T1/T2<br/>historia temporal", body),
                    para("Baseline vs grafo<br/>ranking explicable", body),
                    para("5 vistas<br/>Control Tower offline", body),
                ],
            ],
            colWidths=[40 * mm] * 4,
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#eef6f8")),
                    ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#19a0ae")),
                    ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.white),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("PADDING", (0, 0), (-1, -1), 7),
                ]
            ),
        ),
        para(
            "La capacidad de cinco plazas es ilustrativa y no equivale al tamaño del universo. No hay clientes reales, ventas observadas, modelo entrenado ni experimento causal ejecutado.",
            small,
        ),
        PageBreak(),
        para("Evidencia técnica", title),
        para("De una señal a una decisión revisable", heading),
        para(
            "El sistema conserva observaciones, fechas, fuentes, conflictos e identidades candidatas. Las consultas usan cortes temporales y el ranking explica qué contribuyó a cada posición.",
            body,
        ),
        para(
            "<b>Arquitectura:</b> datos observables → vista temporal → reglas de ranking → Control Tower → evidencia y decisión.",
            body,
        ),
        para(
            "El Economic Graph no fusiona automáticamente identidades ambiguas. Las relaciones confirmadas aportan señales explicables; las referencias y conflictos permanecen visibles para revisión.",
            body,
        ),
        para(
            "El ranking muestra una forma de ordenar la investigación. No es una probabilidad de compra ni una predicción de ventas.",
            body,
        ),
        para("Evaluación económica", heading),
        para(
            "Supuestos: $10,000 MXN de implementación, $6,000 de operación, $50 por plaza investigada, activación de referencia de 10%, activación hipotética de 12% y $8,000 de margen por activación.",
            body,
        ),
        Table(
            [
                [
                    para(
                        "<b>5 plazas · base</b><br/><font color='#c04a35'>−$15,450</font><br/>antes de reserva",
                        body,
                    ),
                    para(
                        "<b>500 plazas · base</b><br/><font color='#0b7f70'>+$39,000</font><br/>antes de reserva",
                        body,
                    ),
                    para(
                        "<b>500 · nulo</b><br/><font color='#c04a35'>−$41,000</font><br/>antes de reserva",
                        body,
                    ),
                ]
            ],
            colWidths=[53 * mm] * 3,
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fff4e8")),
                    ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#e06b3c")),
                    ("PADDING", (0, 0), (-1, -1), 9),
                ]
            ),
        ),
        para(
            "El saldo base de 500 plazas después de una reserva de $3,200 sería +$35,800. Son escenarios educativos, no ROI observado.",
            small,
        ),
        PageBreak(),
        para("Siguiente experimento", title),
        para("Cómo mediríamos valor incremental", heading),
        para(
            "1. Definir una unidad elegible y un horizonte comercial.<br/>2. Separar bolsas comparables y pre-registrar la regla.<br/>3. Medir activación, margen, costo de atención y calidad de datos.<br/>4. Comparar contra un baseline sin atribuir causalidad donde no exista diseño experimental.",
            body,
        ),
        para("Condiciones para avanzar", heading),
        para(
            "Validar identidad, cobertura y calidad de señales con usuarios comerciales. Estabilizar el proceso de seguimiento. Diseñar una prueba acotada y autorizada antes de operar.",
            body,
        ),
        para("Conclusión", heading),
        para(
            "ConectaPyME muestra cómo unir ciencia de datos, relaciones económicas y razonamiento financiero en una experiencia revisable. Su valor está en hacer explícitas las señales, los supuestos y la siguiente medición necesaria.",
            body,
        ),
        para(
            "TelcoMx es un caso consultivo ficticio complementario y no comparte entidades ni métricas con este prototipo.",
            small,
        ),
    ]
    doc.build(story)


if __name__ == "__main__":
    build()
