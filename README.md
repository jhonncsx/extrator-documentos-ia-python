# 📄 Extrator Inteligente de Documentos Fiscais e PDFs com IA

Pipeline de hiperautomação em **Python** que lê documentos não estruturados (Notas Fiscais, Boletos e Faturas em PDF), extrai campos financeiros críticos usando **Google Gemini + Pydantic (Structured Outputs)** e consolida tudo automaticamente em planilhas **Excel (`.xlsx`)** e **CSV**.

---

## 🎯 Problema Resolvido
Processos administrativos e financeiros perdem horas digitando manualmente dados de notas fiscais e boletos (CNPJ, datas de vencimento, valores e descrições) em planilhas ou sistemas ERP. Este projeto elimina o trabalho manual e reduz erros de digitação.

## ⚙️ Como Funciona o Pipeline
1. **Ingestão de Arquivos:** Varre automaticamente a pasta `documentos/` em busca de arquivos `.pdf` utilizando `pypdf` *(possui também modo demonstração integrado caso a pasta esteja vazia)*.
2. **Extração Cognitiva (`temperature=0.0`):** Envia o texto bruto para o modelo `gemini-2.5-flash` instruído a atuar com precisão contábil.
3. **Validação Estrita (Pydantic):** Garante que valores monetários, CNPJs e datas saiam tipados corretamente (`float`, `str`) sem quebrar a planilha.
4. **Exportação Tabular:** Gera automaticamente os arquivos `relatorio_extraido.xlsx` e `relatorio_extraido.csv` via `pandas` e `openpyxl`.

## 🛠️ Tecnologias Utilizadas
* **Python 3.10+**
* **Google GenAI SDK (`google-genai`)**
* **Pydantic** (Structured Outputs)
* **PyPDF** (Leitura e extração de texto de PDFs)
* **Pandas & OpenPyXL** (Geração de planilhas Excel e CSV)

## 🚀 Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/jhonncsx/extrator-documentos-ia-python.git
   cd extrator-documentos-ia-python
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure sua chave gratuita do Google AI Studio:
   ```bash
   cp .env.example .env
   # Adicione sua GEMINI_API_KEY dentro do arquivo .env
   ```

4. *(Opcional)* Crie uma pasta `documentos/` e coloque seus PDFs lá dentro, ou rode direto no modo demonstração:
   ```bash
   python main.py
   ```
