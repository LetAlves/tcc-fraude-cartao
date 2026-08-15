"""
Gera o dicionário de dados do dataset IEEE-CIS Fraud Detection em .docx.
Cobre todas as colunas das duas tabelas: train_transaction e train_identity.
"""

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from pathlib import Path

SAIDA = Path(__file__).resolve().parent.parent / "reports" / "dicionario_dados.docx"

# ── Paleta de cores por grupo ──────────────────────────────────────────────────
CORES = {
    "alvo":        RGBColor(0x7C, 0x3A, 0xED),   # roxo
    "transacao":   RGBColor(0x05, 0x96, 0x69),   # verde
    "cartao":      RGBColor(0x0E, 0x7A, 0xFF),   # azul
    "endereco":    RGBColor(0xF5, 0x9E, 0x0B),   # âmbar
    "email":       RGBColor(0xEF, 0x44, 0x44),   # vermelho
    "C":           RGBColor(0x06, 0xB6, 0xD4),   # ciano
    "D":           RGBColor(0x84, 0xCC, 0x16),   # lima
    "M":           RGBColor(0xF9, 0x73, 0x16),   # laranja
    "V":           RGBColor(0x6B, 0x72, 0x80),   # cinza
    "identidade":  RGBColor(0xEC, 0x48, 0x99),   # rosa
    "dispositivo": RGBColor(0x14, 0xB8, 0xA6),   # teal
}

# ── Dados do dicionário ────────────────────────────────────────────────────────
GRUPOS = [

    {
        "titulo": "Variável Alvo",
        "arquivo": "train_transaction.csv",
        "cor": "alvo",
        "descricao": (
            "A única coluna que o modelo deve prever. "
            "Fortemente desbalanceada: ~96,5% são legítimas e ~3,5% são fraudes."
        ),
        "colunas": [
            ("isFraud", "int", "0 ou 1",
             "Rótulo binário fornecido pela competição: 0 = classe negativa | "
             "1 = classe de fraude. Não equivale a decisão jurídica sobre Pix e "
             "nunca deve ser usado como feature de entrada."),
        ],
    },

    {
        "titulo": "Identificadores e Tempo",
        "arquivo": "train_transaction.csv",
        "cor": "transacao",
        "descricao": (
            "Colunas de controle. TransactionDT não é um timestamp real — "
            "é um contador em segundos a partir de uma data de referência não divulgada pela Vesta."
        ),
        "colunas": [
            ("TransactionID",  "int",   "Ex: 2987000",
             "Chave primária. Usado para fazer o join com train_identity.csv."),
            ("TransactionDT",  "int",   "Ex: 86400 (= 1 dia)",
             "Segundos decorridos desde uma referência não divulgada. "
             "O módulo por 86400 indica posição relativa no ciclo diário; "
             "não deve ser chamado de hora local sem data-base e fuso."),
            ("TransactionAmt", "float", "Ex: 31.95, 117.00",
             "Valor de pagamento da transação no domínio original. "
             "Analisar a distribuição e os valores extremos sem presumir padrão causal."),
            ("ProductCD",      "str",   "W, H, C, S, R",
             "Código de produto. O significado dos códigos não foi divulgado; "
             "eventuais associações com o alvo precisam ser medidas no treino."),
        ],
    },

    {
        "titulo": "Informações do Cartão (card1–card6)",
        "arquivo": "train_transaction.csv",
        "cor": "cartao",
        "descricao": (
            "Informações do cartão no domínio original. card4 e card6 têm categorias "
            "legíveis; o significado individual de card1, card2, card3 e card5 não foi publicado."
        ),
        "colunas": [
            ("card1", "int",   "Ex: 4150, 9500",
             "Atributo codificado de cartão com alta cardinalidade. O significado exato não foi divulgado."),
            ("card2", "float", "Ex: 111, 360, 555",
             "Atributo adicional do cartão (codificado). Muitos valores nulos."),
            ("card3", "float", "Ex: 150, 185",
             "Atributo adicional do cartão (codificado)."),
            ("card4", "str",   "visa, mastercard, american express, discover",
             "Rede/bandeira do cartão no domínio original."),
            ("card5", "float", "Ex: 101, 145, 226",
             "Atributo adicional do cartão (codificado)."),
            ("card6", "str",   "debit, credit, debit or credit, charge card",
             "Tipo do cartão no domínio original."),
        ],
    },

    {
        "titulo": "Endereço (addr1, addr2)",
        "arquivo": "train_transaction.csv",
        "cor": "endereco",
        "descricao": (
            "Endereço associado à transação. "
            "Ambas as colunas são numéricas codificadas — não representam texto de endereço."
        ),
        "colunas": [
            ("addr1", "float", "Ex: 299, 325, 204",
             "Região de cobrança codificada numericamente."),
            ("addr2", "float", "Ex: 87, 96",
             "País de cobrança codificado numericamente."),
            ("dist1", "float", "Ex: 0, 9, 298",
             "Uma das medidas de distância fornecidas no domínio original; definição detalhada não publicada."),
            ("dist2", "float", "Ex: 0, 65",
             "Segunda medida de distância; definição detalhada não publicada e alta presença de nulos."),
        ],
    },

    {
        "titulo": "E-mail (P_emaildomain, R_emaildomain)",
        "arquivo": "train_transaction.csv",
        "cor": "email",
        "descricao": (
            "Domínios de e-mail do comprador (P = purchaser) e do destinatário (R = recipient). "
            "Qualquer associação com o alvo deve ser medida, não presumida."
        ),
        "colunas": [
            ("P_emaildomain", "str", "gmail.com, yahoo.com, hotmail.com…",
             "Domínio do e-mail de quem comprou no domínio original."),
            ("R_emaildomain", "str", "gmail.com, anonymous.com…",
             "Domínio do e-mail do destinatário no domínio original."),
        ],
    },

    {
        "titulo": "Grupo C — Variáveis de Contagem (C1–C14)",
        "arquivo": "train_transaction.csv",
        "cor": "C",
        "descricao": (
            "Grupo descrito oficialmente como contagens. O evento contado por cada coluna "
            "não foi divulgado. Interpretações da comunidade são hipóteses e não devem ser "
            "apresentadas como dicionário factual ou equivalência com sinais Pix."
        ),
        "colunas": [
            ("C1–C14", "float", "contagens", "14 atributos de contagem anonimizados; semântica individual não publicada."),
        ],
    },

    {
        "titulo": "Grupo D — Variáveis de Tempo (D1–D15)",
        "arquivo": "train_transaction.csv",
        "cor": "D",
        "descricao": (
            "Grupo descrito oficialmente como deltas temporais. Os eventos de origem e destino "
            "de cada delta não foram publicados. Importância e associação com o alvo dependem do experimento."
        ),
        "colunas": [
            ("D1–D15", "float", "deltas temporais", "15 atributos temporais anonimizados; semântica individual não publicada."),
        ],
    },

    {
        "titulo": "Grupo M — Variáveis de Match (M1–M9)",
        "arquivo": "train_transaction.csv",
        "cor": "M",
        "descricao": (
            "Indicadores de correspondência (match) do domínio original. A variável M4 possui "
            "categorias próprias; as demais aparecem como T/F/ausente. O significado individual não foi publicado."
        ),
        "colunas": [
            ("M1–M3", "str", "T, F, NaN", "Indicadores de match anonimizados."),
            ("M4", "str", "M0–M6, NaN", "Indicador categórico de match com significado não publicado."),
            ("M5–M9", "str", "T, F, NaN", "Indicadores de match anonimizados."),
        ],
    },

    {
        "titulo": "Grupo V — Features Vesta (V1–V339)",
        "arquivo": "train_transaction.csv",
        "cor": "V",
        "descricao": (
            "339 atributos numéricos engenheirados pela Vesta e anonimizados. A competição "
            "não publicou agrupamentos semânticos por faixa. Nulos e distribuição devem ser "
            "medidos coluna a coluna no EDA."
        ),
        "colunas": [
            ("V1–V339", "float", "valores numéricos e NaN", "Atributos Vesta anonimizados; semântica individual e por faixa não publicada."),
        ],
    },

    {
        "titulo": "Identidade (id_01–id_38)",
        "arquivo": "train_identity.csv",
        "cor": "identidade",
        "descricao": (
            "Atributos de identidade, rede e assinatura digital do domínio original. "
            "No treino, existem para 144.233 de 590.540 transações (24,4%). "
            "A competição não publicou o significado individual de id_01 a id_38."
        ),
        "colunas": [
            ("id_01–id_11", "numérico", "valores e NaN", "Atributos numéricos anonimizados; definição individual não publicada."),
            ("id_12–id_38", "categórico/numérico", "categorias, valores e NaN", "Atributos anonimizados; preservar nomes e não inferir significado individual."),
        ],
    },

    {
        "titulo": "Dispositivo (DeviceType, DeviceInfo)",
        "arquivo": "train_identity.csv",
        "cor": "dispositivo",
        "descricao": (
            "Informações diretas sobre o dispositivo usado na transação."
        ),
        "colunas": [
            ("DeviceType", "str", "desktop, mobile",
             "Tipo do dispositivo no domínio original. Associação com o alvo deve ser medida."),
            ("DeviceInfo", "str", "Ex: Windows, iOS Device, Samsung…",
             "Informação textual do dispositivo. Tem alta cardinalidade e valores ausentes; "
             "qualquer agrupamento precisa de regra documentada."),
        ],
    },
]


# ── Funções de formatação ──────────────────────────────────────────────────────

def set_cell_bg(cell, hex_color: str):
    """Define a cor de fundo de uma célula da tabela."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)


def rgb_to_hex(cor: RGBColor) -> str:
    return f"{cor[0]:02X}{cor[1]:02X}{cor[2]:02X}"


def cor_texto_para_fundo(cor: RGBColor) -> RGBColor:
    """Retorna branco ou preto conforme a luminosidade do fundo."""
    r, g, b = cor
    luminancia = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return RGBColor(0xFF, 0xFF, 0xFF) if luminancia < 0.5 else RGBColor(0x1E, 0x29, 0x3B)


def paragrafo(doc, texto, tamanho=11, negrito=False, italico=False,
              alinhamento=WD_ALIGN_PARAGRAPH.LEFT,
              cor=None, espaco_antes=0, espaco_depois=6):
    p = doc.add_paragraph(texto)
    p.alignment = alinhamento
    p.paragraph_format.space_before = Pt(espaco_antes)
    p.paragraph_format.space_after = Pt(espaco_depois)
    for run in p.runs:
        run.font.size = Pt(tamanho)
        run.font.bold = negrito
        run.font.italic = italico
        if cor:
            run.font.color.rgb = cor
    return p


def adicionar_grupo(doc, grupo):
    cor_obj = CORES[grupo["cor"]]
    cor_hex = rgb_to_hex(cor_obj)
    cor_txt = cor_texto_para_fundo(cor_obj)

    # Cabeçalho colorido do grupo
    p_titulo = doc.add_paragraph()
    p_titulo.paragraph_format.space_before = Pt(14)
    p_titulo.paragraph_format.space_after = Pt(4)
    run = p_titulo.add_run(f"  {grupo['titulo']}")
    run.font.bold = True
    run.font.size = Pt(12)
    run.font.color.rgb = cor_txt
    # Fundo colorido via XML
    pPr = p_titulo._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), cor_hex)
    pPr.append(shd)

    # Arquivo de origem
    p_arq = doc.add_paragraph()
    p_arq.paragraph_format.space_before = Pt(0)
    p_arq.paragraph_format.space_after = Pt(4)
    run2 = p_arq.add_run(f"  Arquivo: {grupo['arquivo']}")
    run2.font.size = Pt(9)
    run2.font.italic = True
    run2.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    # Descrição do grupo
    p_desc = doc.add_paragraph(grupo["descricao"])
    p_desc.paragraph_format.space_before = Pt(0)
    p_desc.paragraph_format.space_after = Pt(8)
    for run in p_desc.runs:
        run.font.size = Pt(10)
        run.font.italic = True

    # Tabela de colunas
    tabela = doc.add_table(rows=1, cols=4)
    tabela.style = 'Table Grid'

    # Cabeçalho da tabela
    cabecalhos = ["Coluna", "Tipo", "Valores exemplo", "Descrição"]
    for i, texto in enumerate(cabecalhos):
        cell = tabela.rows[0].cells[i]
        set_cell_bg(cell, cor_hex)
        p = cell.paragraphs[0]
        run = p.add_run(texto)
        run.font.bold = True
        run.font.size = Pt(9)
        run.font.color.rgb = cor_txt
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)

    # Larguras das colunas
    larguras = [Cm(3.2), Cm(1.6), Cm(3.0), Cm(8.8)]
    for i, larg in enumerate(larguras):
        for row in tabela.rows:
            row.cells[i].width = larg

    # Linhas de dados
    for idx, (col, tipo, valores, descricao) in enumerate(grupo["colunas"]):
        row = tabela.add_row()
        dados = [col, tipo, valores, descricao]
        bg = "F8F9FC" if idx % 2 == 0 else "FFFFFF"
        for i, texto in enumerate(dados):
            cell = row.cells[i]
            set_cell_bg(cell, bg)
            p = cell.paragraphs[0]
            run = p.add_run(texto)
            run.font.size = Pt(9)
            if i == 0:
                run.font.bold = True
                run.font.color.rgb = cor_obj
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)

    doc.add_paragraph()  # espaço após tabela


def gerar_docx():
    doc = Document()

    # Margens
    for section in doc.sections:
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2)

    doc.styles['Normal'].font.name = 'Calibri'
    doc.styles['Normal'].font.size = Pt(11)

    # ── Capa ──────────────────────────────────────────────────────────────────
    paragrafo(doc, "Dicionário de Dados", tamanho=20, negrito=True,
              alinhamento=WD_ALIGN_PARAGRAPH.CENTER,
              espaco_antes=0, espaco_depois=6)

    paragrafo(doc,
              "IEEE-CIS Fraud Detection Dataset",
              tamanho=13, italico=True,
              alinhamento=WD_ALIGN_PARAGRAPH.CENTER,
              cor=RGBColor(0x64, 0x74, 0x8B),
              espaco_antes=0, espaco_depois=4)

    paragrafo(doc,
              "TCC — Sistema Híbrido de Detecção de Fraudes com ML + RAG",
              tamanho=10,
              alinhamento=WD_ALIGN_PARAGRAPH.CENTER,
              cor=RGBColor(0x94, 0xA3, 0xB8),
              espaco_antes=0, espaco_depois=24)

    # ── Resumo do dataset ──────────────────────────────────────────────────────
    paragrafo(doc, "Visão Geral do Dataset", tamanho=13, negrito=True,
              espaco_antes=0, espaco_depois=6)

    resumo = (
        "O dataset IEEE-CIS Fraud Detection é composto por duas tabelas que devem ser unidas "
        "pela coluna TransactionID usando um left join (nem toda transação tem registro de identidade).\n\n"
        "• train_transaction.csv — 590.540 linhas × 394 colunas\n"
        "  Contém dados da transação em si: valor, cartão, endereço, e-mail e as features "
        "  dos grupos C, D, M e V.\n\n"
        "• train_identity.csv — 144.233 linhas × 41 colunas\n"
        "  Contém dados sobre o dispositivo e identidade digital do usuário. "
        "  Presente em 24,4% das transações de treino.\n\n"
        "• Taxa de fraude: 3,5% (20.663 fraudes de 590.540 transações)\n"
        "• Período coberto: 6 meses (inferido pelos valores de TransactionDT)\n"
        "• Fonte: Vesta Corporation — empresa de serviços de garantia de pagamento"
    )
    p = doc.add_paragraph(resumo)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(16)
    for run in p.runs:
        run.font.size = Pt(10)

    # ── Grupos de colunas ──────────────────────────────────────────────────────
    paragrafo(doc, "Descrição das Colunas por Grupo", tamanho=13, negrito=True,
              espaco_antes=0, espaco_depois=8)

    for grupo in GRUPOS:
        adicionar_grupo(doc, grupo)

    # ── Nota final ────────────────────────────────────────────────────────────
    doc.add_page_break()
    paragrafo(doc, "Notas Importantes para o TCC", tamanho=13, negrito=True,
              espaco_antes=0, espaco_depois=8)

    notas = [
        ("Colunas V1–V339 são anônimas",
         "A Vesta não divulgou o significado dessas features. Use análise de importância "
         "(SHAP) para identificar quais são relevantes. Não tente interpretar individualmente."),
        ("Muitos nulos não são necessariamente erro",
         "A ausência pode refletir o processo de coleta. Meça por coluna e valide se indicadores "
         "de ausência ajudam sem causar vazamento; não presuma a causa do nulo."),
        ("TransactionDT não é hora real",
         "O módulo por 86400 permite uma posição cíclica relativa, mas a data-base e o fuso "
         "não foram divulgados. Não chame o resultado de hora local."),
        ("train_identity.csv cobre 24,4% do treino",
         "Após o left join, as colunas id_ e Device* ficam ausentes nas demais transações. "
         "Imputação e indicadores devem ser ajustados apenas no treino."),
        ("card1–card5 têm alta cardinalidade",
         "Avalie codificação e memória. Se usar target encoding, calcule-o dentro das partições "
         "de treino para evitar vazamento do alvo."),
        ("Colunas anônimas não ganham significado com SHAP",
         "SHAP mede contribuição para a previsão. Não converta C*, D*, M*, V* ou id_* em "
         "conceitos Pix sem atributo derivado, definição e validação."),
    ]

    for titulo_nota, descricao_nota in notas:
        p_n = doc.add_paragraph()
        p_n.paragraph_format.space_before = Pt(0)
        p_n.paragraph_format.space_after = Pt(8)
        r1 = p_n.add_run(f"⚠ {titulo_nota}: ")
        r1.font.bold = True
        r1.font.size = Pt(10)
        r2 = p_n.add_run(descricao_nota)
        r2.font.size = Pt(10)

    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    doc.save(SAIDA)
    print(f"Dicionário gerado: {SAIDA}")


if __name__ == "__main__":
    gerar_docx()
