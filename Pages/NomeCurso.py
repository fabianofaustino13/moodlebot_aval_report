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
            await page.goto(f'https://mooc38.escolavirtual.gov.br/course/edit.php?id={id_link_curso}')#, timeout=300000) # AGUARDAR ATÉ 5 MINUTOS PARA CARREGAR A PÁGINA 
            await page.locator('xpath=//a[@class="collapseexpand" and @role="button"]').click(timeout=300000)
        else:
            await page.goto(f'https://mooc41.escolavirtual.gov.br/course/edit.php?id={id_link_curso}')#, timeout=300000) # AGUARDAR ATÉ 5 MINUTOS PARA CARREGAR A PÁGINA 
            await page.locator('xpath=//a[@class="btn btn-link p-1 collapseexpand collapsemenu collapsed" and @role="button"]').click(timeout=300000)
        
        time.sleep(0.5)
        nome_curso = await page.locator('#id_fullname').input_value()
        short_name_full = await page.locator('#id_shortname').input_value()
        print(f'Nome breve: {short_name_full}')
        num_identificacao = await page.locator('#id_idnumber').input_value()
        print(f'Número de identificacao do curso: {num_identificacao}')
        formato_curso = await page.locator('#id_courseformathdr').locator('#id_format').input_value()
        print(f'Formato do Curso: {formato_curso}')           
        #LIMPANDO O NOME DO CURSO
        print(f"Nome do curso - original: {nome_curso}")
        nome_curso = nome_curso.replace(':',' -')
        nome_curso = nome_curso.replace('?','')
        nome_curso = nome_curso.replace('/','')
        print(f"Nome do curso - alterado: {nome_curso}")
        #LIMPANDO O NOME BREVE - TURMA
        nome_breve_turma = short_name_full
        print(f"Nome breve do curso - original: {nome_breve_turma}")
        nome_breve_turma = nome_breve_turma.replace(':','-')
        nome_breve_turma = nome_breve_turma.replace('?','')
        #nome_breve_turma = nome_breve_turma.replace('/','')
        nome_breve_turma = nome_breve_turma.replace('|','')
        nome_breve_turma = nome_breve_turma.strip()
        nome_breve_turma = nome_breve_turma.upper()
        #data_hora = data_hora_agora.strftime(f'%d%H%M%S')
        pesquisa_turma = nome_breve_turma.find('TURMA')
        if pesquisa_turma != -1:
            nome_breve_turma = nome_breve_turma[pesquisa_turma:]
            #nome_arquivo = nome_curso + " - Avaliação de Satisfação - " + turma + "-" + data_hora + ".pdf"
            nome_breve_turma = nome_breve_turma.upper()
        else:
            #nome_arquivo = nome_curso + " - Avaliação de Satisfação - " + data_hora + ".pdf"
            nome_breve_turma = nome_curso + " - " + short_name_full
        print(f"Nome breve do curso - alterado: {nome_breve_turma}")

    except Exception as err:
        results+=  [f"Problema no Nome do Curso do Ambiente. Uma possível falha de conexão. Se possível, tente rodar novamente."]
        results+=  [f"Erro {err}, {type(err)=}."]
        print(f"Erro {err}, {type(err)=}.")

    #RETORNA: NOME DO CURSO, NOME BREVE, NÚMERO DE IDENTIFICAÇÃO, FORMATO DO CURSO
    return nome_curso, short_name_full, num_identificacao, formato_curso, nome_breve_turma