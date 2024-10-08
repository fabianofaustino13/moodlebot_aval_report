async def Login(page, login_evg, senha_evg):
    username = login_evg
    password = senha_evg
    login_url = page
    login_sucesso = False
    try:
        await page.locator("#usrCpfEmail").fill(username)
        await page.locator('xpath=//button[@class="btn btn-primary mb-3 w-100"]').click()
        await page.locator('#password').fill(password)
        await page.locator('xpath=//button[@class="btn btn-primary mb-3 w-100"]').click()
        pagina_logado = str(page)
        procura_logado = pagina_logado.find('https://www.escolavirtual.gov.br/home')
        if procura_logado != -1:
            login_sucesso = True     
        else:
            login_sucesso = False
                
    except:
        login_sucesso = False
    
    return login_sucesso




