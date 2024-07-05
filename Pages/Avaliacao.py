import time

async def PesquisaAvaliacao(page, linha, cont_curso):
    results = []    
    #return results
    try:        
        print('Entrou pesquisa')
        time.sleep(0.5)
        # Pesquisa pela Avaliação
        lista_avaliacao = []
        avaliacao = await page.locator('xpath=//li[@class="activity questionnaire modtype_questionnaire "]').count()
        print(avaliacao)
        x=0
        for x in range(avaliacao):
            print('teste')
            await page[x].locator('xpath=//li[@class="activity questionnaire modtype_questionnaire "]').click()
            print('teste2')


        
    except Exception as err:
        results+=  [f"Problema na Pesquisa de Avaliação. Na linha {cont_curso}: {linha}. Uma possível falha de conexão. Se possível, tente rodar novamente."]
        results+=  [f"Erro {err}, {type(err)=}."]
        print(f"Erro {err}, {type(err)=}.")

    return results