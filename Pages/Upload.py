import streamlit as st

def UploadTxt():
    upload_txt = False
    linhas = None
    uploaded_file = st.file_uploader("Selecione o arquivo txt")
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        #st.write(bytes_data)
        linhas = bytes_data.split()
        total_linhas = len(linhas)
        upload_txt = True

    return linhas, upload_txt