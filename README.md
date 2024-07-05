# moodlebot_relatorio
Moodlebot para baixar relatórios

#Instalar dependências.
pip install -r requirements.in

#Criar requerimentos
pip freeze > requirements.in

#Iniciar venv
.\moodlebot\venv\Scripts\Activate.ps1

#Criar venv
mkdir novo_projeto
cd novo_projeto/
python3 -m venv nome_do_ambiente_virtual

#RODAR
python -m streamlit run .\main.py
ou
python -m streamlit run --client.showSidebarNavigation=False .\main.py