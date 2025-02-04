import Pages.DownPDFQuestionario as DownQuestionario
import time, asyncio

async def Questionario(page, nome_curso, linha, cont_curso, endereco_salvar, versao_ava, short_name_full):
#def PesquisaAvaliacao(page, linha, cont_curso):
    results = []    
    #return results
    try:        
        #asyncio.sleep(0.5)
        time.sleep(1)
        # Pesquisa pela Avaliação
        board = False
        board_chave = await page.query_selector_all('xpath=//li[@class="activity quiz modtype_quiz "]')
        #board_chave = page.query_selector_all('xpath=//li[@class="activity questionnaire modtype_questionnaire "]')
        if len(board_chave) != 0:
            cont = await page.query_selector_all('xpath=//li[@class="activity quiz modtype_quiz "]')
            #cont = page.query_selector_all('xpath=//li[@class="activity questionnaire modtype_questionnaire "]')
            board = True
            #print(f'Total de cont: {len(cont)}')
        else:
            cont = await page.query_selector_all('xpath=//li[@class="activity activity-wrapper quiz modtype_quiz hasinfo dropready draggable"]')
            #cont = page.query_selector_all('xpath=//li[@class="activity activity-wrapper questionnaire modtype_questionnaire hasinfo dropready draggable"]')
            #print(f'Total de cont: {len(cont)}')
            if len(cont) == 0:
                cont = await page.query_selector_all('xpath=//li[@class="activity activity-wrapper quiz modtype_quiz  hasinfo"]')
                #print('Curso no formato: Tópicos Contraídos')
            

        #VERIFICAR SE O FORMATO DO CURSO É DO TIPO TILES - SE SIM, ENTRAR ABAIXO E MARCAR COMO VERDADEIRO PQ NA HORA DE SAIR DA ATIVIDADE ELE DEVE VOLTAR PARA O HOME
        formato_tiles = await page.query_selector_all('xpath=//ul[@class="tiles"]')
        #formato_tiles = page.query_selector_all('xpath=//ul[@class="tiles"]')
        tiles = False
        #print(f'Total de tiles: {len(formato_tiles)}')
        if len(formato_tiles) != 0:
            tiles = True
        
        f_tiles = await page.query_selector_all('xpath=//li[@class="activity activity-wrapper quiz modtype_quiz dropready draggable"]')
        #print(f'Tiles: {len(f_tiles)}')
        if len(f_tiles) != 0:
            cont = await page.query_selector_all('xpath=//li[@class="activity activity-wrapper quiz modtype_quiz dropready draggable"]')

        #VERIFICAR SE O FORMATO DO CURSO É DO TIPO TOPICO - SE SIM, ENTRA ABAIXO E MARCA COMO VERDADEIRO
        topico = False
        formato_topico = await page.query_selector_all('xpath=//ul[@class="topics"]')
        #formato_topico = page.query_selector_all('xpath=//ul[@class="topics"]')
        #print(f'Total de Tópicos: {len(formato_topico)}')
        if len(formato_topico) != 0:
            topico = True

        total = len(cont)
        print(f'Total de Questionários: {total}')
        questionarios = []
        for question in cont:
            questionarios.append(await question.get_attribute('id'))
            #enquetes.append(enq.get_attribute('id'))
        
        x = 1
        for id_atividade in questionarios:   
            #TÓPICO CONTRAÍDO - ABRIR TUDO
            exp_novamente = True
            print(f'Questionário {x}/{total}')
            x+=1
            if versao_ava == 38: #VERSÃO 3.8
                #NOME DO QUESTIONÁRIO
                nome_questionario = await page.locator(f'#{id_atividade}').locator('.instancename').inner_text()
                print(f'Nome do Questionário: {nome_questionario}')
                #CLICAR NO QUESTIONÁRIO
                await page.locator(f'#{id_atividade}').locator('.instancename').click(timeout=500000)
                questionario_descricao = await page.locator('#intro').inner_text()
                quest_desc_maiusculo = questionario_descricao.upper()
                #print(quest_desc_maiusculo)

                termo_fixacao = quest_desc_maiusculo.find('FIXAÇÃO')
                termo_revisao = quest_desc_maiusculo.find('REVISÃO')
                termo_fixar = quest_desc_maiusculo.find('FIXAR')
                termo_nao_avaliativo = quest_desc_maiusculo.find('NÃO AVALIATIVO')
                if termo_fixacao == -1 and termo_revisao == -1 and termo_fixar == -1 and termo_nao_avaliativo == -1: #and pontos != -1: #Não existe o termo procurado
                    fixacao = False
                    pesquisa_id_questionario = id_atividade.find('module-')
                    #print(id_atividade[pesquisa_id_questionario+7:])
                    id_quest = id_atividade[pesquisa_id_questionario+7:]
                    try:
                        await page.goto(f'https://mooc38.escolavirtual.gov.br/mod/quiz/report.php?id={id_quest}&mode=statistics', timeout=600000) # AGUARDAR ATÉ 10 MINUTOS PARA CARREGAR A PÁGINA
                        await page.locator('xpath=//div[@class="form-inline text-xs-right"]').nth(0).locator('#downloadtype_download').select_option(value='pdf')
                    except:
                        print('############################################################################')
                        print(f'Tentando baixar, novamente, o Questionário: {nome_questionario}')
                        print('############################################################################')
                        time.sleep(10)
                        await asyncio.sleep(3)
                        await page.goto(f'https://mooc38.escolavirtual.gov.br/mod/quiz/report.php?id={id_quest}&mode=statistics', timeout=600000) # AGUARDAR ATÉ 10 MINUTOS PARA CARREGAR A PÁGINA
                        await asyncio.sleep(3)
                        await page.locator('xpath=//div[@class="form-inline text-xs-right"]').nth(0).locator('#downloadtype_download').select_option(value='pdf')
                    arquivo_down = await DownQuestionario.DownloadPDFQuestionario(page, nome_curso, linha, cont_curso, endereco_salvar, short_name_full)#, linha, cont_curso)                                      
                    #download_extensao = await page.locator('xpath=//div[@class="form-inline text-xs-right"]').locator('#downloadtype_download').nth(0).input_value()
                    results+= arquivo_down[0]
                else:
                    print(f'Questionário não avaliativo')
            else: #VERSÃO 4.1
                #NOME DA ENQUETE
                #nome_questionario = await page.locator(f'#{id_atividade}').locator('.activityname').inner_text()
                #nome_enquete = page.locator(f'#{id_atividade}').locator('.activityname').inner_text()
                #print(f'Nome do Questionário: {nome_questionario}')
                #CLICAR NA ENQUETE
                await page.locator(f'#{id_atividade}').locator('.activityname').click()
                #page.locator(f'#{id_atividade}').locator('.activityname').click()
                #asyncio.sleep(1)
                #time.sleep(2)
                #CLICAR EM TODAS AS RESPOSTAS
                nome_questionario = await page.locator('.page-header-headings').locator('.h2').inner_text()
                print(f'Nome do Questionário: {nome_questionario}')
                questionario_descricao = await page.locator('#intro').inner_text()
                quest_desc_maiusculo = questionario_descricao.upper()
                #print(quest_desc_maiusculo)     
                fixacao = True #Iniciando como verdadeiro, ou seja, existe o termo fixação na descrição da atividade
                tentativa_descricao = True
                metodo_avaliacao = True
                #nome_questionario = True

                #print(questionario_descricao)
                termo_fixacao = quest_desc_maiusculo.find('FIXAÇÃO')
                termo_revisao = quest_desc_maiusculo.find('REVISÃO')
                termo_fixar = quest_desc_maiusculo.find('FIXAR')
                termo_nao_avaliativo = quest_desc_maiusculo.find('NÃO AVALIATIVO')
                if termo_fixacao == -1 and termo_revisao == -1 and termo_fixar == -1 and termo_nao_avaliativo == -1: #and pontos != -1: #Não existe o termo procurado
                    fixacao = False
                    url = await page.locator('xpath=//input[@name="pageurl"]').input_value()
                    print(f'URL do Questionário: {url}')
                    pesquisa_id_url = url.find('view.php?id=')
                    #print(pesquisa_id_url)
                    print(f'Baixando o Questionário de ID: {url[pesquisa_id_url+12:]}')
                    id_questionario = url[pesquisa_id_url+12:]
                    try:
                        await page.goto(f'https://mooc41.escolavirtual.gov.br/mod/quiz/report.php?id={id_questionario}&mode=statistics', timeout=600000) # AGUARDAR ATÉ 10 MINUTOS PARA CARREGAR A PÁGINA
                        await page.locator('xpath=//div[@class="form-inline text-xs-right"]').nth(0).locator('#downloadtype_download').select_option(value='pdf')
                    except:
                        print('############################################################################')
                        print(f'Tentando baixar, novamente, o Questionário: {nome_questionario}')
                        print('############################################################################')
                        time.sleep(10)
                        await asyncio.sleep(3)
                        await page.goto(f'https://mooc41.escolavirtual.gov.br/mod/quiz/report.php?id={id_questionario}&mode=statistics', timeout=600000) # AGUARDAR ATÉ 10 MINUTOS PARA CARREGAR A PÁGINA
                        await asyncio.sleep(3)
                        await page.locator('xpath=//div[@class="form-inline text-xs-right"]').nth(0).locator('#downloadtype_download').select_option(value='pdf')

                    #await page.locator('xpath=//li[@data-key="quiz_report"]').locator('.nav-link  ').click()
                    arquivo_down = await DownQuestionario.DownloadPDFQuestionario(page, nome_curso, linha, cont_curso, endereco_salvar, short_name_full)#, linha, cont_curso)                                      
                    #download_extensao = await page.locator('xpath=//div[@class="form-inline text-xs-right"]').locator('#downloadtype_download').nth(0).input_value()
                    results+= arquivo_down[0]                   
                    time.sleep(1)
                else:
                    print(f'Questionário não avaliativo')

            await page.goto(linha)
            print('Retornando a página inicial do curso')
            
    except Exception as err:
        results+=  [f"Problema no Questionário: {nome_questionario} da linha {cont_curso}: {linha} do arquivo."]
        results+=  [f"Erro {err}, {type(err)=}."]
        print(f"Erro {err}, {type(err)=}.")

    return results