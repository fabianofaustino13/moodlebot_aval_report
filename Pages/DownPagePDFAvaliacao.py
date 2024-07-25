from datetime import datetime
import os, time
import aspose.pdf as ap
import pdfkit

async def DownloadPagePDFAvaliacao(page, nome_curso, linha, cont_curso, endereco_salvar, short_name_full): #linha, cont_curso):
#def DownloadPDFAvaliacao(page, nome_curso, linha, cont_curso, endereco_salvar): #linha, cont_curso):
    results = []   
    #print(page)
    #return results
    config = pdfkit.configuration(wkhtmltopdf=r'C:\moodlebot_avaliacao_report\wkhtmltopdf.exe')
    try:        
        time.sleep(1)
        async with page.expect_download() as download_info:          
            await page.get_by_alt_text("Baixar em formato PDF").click(timeout = 5000000)
        
        #download = await download_info.value
        download = await download_info.value
        print(f"URL para download: {download}")
        url_para_pesquisa = str(await download_info.value)
        url_pesquisa_instance = url_para_pesquisa.find('&instance=')
        url_pesquisa_group = url_para_pesquisa.find('&group=')
        id_instance = url_para_pesquisa[url_pesquisa_instance+10:url_pesquisa_group]
        await page.goto(f'https://mooc41.escolavirtual.gov.br/mod/questionnaire/report.php?action=vall&instance={id_instance}&group=0&target=print')
        url_print = f'https://mooc41.escolavirtual.gov.br/mod/questionnaire/report.php?action=vall&instance={id_instance}&group=0&target=print'
        print(page)
        pdfkit.from_url('https://mooc41.escolavirtual.gov.br/mod/questionnaire/report.php?action=vall&instance=5359&group=0&target=print', 'teste.pdf', configuration=config)
        #sugestao_nome = download_info.value.suggested_filename
        #nome_breve = await page.locator('xpath=//li[@class="breadcrumb-item"]').nth(2).inner_text()#locator('a:has-text("Ver todas as respostas")').get_attribute('href')
        #print(f'Nome breve: {nome_breve}')
        short_name_full = short_name_full.replace(':',' -')
        short_name_full = short_name_full.replace('?','')
        short_name_full = short_name_full.replace('/','')
        short_name_full = short_name_full.upper()
        data_hora_agora = datetime.now()
        data_hora = data_hora_agora.strftime(f'%Y%m%d%H%M%S')
        pesquisa_turma = short_name_full.find('TURMA')
        #print(pesquisa_turma)
        if pesquisa_turma != -1:
            turma = short_name_full[pesquisa_turma:]
            #print(turma)
            nome_arquivo = nome_curso + " - Avaliação de Satisfação - " + turma + "-" + data_hora + ".pdf"
        else:
            nome_arquivo = nome_curso + " - Avaliação de Satisfação - " + data_hora + ".pdf"
     
        print(f'Nome do arquivo: {nome_arquivo}')
        salvar_arquivo = os.path.join(endereco_salvar, nome_arquivo)
        #download_info.value.save_as(salvar_arquivo)
        #await download.save_as(salvar_arquivo)
        await download.save_as(salvar_arquivo)
    except Exception as err:        
        nome_arquivo = f'Erro ao baixar a Avaliação de Satisfação. Linha: {cont_curso} do arquivo.'
        results+=  [f"{nome_arquivo} - Link: {linha}"]
        #results+=  [f"Erro {err}, {type(err)=}."]
        print(f"Erro ao baixar o arquivo da linha = {cont_curso}: {linha}")
        print(f"Erro {err}, {type(err)=}.")
        await page.goto(linha)
    
    #print(f'Salvando em: {salvar_arquivo}')
    #print(f'Nome do arquivo: {nome_arquivo}')

    return results, nome_arquivo