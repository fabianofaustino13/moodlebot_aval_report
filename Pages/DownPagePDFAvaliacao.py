from datetime import datetime
import os, time
import aspose.pdf as ap

async def DownloadPagePDFAvaliacao(page, nome_curso, linha, cont_curso, endereco_salvar, short_name_full, versao_ava, url_avaliacao):
#def DownloadPDFAvaliacao(page, nome_curso, linha, cont_curso, endereco_salvar): #linha, cont_curso):
    results = []   
    #print(page)
    #return results
    try:        
        time.sleep(1)
        #async with page.expect_download() as download_info:          
        #    await page.get_by_alt_text("Baixar em formato PDF").click()
        
        #download = await download_info.value
        #download = await download_info.value
        #print(f"URL para download: {download}")
        #url_para_pesquisa = str(await download_info.value)
        url_pesquisa_instance = url_avaliacao.find('?instance=')
        url_pesquisa_group = url_avaliacao.find('&group=')
        id_instance = url_avaliacao[url_pesquisa_instance+10:url_pesquisa_group]  
        short_name_full = short_name_full.replace(':',' -')
        short_name_full = short_name_full.replace('?','')
        short_name_full = short_name_full.replace('/','')
        short_name_full = short_name_full.replace('|','')
        short_name_full = short_name_full.replace(' ','')
        short_name_full = short_name_full.strip()
        short_name_full = short_name_full.upper()
        data_hora_agora = datetime.now()
        data_hora = data_hora_agora.strftime(f'%Y%m%d%H%M%S')
        pesquisa_turma = short_name_full.find('TURMA')
        if pesquisa_turma != -1:
            #turma = short_name_full[pesquisa_turma:]
            #nome_arquivo = nome_curso + " - Avaliação de Satisfação - " + turma + "-" + data_hora + ".pdf"
            nome_arquivo = "Avaliação de Satisfação-" + short_name_full + "-" + data_hora + ".pdf"
        else:
            #nome_arquivo = nome_curso + " - Avaliação de Satisfação - " + data_hora + ".pdf"
            nome_arquivo = "Avaliação de Satisfação-" + data_hora + ".pdf"
     
        await page.emulate_media(media='print')
        if versao_ava == 38:
            print(f'Print PDF => https://mooc38.escolavirtual.gov.br/mod/questionnaire/report.php?action=vall&instance={id_instance}&group=0&target=print')
            await page.goto(f'https://mooc38.escolavirtual.gov.br/mod/questionnaire/report.php?action=vall&instance={id_instance}&group=0&target=print')
        else:
            print(f'Print PDF => https://mooc41.escolavirtual.gov.br/mod/questionnaire/report.php?action=vall&instance={id_instance}&group=0&target=print')
            await page.goto(f'https://mooc41.escolavirtual.gov.br/mod/questionnaire/report.php?action=vall&instance={id_instance}&group=0&target=print')
        time.sleep(0.5)
        salvar_arquivo = os.path.join(endereco_salvar, nome_arquivo)
        await page.pdf(path=salvar_arquivo)
        time.sleep(0.5)
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