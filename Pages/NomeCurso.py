
async def NomeCurso(page):
    results = []    
    #return results
    pagina = page
    try:        
        #nome_curso = page.wait_for_selector('#page-header').query_selector('.page-header-headings').inner_text()
        nome_curso = await page.locator('#page-header').locator('.page-header-headings').inner_text()
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