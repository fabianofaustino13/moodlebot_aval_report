import streamlit as st
import easygui

def LocalSalvar():     
    escolha_local = False
    endereco_salvar = None    
    #st.warning('ATENÇÃO: Escolha a pasta para salvar os arquivos que serão baixados!')
    #print('ATENÇÃO: Escolha a pasta para salvar os arquivos que serão baixados!')
    #print(f'Pasta escolhida: {endereco_salvar}')
    while endereco_salvar == None:
        endereco_salvar = easygui.diropenbox(title='Selecione uma pasta para salvar os arquivos')
        st.error('ATENÇÃO: Escolha a pasta para salvar os arquivos que serão baixados!')    
    escolha_local = True
    st.success('Pasta selecionada com sucesso!')
    return endereco_salvar, escolha_local
        