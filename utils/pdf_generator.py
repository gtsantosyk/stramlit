from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
import os
from datetime import datetime

def gerar_pdf(dados):
    nome_arquivo = f"data/exemplos/Relatorio_{dados['ordem']}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    os.makedirs("data/exemplos", exist_ok=True)

    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    c.drawString(50, 800, f"Relatório Técnico - Ordem: {dados['ordem']}")
    c.drawString(50, 780, f"Data: {dados['data']} - Cliente: {dados['cliente']}")
    c.drawString(50, 760, f"Técnico: {dados['tecnico']} - Tipo: {dados['tipo']}")
    c.drawString(50, 740, f"Equipamento: {dados['equip'][0]} - {dados['equip'][1]} (SN: {dados['equip'][2]})")

    c.drawString(50, 700, "Referências:")
    for i, ref in enumerate(dados['referencias']):
        c.drawString(60, 680 - i*15, f"- {ref}")

    c.drawString(50, 600, "Resultado Final: " + dados['resultado'])
    c.drawString(50, 580, "Problemas Reportados:")
    c.drawString(60, 565, dados['problemas'][:100])

    if dados["assinatura"] is not None:
        assinatura_image = ImageReader(dados["assinatura"])
        c.drawImage(assinatura_image, 50, 480, width=150, height=50)

    if dados["imagens"]:
        y = 400
        for img in dados["imagens"]:
            try:
                image_reader = ImageReader(img)
                c.drawImage(image_reader, 50, y, width=100, height=75)
                y -= 85
                if y < 100: break
            except:
                pass

    c.save()
