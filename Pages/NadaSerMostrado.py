async def NadaSerMostrado(page):
    results = []    
    #return results
    try: 
        procurar_nada_mostrado = await page.locator('xpath=//div[@role="main"]').inner_text()
        nada_ser_mostrado = procurar_nada_mostrado.upper()
        nada_encontrado = nada_ser_mostrado.find('NADA A SER MOSTRADO')
    except Exception as err:
        results+=  [f"Problema na Função Nada a ser mostrado. Uma possível falha de conexão. Se possível, tente rodar novamente."]
        results+=  [f"Erro {err}, {type(err)=}."]
        print(f"Erro {err}, {type(err)=}.")
    return nada_encontrado