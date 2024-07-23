import streamlit as st
import asyncio, time
import Pages.Cliente as Login
import Pages.Pasta as PastaLocal
import Pages.Logar as Logando
import Pages.NomeCurso as Nome
import Pages.DownPDFAvaliacao as DownAvaliacao
import Pages.DownPDFQuestionario as DownQuestionario
import Pages.Questionario as Quest
import Pages.Avaliacao as Aval
from playwright.async_api import async_playwright
#from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
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
def NomeCurso(page):
    results = []    
    #return results
    pagina = page
    try:        
        nome_curso = page.wait_for_selector('#page-header').query_selector('.page-header-headings').inner_text()
        #nome_curso = await page.locator('#page-header').locator('.page-header-headings').inner_text()
        #nome_curso = page.locator('#page-header').locator('.page-header-headings').inner_text()
        #nome_curso = await n_curso.inner_text()
        print(f"Nome do curso original: {nome_curso}")
        nome_curso = nome_curso.replace(':',' -')
        nome_curso = nome_curso.replace('?','')
        nome_curso = nome_curso.replace('/','')
        print(f"Nome do curso alterado: {nome_curso}")
    except Exception as err:
        results+=  [f"Problema no Nome do Curso do Ambiente. Uma possível falha de conexão. Se possível, tente rodar novamente."]
        results+=  [f"Erro {err}, {type(err)=}."]
        print(f"Erro {err}, {type(err)=}.")

    return nome_curso

def PesquisaAvaliacao(page, linha, cont_curso):
#def PesquisaAvaliacao(page, linha, cont_curso):
    results = []    
    #return results
    try:        
        print('Entrou pesquisa Local')
        asyncio.sleep(0.5)
        # Pesquisa pela Avaliação
        board = False
        #board_chave = await page.query_selector_all('xpath=//li[@class="activity questionnaire modtype_questionnaire "]')
        board_chave = page.query_selector_all('xpath=//li[@class="activity questionnaire modtype_questionnaire "]')
        print(f'Board chave: {board_chave.count()}')
        if len(board_chave) != 0:
            #cont = await page.query_selector_all('xpath=//li[@class="activity questionnaire modtype_questionnaire "]')
            cont = page.query_selector_all('xpath=//li[@class="activity questionnaire modtype_questionnaire "]')
            board = True
            print(f'Total de cont: {len(cont)}')
        else:
            #cont = await page.query_selector_all('xpath=//li[@class="activity activity-wrapper questionnaire modtype_questionnaire hasinfo dropready draggable"]')
            cont = page.query_selector_all('xpath=//li[@class="activity activity-wrapper questionnaire modtype_questionnaire hasinfo dropready draggable"]')
            print(f'Total de cont: {len(cont)}')

        #VERIFICAR SE O FORMATO DO CURSO É DO TIPO TILES - SE SIM, ENTRAR ABAIXO E MARCAR COMO VERDADEIRO PQ NA HORA DE SAIR DA ATIVIDADE ELE DEVE VOLTAR PARA O HOME
        #formato_tiles = await page.query_selector_all('xpath=//ul[@class="tiles"]')
        formato_tiles = page.query_selector_all('xpath=//ul[@class="tiles"]')
        tiles = False
        print(f'Total de tiles: {len(formato_tiles)}')
        if len(formato_tiles) != 0:
            tiles = True

        #VERIFICAR SE O FORMATO DO CURSO É DO TIPO TOPICO - SE SIM, ENTRA ABAIXO E MARCA COMO VERDADEIRO
        topico = False
        #formato_topico = await page.query_selector_all('xpath=//ul[@class="topics"]')
        formato_topico = page.query_selector_all('xpath=//ul[@class="topics"]')
        print(f'Total de Tópicos: {len(formato_topico)}')
        if len(formato_topico) != 0:
            topico = True

        total = len(cont)
        enquetes = []
        for enq in cont:
            #enquetes.append(await enq.get_attribute('id'))
            enquetes.append(enq.get_attribute('id'))
            print(f'IDs Enquetes: {enquetes}')
        
        x = 1
        for id_atividade in enquetes:   
            #TÓPICO CONTRAÍDO - ABRIR TUDO
            exp_novamente = True
            print(f'Enquete {x}/{total}')
            x+=1
            #NOME DA ENQUETE
            #nome_enquete = await page.locator(f'#{id_atividade}').locator('.activityname').inner_text()
            nome_enquete = page.locator(f'#{id_atividade}').locator('.activityname').inner_text()
            print(nome_enquete)
            #CLICAR NA ENQUETE
            #await page.locator(f'#{id_atividade}').locator('.activityname').click()
            page.locator(f'#{id_atividade}').locator('.activityname').click()
            asyncio.sleep(1)
            #CLICAR EM TODAS AS RESPOSTAS
            #await page.get_by_text("Ver todas as respostas").click()
            #nome = await page.locator('xpath=//div[@role="main"]').locator('.allresponses').inner_text()
            nome = page.locator('xpath=//div[@role="main"]').locator('.allresponses').inner_text()
            print(nome)
            #url = await page.locator('xpath=//div[@role="main"]').locator('.allresponses').get_attribute('id')
            #print(url)
            #respostas = await page.query_selector_all('.allresponses')
            respostas = page.query_selector('.allresponses')
            print(respostas)
            #await page.locator('.allresponses').click()
            #await page.get_by_role("a", ".allresponses").click()
            #navegacao_secundaria = 
            #await page.locator('xpath=//div[@class="secondary-navigation d-print-none"]').locator('a:has-text("Mais")').click()
            #await asyncio.sleep(0.5)
            #navegacao_secundaria.locator('a:has-text("Mais")').click()
            #await asyncio.sleep(0.5)
            #await page.locator('xpath=//div[@class="secondary-navigation d-print-none"]').locator('a:has-text("Mais")').locator(f'a:has-text("{nome}")').click()
            #//*[@id="yui_3_17_2_1_1720563417142_45"]
            
            print('Todas as respostas')

            #await page.get_by_text("Download").click()
            #atividade = await page.wait_for_selector(f'#{id_atividade}').query_selector('xpath=//div[@class="activity-actions align-self-start"]')
            #atividade.wait_for_element_state('enabled')
            #atividade.hover()
            #atividade.click()
            #page.wait_for_selector(f'#{id_atividade}').query_selector('span:has-text("Editar configurações")').click()

    except Exception as err:
        results+=  [f"Problema na Pesquisa de Avaliação. Na linha {cont_curso}: {linha}. Uma possível falha de conexão. Se possível, tente rodar novamente."]
        results+=  [f"Erro {err}, {type(err)=}."]
        print(f"Erro {err}, {type(err)=}.")

    return results

async def HomePage():
#def HomePage():
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
            #await asyncio.sleep(2)
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
                #with async_playwright() as p:
                    browser = await p.chromium.launch(headless=False, channel="chrome")
                    #browser = p.chromium.launch(headless=False, channel="chrome")
                    page = await browser.new_page()
                    # AUMENTANDO A RESOLUÇÃO PARA 1920X1080 PARA ANTENDER AOS CURSOS NO FORMATO BOARD COM 25%
                    await page.set_viewport_size({"width": 1920, "height": 1080})

                    #page = browser.new_page()
                    endereco_evg = 'https://www.escolavirtual.gov.br/login'
                    await page.goto(endereco_evg)
                    #page.goto(endereco_evg)
                    login_sucesso = await Logando.Login(page, login, senha)
                    try:
                        if login_sucesso:
                            st.success('Login com sucesso!')
                            print('Login com sucesso!')
                            await asyncio.sleep(1)
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
                                await asyncio.sleep(1)
                                versao_ava_38 = linha.find('/mooc38.escolavirtual.gov.')
                                #print(f'Versão 38: {versao_ava_38}')
                                versao_ava_41 = linha.find('/mooc41.escolavirtual.gov.') 
                                #print(f'Versão 41: {versao_ava_41}')
                                pagina_carregada = False   
                                #print('Aqui')    
                                
                                try:
                                    if versao_ava_38 != -1:
                                        print("Ambiente Virtual de Aprendizagem 3.8")
                                        url_38 = "https://mooc38.escolavirtual.gov.br/my/"                                
                                        await page.goto(url_38)#, wait_until="load")
                                        #page.goto(url_38)#, wait_until="load")
                                        await page.goto(linha)#, wait_until="load")
                                        #PEGAR O NOME BREVE DO CURSO
                                        pesquisa_id_curso = linha.find('?id=')
                                        id_link_curso = linha[pesquisa_id_curso+4:]
                                        await page.goto(f'https://mooc38.escolavirtual.gov.br/course/edit.php?id={id_link_curso}')
                                        short_name_full = await page.locator('#id_shortname').input_value()
                                        #print(short_name_full)
                                        await page.goto(linha)
                                        pagina_carregada = True
                                        nome_curso = await Nome.NomeCurso(page)
                                        versao_ava = 38
                                        pesquisa_avaliacao_curso = await Aval.PesquisaAvaliacao(page, linha, cont_curso, versao_ava)  
                                        arquivo_down = await DownAvaliacao.DownloadPDFAvaliacao(page, nome_curso, linha, cont_curso, endereco_salvar, short_name_full)#, linha, cont_curso)                                      
                                        results+= arquivo_down[0]
                                        #### Questionários #####
                                        await page.goto(linha)
                                        print('Retornando a página inicial do curso')
                                        pesquisa_questionario_curso = await Quest.Questionario(page, nome_curso, linha, cont_curso, endereco_salvar, versao_ava, short_name_full)
                                        results+= pesquisa_questionario_curso         

                                    elif versao_ava_41 != -1:
                                        print("Ambiente Virtual de Aprendizagem 4.1")
                                        url_41 = "https://mooc41.escolavirtual.gov.br/my/"                                        
                                        await page.goto(url_41)#, wait_until="load")    
                                        #page.goto(url_41)#, wait_until="load")    
                                        await page.goto(linha)#, wait_until="load") 
                                        #PEGAR O NOME BREVE DO CURSO
                                        pesquisa_id_curso = linha.find('?id=')
                                        id_link_curso = linha[pesquisa_id_curso+4:]
                                        await page.goto(f'https://mooc41.escolavirtual.gov.br/course/edit.php?id={id_link_curso}')
                                        short_name_full = await page.locator('#id_shortname').input_value()
                                        print(short_name_full)
                                        await page.goto(linha)
                                        pagina_carregada = True                   
                                        nome_curso = await Nome.NomeCurso(page)
                                        versao_ava = 41
                                        try:
                                            pesquisa_avaliacao_curso = await Aval.PesquisaAvaliacao(page, linha, cont_curso, versao_ava)
                                        except:
                                            print('goto 4.1')
                                            await page.goto(linha)
                                        arquivo_down = await DownAvaliacao.DownloadPDFAvaliacao(page, nome_curso, linha, cont_curso, endereco_salvar, short_name_full)#, linha, cont_curso)                                      
                                        results+= arquivo_down[0]
                                        #### Questionários #####
                                        await page.goto(linha)
                                        print('Retornando a página inicial do curso')
                                        pesquisa_questionario_curso = await Quest.Questionario(page, nome_curso, linha, cont_curso, endereco_salvar, versao_ava, short_name_full)
                                        results+= pesquisa_questionario_curso                                                           
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
                                            #page.goto(nova_requisicao)#, wait_until="load")
                                        elif versao_ava_41 != -1:
                                            nova_requisicao = 'https://mooc41.escolavirtual.gov.br/my/'
                                            await page.goto(nova_requisicao)#, wait_until="load")
                                            #page.goto(nova_requisicao)#, wait_until="load")
                                        else:
                                            nova_requisicao = 'https://mooc41.escolavirtual.gov.br/my/'
                                            await page.goto(nova_requisicao)#, wait_until="load")
                                            #page.goto(nova_requisicao)#, wait_until="load")
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
                            #await browser.close()                        
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
    #asyncio.run(HomePage)
    #python -m streamlit run --client.showSidebarNavigation=False .\homepage.py
    #app_streamlit.terminate()
