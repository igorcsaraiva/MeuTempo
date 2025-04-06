import streamlit as st
import pandas as pd
from datetime import datetime

def formatar_tempo_completo(td):
    total_ms = td.total_seconds() * 1000
    sign = "-" if total_ms < 0 else ""
    total_ms = abs(total_ms)

    horas = int(total_ms // (3600 * 1000))
    minutos = int((total_ms % (3600 * 1000)) // (60 * 1000))
    segundos = int((total_ms % (60 * 1000)) // 1000)
    milissegundos = int(total_ms % 1000)

    return f"{sign}{horas:02}:{minutos:02}:{segundos:02}.{milissegundos:03}"


def main():
    df = pd.read_excel("1213-bf-runing-geral.xlsx", engine='openpyxl', sheet_name='Table 3')
    nomes = df.sort_values(['Nome'])['Nome']
    
    df = df.sort_values('Tempo').reset_index(drop=True)
    df['Posição'] = df.index + 1

    st.title("Meu tempo")
  
    nome = st.selectbox("Selecione um nome",nomes, index= None, placeholder="Selecione um nome")

    if nome:
        tempo_participante = df[df['Nome'] == f'{nome}']
        posicao = int(tempo_participante.iloc[0]['Posição']) - 1
        tempos = []
        for value in df['Tempo']:
            tempos.append(datetime.combine(datetime.now(), value) - datetime.combine(datetime.now(), tempo_participante['Tempo'][posicao]))

        df['tempos_passados'] = tempos

        df['Diferença'] = df['tempos_passados'].apply(formatar_tempo_completo)

        df = df.drop(['tempos_passados'],axis=1)

    st.write(df.set_index('Posição'))




if __name__ == '__main__':
    main()