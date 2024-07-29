import time, asyncio

async def PesquisaAvaliacao(page, linha, cont_curso, versao_ava):
#def PesquisaAvaliacao(page, linha, cont_curso):
    results = []    
    #return results
    try:        
        #print('Entrou pesquisa')
        #asyncio.sleep(0.5)
        time.sleep(0.5)
        # Pesquisa pela Avaliação
        board = False
        board_chave = await page.query_selector_all('xpath=//li[@class="activity questionnaire modtype_questionnaire "]')
        #board_chave = page.query_selector_all('xpath=//li[@class="activity questionnaire modtype_questionnaire "]')
        if len(board_chave) != 0:
            cont = await page.query_selector_all('xpath=//li[@class="activity questionnaire modtype_questionnaire "]')
            #cont = page.query_selector_all('xpath=//li[@class="activity questionnaire modtype_questionnaire "]')
            board = True
            #print(f'Total de cont: {len(cont)}')
        else:
            cont = await page.query_selector_all('xpath=//li[@class="activity activity-wrapper questionnaire modtype_questionnaire hasinfo dropready draggable"]')
            #cont = page.query_selector_all('xpath=//li[@class="activity activity-wrapper questionnaire modtype_questionnaire hasinfo dropready draggable"]')
            if len(cont) == 0:
                cont = await page.query_selector_all('xpath=//li[@class="activity activity-wrapper questionnaire modtype_questionnaire  hasinfo"]')
                #print('Curso no formato: Tópicos Contraídos')
            #print(f'Total de cont: {len(cont)}')

        #VERIFICAR SE O FORMATO DO CURSO É DO TIPO TILES - SE SIM, ENTRAR ABAIXO E MARCAR COMO VERDADEIRO PQ NA HORA DE SAIR DA ATIVIDADE ELE DEVE VOLTAR PARA O HOME
        formato_tiles = await page.query_selector_all('xpath=//ul[@class="tiles"]')
        #formato_tiles = page.query_selector_all('xpath=//ul[@class="tiles"]')
        tiles = False
        #print(f'Total de tiles: {len(formato_tiles)}')
        if len(formato_tiles) != 0:
            tiles = True

        f_tiles = await page.query_selector_all('xpath=//li[@class="activity activity-wrapper questionnaire modtype_questionnaire dropready draggable"]')
        #print(f'Tiles: {len(f_tiles)}')
        if len(f_tiles) != 0:
            cont = await page.query_selector_all('xpath=//li[@class="activity activity-wrapper questionnaire modtype_questionnaire dropready draggable"]')
        #VERIFICAR SE O FORMATO DO CURSO É DO TIPO TOPICO - SE SIM, ENTRA ABAIXO E MARCA COMO VERDADEIRO
        topico = False
        formato_topico = await page.query_selector_all('xpath=//ul[@class="topics"]')
        #formato_topico = page.query_selector_all('xpath=//ul[@class="topics"]')
        #print(f'Total de Tópicos: {len(formato_topico)}')
        if len(formato_topico) != 0:
            topico = True

        total = len(cont)
        enquetes = []
        for enq in cont:
            enquetes.append(await enq.get_attribute('id'))
            #enquetes.append(enq.get_attribute('id'))        
        
        x = 1
        for id_atividade in enquetes:   
            #TÓPICO CONTRAÍDO - ABRIR TUDO
            exp_novamente = True
            print(f'Enquete {x}/{total}')
            x+=1
            #NOME DA ENQUETE
            if versao_ava == 38:
                #nome_enquete = await page.locator(f'#{id_atividade}').locator('.activityname').inner_text()
                #CLICAR NA ENQUETE
                await page.locator(f'#{id_atividade}').locator('.instancename').click(timeout = 500000)
                #CLICAR EM TODAS AS RESPOSTAS
                #await page.locator('xpath=//div[@class="allresponses"]').locator('a:has-text("Visualizar Todas as Respostas")').click(timeout = 500000)
                url_avaliacao = await page.locator('xpath=//div[@class="allresponses"]/a').get_attribute('href')
            else:
                #nome_enquete = await page.locator(f'#{id_atividade}').locator('.activityname').inner_text()
                #CLICAR NA ENQUETE
                await page.locator(f'#{id_atividade}').locator('.activityname').click(timeout = 500000)
                #CLICAR EM TODAS AS RESPOSTAS
                nome = await page.locator('xpath=//div[@role="main"]').locator('.allresponses').inner_text()
                #print(nome)
            
                #await page.locator('xpath=//div[@class="allresponses"]').locator('a:has-text("Ver todas as respostas")').click(timeout = 500000)
                url_avaliacao = await page.locator('xpath=//div[@class="allresponses"]/a').get_attribute('href')
    except Exception as err:
        results+=  [f"Problema na Avaliação de Satisfação. Na linha {cont_curso}: {linha}. Uma possível falha de conexão. Se possível, tente rodar novamente."]
        results+=  [f"Erro {err}, {type(err)=}."]
        print(f"Erro {err}, {type(err)=}.")

    print(url_avaliacao)
    return results, url_avaliacao