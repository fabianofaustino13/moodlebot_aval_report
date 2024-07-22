@echo off
timeout /t 2
echo #######################
echo Iniciando a Instalacao.
echo #######################
set minhaPasta=C:\moodlebot_avaliacao_report\
rem Arquivo txt que o processo vai ler com o nome dos arquivos.
set meuArquivo=Relatorio_Oferta_Piloto.bat
echo ########################################
echo Procurando pelo arquivo: %meuArquivo%
echo ########################################
timeout /t 2
if not exist %meuArquivo% (
	echo ########################
	echo Instalando Python
	echo ########################
	timeout /t 2
	C:\moodlebot_user_report\python-3.12.4-amd64.exe /quiet /passive InstallAllUsers=1 PrependPath=1 Include_test=0 InstallLauncherAllUsers=1 DefaultAllUsersTargetDir=C:\moodlebot_avaliacao_report\Python\ DefaultCustomTargetDir=C:\moodlebot_avaliacao_report\Python\
	echo ########################
	echo Instalando a biblioteca.
	echo ########################
	timeout /t 2
	C:\moodlebot_avaliacao_report\Python\Scripts\pip.exe install -r requirements.in
	echo ##################
	echo Criando o arquivo.
	echo ##################
	echo streamlit run --client.showSidebarNavigation=False .\main.py >> Relatorio_Oferta_Piloto.bat
) else (
	echo ##################
	echo Arquivo existente.
	echo ##################
)
echo #########################################################
echo Crie um ATALHO do arquivo %meuArquivo% em seu Desktop.
echo #########################################################
@pause
