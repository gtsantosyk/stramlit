import streamlit as st
from datetime import datetime
from utils.pdf_generator import gerar_pdf
from PIL import Image

st.set_page_config(page_title="Checklist Técnico", layout="wide")

st.title("Relatório Técnico de Inspeção de Equipamentos")

# 1. Informações Gerais
st.header("Informações Gerais")
ordem_servico = st.text_input("Ordem de Serviço")
data = st.date_input("Data", value=datetime.today())
cliente = st.text_input("Nome do Cliente")
tipo_inspecao = st.selectbox("Tipo de Inspeção", ["Inspeção", "Liberação", "Rotina"])

# 2. Dados do Equipamento
st.header("Dados do Equipamento Testado")
codigo_equip = st.text_input("Código do Equipamento")
nome_equip = st.text_input("Nome Descritivo")
num_serie = st.text_input("Número de Série")

# 3. Referências
st.header("Referências Utilizadas")
referencias = [st.text_input(f"Referência {i+1}") for i in range(4)]

# 4. Campos descritivos
st.header("Informações Técnicas")
problemas = st.text_area("Problemas Reportados")
avaliacao = st.text_area("Avaliação Técnica")
servicos = st.text_area("Serviços Necessários/Realizados")

# 5. Imagens
st.header("Imagens do Equipamento")
imagens = st.file_uploader("Envie as imagens do dispositivo", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

# 6. Checklists
def checklist_secao(titulo, itens):
    st.subheader(titulo)
    respostas = {}
    for item in itens:
        respostas[item] = st.radio(item, ["Aprovado", "Reprovado", "N/A"], horizontal=True)
    return respostas

inspecao_fisica = checklist_secao("Inspeção Física", ["Estrutura externa", "Cabos e conexões", "Etiquetas e marcações"])
testes_funcionais = checklist_secao("Testes Funcionais", ["Inicialização", "Alarmes", "Desempenho"])
pecas_acessorios = checklist_secao("Peças e Acessórios", ["Carregador", "Cabos", "Bateria"])

# 7. Observações e Resultado
st.header("Conclusão")
observacoes = st.text_area("Observações Finais")
resultado_final = st.radio("Resultado Final", ["Aprovado", "Reprovado"])

# 8. Assinatura
st.header("Assinatura do Técnico")
tecnico = st.text_input("Nome do Técnico")
assinatura = st.file_uploader("Assinatura (imagem)", type=["png", "jpg", "jpeg"])

# 9. Botão de geração do PDF
if st.button("Gerar Relatório PDF"):
    campos_obrigatorios = [ordem_servico, cliente, tecnico, resultado_final]
    if all(campos_obrigatorios):
        gerar_pdf({
            "ordem": ordem_servico,
            "data": data.strftime("%d/%m/%Y"),
            "cliente": cliente,
            "tipo": tipo_inspecao,
            "equip": [codigo_equip, nome_equip, num_serie],
            "referencias": referencias,
            "problemas": problemas,
            "avaliacao": avaliacao,
            "servicos": servicos,
            "inspecao": inspecao_fisica,
            "funcionais": testes_funcionais,
            "pecas": pecas_acessorios,
            "observacoes": observacoes,
            "resultado": resultado_final,
            "tecnico": tecnico,
            "assinatura": assinatura,
            "imagens": imagens
        })
    else:
        st.error("Preencha todos os campos obrigatórios antes de gerar o relatório.")
