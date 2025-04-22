import streamlit as st
import pandas as pd
import re
import os

st.title("Validador e Estruturador de Dados")

st.markdown("Insira os dados do cliente de forma livre abaixo (ex: 'João, 32 anos, casado, email joao@email.com, 2 compras, renda 50 mil')")
input_text = st.text_area("Texto com os dados do cliente")

st.markdown("Escolha para qual base deseja salvar os dados:")
opcao_base = st.selectbox("Base de destino:", ["CadastroCliente", "Clientes", "Vendas"])

if st.button("Processar e Inserir no Banco de Dados"):
    # Expressões regulares para extrair informações básicas
    nome = re.search(r"([A-ZÀ-Ú][a-zà-ü]+(?: [A-ZÀ-Ú][a-zà-ü]+)*)", input_text)
    idade = re.search(r"(\d{2})\s*anos", input_text)
    estado_civil = re.search(r"(casado|solteiro|divorciado|viúvo)", input_text, re.IGNORECASE)
    email = re.search(r"[\w\.-]+@[\w\.-]+", input_text)
    compras = re.search(r"(\d+)\s*compra", input_text)
    renda = re.search(r"renda\s*(\d+\s?mil|\d{5,})", input_text)

    # Feedback visual dos dados extraídos
    st.subheader("🔎 Dados Extraídos")
    st.write(f"**Nome:** {nome.group(1) if nome else 'Não encontrado'}")
    st.write(f"**Idade:** {idade.group(1) if idade else 'Não encontrado'}")
    st.write(f"**Estado Civil:** {estado_civil.group(1).capitalize() if estado_civil else 'Não encontrado'}")
    st.write(f"**E-mail:** {email.group(0) if email else 'Não encontrado'}")
    st.write(f"**Compras Realizadas:** {compras.group(1) if compras else 'Não encontrado'}")
    st.write(f"**Renda:** {renda.group(1) if renda else 'Não encontrado'}")

    if opcao_base == "CadastroCliente":
        dados = {
            "IDCliente": "cli_" + str(abs(hash(input_text)))[:10],
            "NomeCliente": nome.group(1) if nome else "Não informado",
            "Idade": int(idade.group(1)) if idade else None,
            "DataCadastro": pd.Timestamp.today().strftime('%Y-%m-%d'),
            "Email": email.group(0) if email else "Não informado",
            "Telefone": "Não informado",
            "EstadoCivil": estado_civil.group(1).capitalize() if estado_civil else "Não informado",
            "ComprasRealizadas": int(compras.group(1)) if compras else 0,
            "RendaAnual": int(re.sub("\D", "", renda.group(1))) * 1000 if renda and 'mil' in renda.group(1) else (int(renda.group(1)) if renda else 0),
            "CategoriaProdutoComprado": "Não informado"
        }

    elif opcao_base == "Clientes":
        dados = {
            "ClienteID": abs(hash(input_text)) % 100000,
            "Origem": "Não informado",
            "Idade": int(idade.group(1)) if idade else None,
            "SalarioAnual": int(re.sub("\D", "", renda.group(1))) * 1000 if renda and 'mil' in renda.group(1) else (int(renda.group(1)) if renda else 0),
            "Nota": 0,
            "Profissao": "Não informado",
            "ExperienciaTrabalho": 0,
            "TamanhoFamilia": 0
        }

    elif opcao_base == "Vendas":
        dados = {
            "Data": pd.Timestamp.today().strftime('%Y-%m-%d'),
            "Produto": "Não informado",
            "Quantidade": int(compras.group(1)) if compras else 0,
            "Preco": 0.0,
            "ValorTotal": 0.0
        }

    df = pd.DataFrame([dados])

    file_path = opcao_base + ".xlsx"

    if os.path.exists(file_path):
        existing_df = pd.read_excel(file_path)
        combined_df = pd.concat([existing_df, df], ignore_index=True)
    else:
        combined_df = df

    combined_df.to_excel(file_path, index=False)
    st.success(f"✅ Dados processados e salvos na base {opcao_base}.xlsx com sucesso!")
    st.dataframe(df)
