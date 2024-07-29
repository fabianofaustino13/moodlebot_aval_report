import streamlit as st
import Pages.Upload as UpArquivo

def LoginAVA():
    st.title(':wave: Login')
    ativar_login = False
    ativar_senha = False
    ativar_arquivo = False
    form = st.form(key='Cliente', clear_on_submit=False)

    with form:
        dados = []
        print('############ BEM VINDO AO MOODLEBOT - RELATÓRIO DE AVALIAÇÃO DO CURSO ############')
        print('Abra o navegador de sua preferência e execute um dos endereços apresentados acima "Local URL ou Network URL"')
        print('Entre com suas credenciais da Secretaria e selecione o arquivo txt com os dados necessários.')
        print('########################################################################')
        input_name = st.text_input('Login: ', placeholder='Digite o seu login da Secretaria')
        input_password = st.text_input('Senha: ', placeholder='Digite a sua senha', type='password')
        
        up_arquivo = UpArquivo.UploadTxt()
        #st.write(up_arquivo[1])
        
        botao_submit = form.form_submit_button('Confirma!')

        if botao_submit:
            
            #st.write('Clicou!')
            #st.write(input_name)

            if not input_name:
                st.error("Informe o seu login da Secretaria!")
                #btnEnviar = st.form_submit_button("Enviar", disabled=True)
            else:
                ativar_login = True
                #btnEnviar = st.form_submit_button("Enviar", disabled=False)
                #st.text('Login ok')

            if not input_password:
                st.error("Informe a senha!")    
            else:
                ativar_senha = True      

            if not up_arquivo[1]:
                st.error("Selecione um arquivo")
            else:
                ativar_arquivo = True

            if ativar_senha and ativar_login and ativar_arquivo:                    
                print('ATENÇÃO: Escolha a pasta para salvar os arquivos que serão baixados!')
                return botao_submit, input_name, input_password, up_arquivo


