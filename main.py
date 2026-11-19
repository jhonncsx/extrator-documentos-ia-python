import os
from pathlib import Path
from typing import List
import pandas as pd
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field
from pypdf import PdfReader

load_dotenv()


# 1. Contrato de Dados Estruturados (Schema da Nota Fiscal / Boleto)
class DadosDocumentoFiscal(BaseModel):
    tipo_documento: str = Field(description="Ex: Nota Fiscal de Serviço, Danfe, Boleto, Fatura.")
    numero_documento: str = Field(description="Número da nota ou código identificador.")
    empresa_emissora: str = Field(description="Razão social ou nome fantasia do emissor.")
    cnpj_emissor: str = Field(description="CNPJ formatado (00.000.000/0000-00) ou 'Não informado'.")
    data_emissao: str = Field(description="Data de emissão no formato DD/MM/AAAA.")
    data_vencimento: str = Field(description="Data de vencimento no formato DD/MM/AAAA ou 'À vista'.")
    valor_total: float = Field(description="Valor monetário total do documento (apenas número, ex: 1250.50).")
    descricao_resumida: str = Field(description="Resumo curto do serviço prestado ou produto adquirido.")


# 2. Leitura de Texto de Arquivos PDF
def extrair_texto_pdf(caminho_pdf: Path) -> str:
    leitor = PdfReader(str(caminho_pdf))
    texto_completo = []
    for pagina in leitor.pages:
        conteudo = pagina.extract_text()
        if conteudo:
            texto_completo.append(conteudo)
    return "\n".join(texto_completo)


# 3. Extração Inteligente via Gemini + Pydantic
def processar_documento_com_ia(texto_bruto: str) -> DadosDocumentoFiscal:
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    prompt = f"""
    Você é um especialista em automação fiscal e financeira.
    Extraia com precisão os dados estruturados do documento abaixo.
    Converta valores monetários para formato numérico decimal (ponto como separador).

    Texto do documento:
    \"\"\"{texto_bruto}\"\"\"
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": DadosDocumentoFiscal,
            "temperature": 0.0,  # Zero criatividade: máxima precisão na extração de dados
        },
    )

    return DadosDocumentoFiscal.model_validate_json(response.text)


# 4. Exportação para Planilha Excel e CSV
def salvar_relatorio(registros: List[DadosDocumentoFiscal], arquivo_saida: str = "relatorio_extraido.xlsx") -> None:
    df = pd.DataFrame([item.model_dump() for item in registros])
    df.to_excel(arquivo_saida, index=False)
    df.to_csv("relatorio_extraido.csv", index=False, encoding="utf-8-sig")
    print(f"\n✅ Planilhas geradas com sucesso: '{arquivo_saida}' e 'relatorio_extraido.csv'")
    print(df.to_string(index=False))


# 5. Execução Principal (Lê pasta 'documentos/' ou roda exemplos simulados)
if __name__ == "__main__":
    pasta_docs = Path("documentos")
    arquivos_pdf = list(pasta_docs.glob("*.pdf")) if pasta_docs.exists() else []
    resultados: List[DadosDocumentoFiscal] = []

    if arquivos_pdf:
        print(f"📂 Encontrados {len(arquivos_pdf)} PDF(s) na pasta 'documentos/'. Processando...")
        for pdf in arquivos_pdf:
            print(f" -> Lendo: {pdf.name}")
            texto = extrair_texto_pdf(pdf)
            dados = processar_documento_com_ia(texto)
            resultados.append(dados)
    else:
        print("ℹ️ Nenhum PDF encontrado na pasta 'documentos/'. Executando modo de demonstração...")
        textos_exemplo = [
            """
            PREFEITURA MUNICIPAL DE GUARULHOS - NOTA FISCAL DE SERVIÇOS ELETRÔNICA (NFS-e)
            Número da Nota: 202600489 | Data de Emissão: 12/11/2026
            Prestador: TECHSOLUTIONS AUTOMAÇÃO INDUSTRIAL LTDA | CNPJ: 42.198.765/0001-10
            Discriminação dos Serviços: Manutenção preventiva em painel CLP e calibração de sensores ópticos.
            Valor Total da Nota: R$ 2.450,00 | Vencimento: 25/11/2026
            """,
            """
            BOLETO DE COBRANÇA - BANCO ITAÚ
            Beneficiário: CLOUDHOST INFRAESTRUTURA DIGITAL S.A. - CNPJ: 19.876.543/0001-55
            Documento Nº: 99812-B | Emissão: 05/11/2026 | Vencimento: 20/11/2026
            Referência: Hospedagem de servidores cloud e banco de dados (Plano Business).
            Valor do Documento: R$ 489,90
            """,
        ]
        for idx, texto in enumerate(textos_exemplo, start=1):
            print(f" -> Processando documento simulado #{idx}...")
            resultados.append(processar_documento_com_ia(texto))

    if resultados:
        salvar_relatorio(resultados)
