from datetime import datetime
import Pages.DownPDFQuestionario as DownQuestionario
import os, time

#async def DownloadPDF(page, nome_curso, linha, cont_curso, endereco_salvar): #linha, cont_curso):
async def DownloadPDFQuestionario(page, nome_curso, linha, cont_curso, endereco_salvar, short_name_full): #linha, cont_curso):
    results = []   
    #print(page)
    #return results
    time.sleep(1)
    try:        
        #SE NÃO FOR PDF, IRÁ ESCOLHER A OPÇÃO PDF    
        #print('Baixando o Questionário') 
        #download_extensao = await page.locator('xpath=//div[@class="form-inline text-xs-right"]').locator('#downloadtype_download').nth(0).input_value()     
        #await page.locator('xpath=//div[@class="form-inline text-xs-right"]').nth(0).locator('#downloadtype_download').select_option(value='pdf')
        #print(download_extensao)
        #if download_extensao != 'pdf':
            #await page.locator('#downloadtype_download').select_option(value='pdf')
        #    await page.locator('xpath=//div[@class="form-inline text-xs-right"]').nth(0).locator('#downloadtype_download').select_option(value='pdf')
            #await page.locator('xpath=//div[@class="form-inline text-xs-right"]').locator('#downloadtype_download').nth(1).select_option(value="pdf")
            #page.locator('.custom-select urlselect').select_option(value='/mod/quiz/report.php?id=84410&mode=statistics')
            
        #async with page.expect_download() as download_info:          
        async with page.expect_download() as download_info:
            #await page.get_by_text("Download").click()
            #await page.get_by_text("Download").click()
            await page.locator('xpath=//div[@class="form-inline text-xs-right"]').nth(0).get_by_text("Download").click(timeout=500000)
        download = await download_info.value
        print(f"URL para download: {download}")
        #sugestao_nome = download_info.value.suggested_filename
        #nome_breve = await page.locator('xpath=//li[@class="breadcrumb-item"]').nth(2).inner_text()#locator('a:has-text("Ver todas as respostas")').get_attribute('href')
        #print(f'Nome breve: {nome_breve}')
        sugestao_nome = download.suggested_filename
        #print(f'Sugestão de nome: {sugestao_nome}')
        #print(maiusculo)
        nome_breve = sugestao_nome.replace(':',' -')
        nome_breve = sugestao_nome.replace('?','')
        nome_breve = sugestao_nome.replace('/','')
        nb_maiusculo = nome_breve.upper()
        short_name_full = short_name_full.replace(':',' -')
        short_name_full = short_name_full.replace('?','')
        short_name_full = short_name_full.replace('/','')
        short_name_full = short_name_full.replace('|','')
        short_name_full = short_name_full.replace(' ','')
        short_name_full = short_name_full.strip()
        short_name_full = short_name_full.upper()
        data_hora_agora = datetime.now()
        data_hora = data_hora_agora.strftime(f'%Y%m%d%H%M%S')
        pesquisa_turma = nb_maiusculo.find('TURMA')
        pesquisa_ponto_pdf = nb_maiusculo.find('.PDF')
        #print(pesquisa_turma)
        if pesquisa_turma != -1:
            turma = nome_breve[pesquisa_turma:pesquisa_ponto_pdf]
            #print(turma)
            #nome_arquivo = nome_curso + " - " + turma + "-" + data_hora + ".pdf"
            nome_arquivo = short_name_full + "-" + data_hora + ".pdf"
        else:
            turma = nome_breve[:pesquisa_ponto_pdf]
            #nome_arquivo = nome_curso + " - " + turma + " - " + data_hora + ".pdf"
            nome_arquivo = short_name_full + "-" + data_hora + ".pdf"

        print(f'Nome do arquivo: {nome_arquivo}')
        salvar_arquivo = os.path.join(endereco_salvar, nome_arquivo)
        #download_info.value.save_as(salvar_arquivo)
        #await download.save_as(salvar_arquivo)
        await download.save_as(salvar_arquivo)
    except Exception as err:
        nome_arquivo = f'Erro ao baixar o Questionário: {turma}. Linha: {cont_curso} do arquivo'
        results+=  [f"Link: {linha}"]
        #results+=  [f"Erro {err}, {type(err)=}."]
        print(f"Erro ao baixar o arquivo da linha = {cont_curso}: {linha}")
        print(f"Erro {err}, {type(err)=}.")      

    return results, nome_arquivo