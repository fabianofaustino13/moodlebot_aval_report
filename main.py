#!.env/Script/ python
import streamlit as st
import asyncio, time
import time
import Pages.Cliente as Login
import Pages.Pasta as PastaLocal
import Pages.Logar as Logando
import Pages.NomeCurso as Nome
import Pages.NadaSerMostrado as Nada
import Pages.DownPDF as Down
import Pages.CriarPDF as NewPDF
import Pages.Avaliacao as Aval
from playwright.async_api import async_playwright
import pandas as pd

st.set_page_config(
    page_title='Moodlebot - Relatório de Avaliações do Curso - HomePage',
    page_icon=':earth_americas:',
    layout='wide'
)
st.title("Moodlebot - Relatório de Avaliações do Curso")
#st.subheader("Moodlebot - Relatórios")
# def apply_style(linha):
#     if (linha['message'] == 'Ok'):
#         return ['background-color: yellow'] == len(linha)
#     else:
#         return None

async def HomePage():
    with st.empty():
        #st.title("Moodlebot - Relatórios")
        #st.subheader("Login")
        chama_login = Login.LoginAVA()
        if chama_login:
            st.warning('ATENÇÃO: Escolha a pasta para salvar os arquivos que serão baixados!')
            login = chama_login[1]
            #print(f'Login: {login}')
            senha = chama_login[2]
            linhas = chama_login[3][0]
            #print(f'Arquivo: {linhas}')
            #time.sleep(2)
            escolha_local = False
            if escolha_local == False:
                endereco = PastaLocal.LocalSalvar()
                endereco_salvar = endereco[0]
                st.success('Aguarde até a conclusão dos arquivos')
                print('Aguarde até a conclusão dos arquivos')
                st.warning('ATENÇÃO: Escolha a pasta para salvar os arquivos que serão baixados!')
                #endereco_salvar = easygui.diropenbox(title='Selecione uma pasta para salvar os arquivos')
                print(f'Pasta escolhida: {endereco_salvar}')
                resultados = []
                results = []
                numero_da_linha = []
                linha_nao_baixada = 0
                async with async_playwright() as p:
                    browser = await p.chromium.launch(headless=False, channel="chrome")
                    page = await browser.new_page()
                    endereco_evg = 'https://www.escolavirtual.gov.br/login'
                    await page.goto(endereco_evg)
                    login_sucesso = await Logando.Login(page, login, senha)
                    try:
                        if login_sucesso:
                            st.success('Login com sucesso!')
                            print('Login com sucesso!')
                            time.sleep(1)
                            progress_text = "Baixando os arquivos. Por favor, aguarde."
                            print(f'Total de linhas: {len(linhas)}')
                            cont_linhas = len(linhas)
                            valor_progresso = 1 / int(cont_linhas)
                            #print(valor_progresso)
                            my_bar = st.progress(0, text=progress_text)
                            cont_curso = 0
                            st.warning('Aguarde até a conclusão dos arquivos')
                            for nova_linha in linhas:
                                cont_curso+=1
                                #print(cont_curso)
                                soma_bar = (valor_progresso * 100) * cont_curso
                                #print(soma_bar)
                                my_bar.progress(int(soma_bar), text=progress_text)
                                linha = str(nova_linha)
                                linha = linha[1:].replace("'", "")
                                #linha = linha.replace("b", "").replace("'", "")
                                print(f'Linha {cont_curso}/{cont_linhas}: {linha}')
                                time.sleep(1)
                                versao_ava_38 = linha.find('/mooc38.escolavirtual.gov.')
                                #print(f'Versão 38: {versao_ava_38}')
                                versao_ava_41 = linha.find('/mooc41.escolavirtual.gov.') 
                                #print(f'Versão 41: {versao_ava_41}')
                                pagina_carregada = False   
                                #print('Aqui')    
                                try:
                                    if versao_ava_38 != -1:
                                        print("Ava 38")
                                        url_38 = "https://mooc38.escolavirtual.gov.br/my/"                                
                                        await page.goto(url_38)#, wait_until="load")
                                        await page.goto(linha)#, wait_until="load")
                                        pagina_carregada = True
                                        nome_curso = await Nome.NomeCurso(page)
                                        #identificacao_participante, participante = IdentificacaoParticipante(page)
                                        nada_encontrado = await Nada.NadaSerMostrado(page)
                                        #print(nada_encontrado)
                                        if nada_encontrado == -1:
                                            #results+= await Down.DownloadPDF(page, nome_curso, linha, cont_curso, endereco_salvar) 
                                            arquivo_down = await Down.DownloadPDF(page, nome_curso, linha, cont_curso, endereco_salvar)#, linha, cont_curso)                                      
                                            results+= arquivo_down[0]   
                                        else:
                                            results+= await NewPDF.CriarArquivoPDF(page, nome_curso, linha, cont_curso, endereco_salvar)  

                                    elif versao_ava_41 != -1:
                                        url_41 = "https://mooc41.escolavirtual.gov.br/my/"
                                        
                                        await page.goto(url_41)#, wait_until="load")    
                                        await page.goto(linha)#, wait_until="load") 
                                        pagina_carregada = True                   
                                        nome_curso = await Nome.NomeCurso(page)
                                        print('Chamando pesquisa')
                                        pesquisa_avaliacao_curso = await Aval.PesquisaAvaliacao(page, linha, cont_curso)
                                        print('Passou pesquisa')
                                        print(pesquisa_avaliacao_curso)
                                        #identificacao_participante, participante = IdentificacaoParticipante(page)
                                        #print(nada_encontrado)
                                        nada_encontrado = await Nada.NadaSerMostrado(page)
                                        #print(nada_encontrado)
                                        if nada_encontrado == -1:
                                            arquivo_down = await Down.DownloadPDF(page, nome_curso, linha, cont_curso, endereco_salvar)#, linha, cont_curso)                                      
                                            results+= arquivo_down[0]   
                                        else:
                                            results+= await NewPDF.CriarArquivoPDF(page, nome_curso, linha, cont_curso, endereco_salvar)                   
                                    else:
                                        results+= [f"AVA não configurado."]
                                        numero_da_linha+= f'{cont_curso}'
                                        linha_nao_baixada+=1
                                        #print(f"Na linha {cont_curso} do arquivo. Plugin não configurado para o Ambiente AVA: {linha}")
                                    
                                except Exception as ex:
                                    resultados.append({
                                        "check": str(results),
                                        "message": ex,
                                        "status": False
                                    })
                                finally:
                                    if pagina_carregada == False:
                                        #print('###### Nova requisição ######')
                                        if versao_ava_38 != -1:
                                            nova_requisicao = 'https://mooc38.escolavirtual.gov.br/my/'
                                            await page.goto(nova_requisicao)#, wait_until="load")
                                        elif versao_ava_41 != -1:
                                            nova_requisicao = 'https://mooc41.escolavirtual.gov.br/my/'
                                            await page.goto(nova_requisicao)#, wait_until="load")
                                        else:
                                            nova_requisicao = 'https://mooc41.escolavirtual.gov.br/my/'
                                            await page.goto(nova_requisicao)#, wait_until="load")
                                    #print('###### Resultados #######')
                                    if len(results) > 0:
                                        #print(results)
                                        resultados.append({
                                            #"check": str(f'Na linha {numero_da_linha[cont_curso]} do arquivo'),
                                            "check": str(f'Link: {linha}'),
                                            "message": results,
                                            "status": False
                                        })
                                        results=[]
                                    else:
                                        resultados.append({
                                            #"check": str(f'O arquivo contém {total_linhas} link(s) e {total_linhas-linha_nao_baixada} foram baixada(s).'),
                                            #"check": str(f'Nome do Curso: {nome_curso}'),
                                            "check": str(f'{arquivo_down[1]}'),
                                            "message": "Ok",
                                            "status": True
                                        })
                            await browser.close()                        
                        
                        else:
                            st.error('Login ou senha inválido!')
                            print('Erro da senha')
                            results+= 'Login ou senha inválido!'
                            resultados.append({
                                "check": 'Login ou senha inválido!',
                                "message": 'Erro ao logar na plataforma',
                                "status": False
                            })
                    except Exception as ex:
                        print('Erro da senha')
                        resultados.append({
                            "check": str(results),
                            "message": ex,
                            "status": False
                        })
                #PageList.List(resultados)
                df = pd.DataFrame(
                    resultados
                    #columns=['Item', 'Verificação', 'Resultado']
                )
                #EXCLUÍNDO A ÚLTIMA COLUNA PARA NÃO SER VISÍVEL
                #def color_vowel(value):
                #    return f"background-color: pink;" if value in [*"false"] else None
                
                #st.table(df.style.applymap(color_vowel))
                def apply_style(linha):
                    if (linha['Resultado'] != "Ok"):                        
                        return ['background-color: gold'] * (len(linha))
                    else:
                        return ['background-color: white'] * (len(linha))
                #INICIAR INDEX COM 1 E NÃO COM ZERO
                df.index+= 1
                dados_sem_coluna = df.drop(['status'], axis='columns')
                dados_sem_coluna.rename(columns={'check': 'Nome do arquivo', 'message': 'Resultado'}, inplace=True)
                #OCULTAR INDEX
                data2 = dados_sem_coluna.astype(str)
                data = data2.style.apply(axis=1, func=apply_style)
                #RENOMEANDO AS COLUNAS
                #MOSTRANDO O RESULTADO
                #dados.index += 1
                st.table(data)
                print('##### Concluído! #####')
                print('Se desejar executar um novo arquivo, atualize o seu navegador.')
                print('Para sair, feche o navegador e este console.')

if __name__ == '__main__':
    #app_streamlit = Popen('python -m streamlit run --client.showSidebarNavigation=False .\homepage.py'.split(' '), stdin=PIPE, stderr=PIPE) 
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
    title=loop.run_until_complete(HomePage())
    #python -m streamlit run --client.showSidebarNavigation=False .\homepage.py
    #app_streamlit.terminate()
