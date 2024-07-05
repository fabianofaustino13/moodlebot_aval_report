from datetime import datetime
import os, time


async def DownloadPDF(page, nome_curso, linha, cont_curso, endereco_salvar): #linha, cont_curso):
    results = []   
    print(page)
    #return results
    try:        
        #SE NÃO FOR PDF, IRÁ ESCOLHER A OPÇÃO PDF            
        download_extensao = await page.locator('#downloadtype_download').input_value()
        if download_extensao != 'pdf':
            await page.locator('#downloadtype_download').select_option(value='pdf')
            
        async with page.expect_download() as download_info:          
            await page.get_by_text("Download").click()
        
        download = await download_info.value
        print(f"URL para download: {download}")
        #sugestao_nome = download_info.value.suggested_filename
        sugestao_nome = download.suggested_filename
        #print(f'Sugestão de nome: {sugestao_nome}')
        maiusculo = sugestao_nome.upper()
        #print(maiusculo)
        string_turma = maiusculo.find('TURMA')        
        #print(string_turma)
        data_hora_agora = datetime.now()
        data_hora = data_hora_agora.strftime(f'%H%M%S')
        if string_turma == -1:
            #nome_em_lista = sugestao_nome[string_turma+6:]
            novo_nome = sugestao_nome[string_turma+6:string_turma+23]
            nome_arquivo = nome_curso + " - " + novo_nome + data_hora + ".pdf"
            print(f'Nome do arquivo: {nome_arquivo}')
        else:
            #nome_em_lista = sugestao_nome[string_turma+6:]
            novo_nome = sugestao_nome[string_turma+6:string_turma+23]
            nome_arquivo = nome_curso + " - " + novo_nome + data_hora + ".pdf"
            print(f'Nome do arquivo: {nome_arquivo}')
       
        salvar_arquivo = os.path.join(endereco_salvar, nome_arquivo)
        #download_info.value.save_as(salvar_arquivo)
        await download.save_as(salvar_arquivo)
    except Exception as err:
        print('##### Nova tentativa de download ####')
        # results+=  [f"Problema no Download do Arquivo em PDF. Na linha {cont_curso}: {linha}. Uma possível falha de conexão. Se possível, tente rodar novamente."]
        # results+=  [f"Erro {err}, {type(err)=}."]
        #time.sleep(1)
        #print(linha)
        print('Atualizar')
        time.sleep(1)
        await page.keyboard.press('F5',delay=1000)
        time.sleep(1)
        await page.reload()
        time.sleep(1)
        print('Atualizar')
        #await page.goto(linha)
        download_extensao = await page.locator('#downloadtype_download').input_value()
        if download_extensao != 'pdf':
            await page.locator('#downloadtype_download').select_option(value='pdf')
            
        #link = page.wait_for_selector('xpath=//button[@class="btn btn-secondary"]')#.click(timeout=300000)
        async with page.expect_download() as download_info:           
            await page.get_by_text("Download").click()
        
        download = await download_info.value
        print(f"URL para download: {download}")
        #sugestao_nome = download_info.value.suggested_filename
        sugestao_nome = download.suggested_filename
        print(f'Sugestão de nome: {sugestao_nome}')
        maiusculo = sugestao_nome.upper()
        #print(maiusculo)
        string_turma = maiusculo.find('TURMA')        
        #print(string_turma)
        data_hora_agora = datetime.now()
        data_hora = data_hora_agora.strftime(f'%H%M%S')
        if string_turma == -1:
            #nome_em_lista = sugestao_nome[string_turma+6:]
            novo_nome = sugestao_nome[string_turma+6:string_turma+23]
            nome_arquivo = nome_curso + " - " + novo_nome + data_hora + ".pdf"
            print(f'Nome do arquivo: {nome_arquivo}')
        else:
            #nome_em_lista = sugestao_nome[string_turma+6:]
            novo_nome = sugestao_nome[string_turma+6:string_turma+23]
            nome_arquivo = nome_curso + " - " + novo_nome + data_hora + ".pdf"
            print(f'Nome do arquivo: {nome_arquivo}')
       
        salvar_arquivo = os.path.join(endereco_salvar, nome_arquivo)
        #download_info.value.save_as(salvar_arquivo)
        
        await download.save_as(salvar_arquivo)

        print(f"Erro {err}, {type(err)=}.")
    
    print(f'Nome: {salvar_arquivo}')
    print(f'Nome do arquivo: {nome_arquivo}')

    return results, nome_arquivo