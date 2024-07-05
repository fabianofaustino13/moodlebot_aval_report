from datetime import datetime
import aspose.pdf as ap
import time

async def CriarArquivoPDF(page, nome_curso, linha, cont_curso, endereco_salvar):
    results = []    
    #return results
    try:        
        time.sleep(0.5)
        # Inicializar objeto de documento
        document = ap.Document()
        # Adicionar Página
        arquivo = document.pages.add()
        # Inicializar objeto textfragment
        text_fragment = ap.text.TextFragment("Nada a ser mostrado")
        # Adicionar fragmento de texto à nova página
        arquivo.paragraphs.add(text_fragment)
        data_hora_agora = datetime.now()
        data_hora = data_hora_agora.strftime(f'%Y%m%d-%H%M%S')
        # Salvar PDF atualizado
        document.save(endereco_salvar + f"/{nome_curso} - Nada a ser mostrado {data_hora}.pdf")
    except Exception as err:
        results+=  [f"Problema ao Criar um Arquivo em PDF. Na linha {cont_curso}: {linha}. Uma possível falha de conexão. Se possível, tente rodar novamente."]
        results+=  [f"Erro {err}, {type(err)=}."]
        print(f"Erro {err}, {type(err)=}.")

    return results