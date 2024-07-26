import time
async def NomeCurso(page, linha, versao_ava):
#def NomeCurso(page):
    results = []    
    #return results
    pagina = page
    try:        
        pesquisa_id_curso = linha.find('?id=')
        id_link_curso = linha[pesquisa_id_curso+4:]
        if versao_ava == 38:
            await page.goto(f'https://mooc38.escolavirtual.gov.br/course/edit.php?id={id_link_curso}')
            await page.locator('xpath=//a[@class="collapseexpand" and @role="button"]').click(timeout=300000)
        else:
            await page.goto(f'https://mooc41.escolavirtual.gov.br/course/edit.php?id={id_link_curso}')
            await page.locator('xpath=//a[@class="btn btn-link p-1 collapseexpand collapsemenu collapsed" and @role="button"]').click(timeout=300000)
        
        time.sleep(0.5)
        nome_curso = await page.locator('#id_fullname').input_value()
        short_name_full = await page.locator('#id_shortname').input_value()
        print(f'Nome breve: {short_name_full}')
        formato_curso = await page.locator('#id_courseformathdr').locator('#id_format').input_value()
        print(f'Formato do Curso: {formato_curso}')
        
        #if (formato.input_value() != 'board') and (formato.input_value() != 'topics') and (formato.input_value() != 'topcoll') and (formato.input_value() != 'tiles') and (formato.input_value() != 'grid'): 
            #pagina_carregada = True                   
            #await page.locator('xpath=//input[@name="setmode"]').click()
            #await page.get_by_role("checkbox").set_checked(True)
        #    results+= ["Editar configurações do Curso 'Formato' deve ser: 'Formato Board, Tópicos, Tópicos Contraídos ou Tiles' atendendo ao Padrão."]

        #await page.goto(linha)
        #await page.goto(linha)#, wait_until="load")
        #time.sleep(1)
        #nome_curso = page.wait_for_selector('#page-header').query_selector('.page-header-headings').inner_text()
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

    return nome_curso, short_name_full, formato_curso