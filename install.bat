@echo off
timeout /t 2
echo #######################
echo Iniciando o teste.
echo #######################
set minhaPasta=C:\moodlebot_avaliacao_report\
set pasta_atual=%cd%
echo ########################################
echo Procurando pelo arquivo: %minhaPasta%
echo ########################################
set meuArquivo=Relatorio_Oferta_Piloto.bat
echo ########################################
timeout /t 2
IF not exist %minhaPasta% (
	echo ########################################################################
	echo Criando a pasta de destino: C:\moodlebot_avaliacao_report\
	echo #######################################################################
	mkdir %minhaPasta%
	echo #######################################################################	
	timeout /t 2
	IF not exist %meuArquivo% (
		echo Criando o arquivo.
		echo #######################################################################
		echo streamlit run --client.showSidebarNavigation=False .\main.py >> Relatorio_Oferta_Piloto.bat		
		echo #######################################################################
		echo Copiando os arquivos....
		Xcopy /E %pasta_atual% %minhaPasta%	
		echo #######################################################################
		echo Instalando Python
		echo #######################################################################
		timeout /t 2
		C:\moodlebot_avaliacao_report\python-3.12.4-amd64.exe /quiet /passive InstallAllUsers=1 PrependPath=1 Include_test=0 InstallLauncherAllUsers=1 DefaultAllUsersTargetDir=C:\moodlebot_avaliacao_report\Python\ DefaultCustomTargetDir=C:\moodlebot_avaliacao_report\Python\
		echo #######################################################################
		echo Instalando a biblioteca.
		echo #######################################################################
		timeout /t 2
		C:\moodlebot_avaliacao_report\Python\Scripts\pip.exe install -r requirements.in
		echo #######################################################################		
	)	
) else (
	cd C:\moodlebot_avaliacao_report
	timeout /t 5
	echo %cd%
	timeout /t 5
	echo %meuArquivo%
	IF not exist %meuArquivo% (
		echo #######################################################################
		echo Instalando Python
		echo #######################################################################
		timeout /t 2
		C:\moodlebot_avaliacao_report\python-3.12.4-amd64.exe /quiet /passive InstallAllUsers=1 PrependPath=1 Include_test=0 InstallLauncherAllUsers=1 DefaultAllUsersTargetDir=C:\moodlebot_avaliacao_report\Python\ DefaultCustomTargetDir=C:\moodlebot_avaliacao_report\Python\
		echo #######################################################################
		echo Instalando a biblioteca.
		echo #######################################################################
		timeout /t 2
		C:\moodlebot_avaliacao_report\Python\Scripts\pip.exe install -r requirements.in
		echo #######################################################################
		echo Criando o arquivo.
		echo #######################################################################
		echo streamlit run --client.showSidebarNavigation=False .\main.py >> Relatorio_Oferta_Piloto.bat
	)	
)
echo #########################################################
echo Crie um ATALHO do arquivo %meuArquivo% em seu Desktop.
echo #########################################################
@pause