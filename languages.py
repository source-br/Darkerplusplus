import locale

# Translations
translations = {
    "pt-br": {
        # main
        "no game": "Nenhum jogo selecionado",
        "please select": "Por favor, selecione pelo menos um jogo para continuar.",
        # welcome screen
        "title 1": "BEM VINDO AO DARKER++",
        "subtitle 1": "Deixe seu Hammer++ no modo escuro de maneira simples.",
        "continue": "Continuar",
        # Pop up
        "atention": "ATENÇÃO",
        "info": "O Darker++ utiliza o Ultrauxtheme <br> para poder aplicar o tema escuro, <br> somente prossiga caso já o tenha <br> instalado e reiniciado seu computador.",
        # selection screen
        "title 2": "JOGOS ENCONTRADOS",
        "subtitle 2": "Clique no jogo para selecionar sua pasta manualmente.",
        "install": "Instalar",
        # Pop ups
        "path": "Caminho Atualizado",
        "path 2": "Caminho para {game_name} atualizado com sucesso.",
        "invalid": "Caminho Inválido",
        "invalid 2": "O caminho selecionado não contém o jogo esperado.",
        "select": "Selecione o diretório do {game_name}",
        # end Screen
        "title 3": "PRONTO!",
        "subtitle 3": "Aproveite seu Hammer++ com o modo escuro.",
        "close": "Fechar",
    },
    "en": {
        # main
        "no game": "No game selected",
        "please select": "Please select at least one game to continue.",
        # welcome screen
        "title 1": "WELCOME TO DARKER++",
        "subtitle 1": "Set your Hammer++ to dark mode easily.",
        "continue": "Continue",
        # Pop up
        "atention": "ATTENTION",
        "info": "Darker++ uses Ultrauxtheme <br> to apply the dark theme. <br> Only proceed if you have already <br> installed it and restarted your computer.",
        # selection screen
        "title 2": "GAMES FOUND",
        "subtitle 2": "Click on the game to manually select its folder.",
        "install": "Install",
        # Pop ups
        "path": "Path Updated",
        "path 2": "Path to {game_name} successfully updated.",
        "invalid": "Invalid Path",
        "invalid 2": "The selected path does not contain the expected game.",
        "select": "Select the {game_name} directory.",
        # end screen
        "title 3": "DONE!",
        "subtitle 3": "Enjoy your Hammer++ in dark mode.",
        "close": "Close",
    },
    "es": {
        # main
        "no game": "No se seleccionó ningún juego",
        "please select": "Por favor, seleccione al menos un juego para continuar.",
        # welcome screen
        "title 1": "BIENVENIDO A DARKER++",
        "subtitle 1": "Configura tu Hammer++ en modo oscuro fácilmente.",
        "continue": "Continuar",
        # Pop up
        "atention": "ATENCIÓN",
        "info": "Darker++ utiliza Ultrauxtheme <br> para aplicar el tema oscuro. <br> Solo continúe si ya lo ha <br> instalado y reiniciado su computadora.",
        # selection screen
        "title 2": "JUEGOS ENCONTRADOS",
        "subtitle 2": "Haga clic en el juego para seleccionar manualmente su carpeta.",
        "install": "Instalar",
        # Pop ups
        "path": "Ruta actualizada",
        "path 2": "La ruta hacia {game_name} se actualizó con éxito.",
        "invalid": "Ruta inválida",
        "invalid 2": "La ruta seleccionada no contiene el juego esperado.",
        "select": "Seleccione el directorio de {game_name}",
        # end screen
        "title 3": "¡LISTO!",
        "subtitle 3": "Disfruta de tu Hammer++ en modo oscuro.",
        "close": "Cerrar",
    }
}

# Detectar o idioma do sistema operacional
system_language = locale.getdefaultlocale()[0]  # Retorna algo como 'pt_BR'

# Converter o idioma para o formato usado nas traduções (ex: 'pt-br')
if system_language:
    formatted_language = system_language.replace('_', '-').lower()
else:
    formatted_language = "en"  # Idioma padrão em caso de erro

# Verificar se o idioma detectado possui tradução disponível
current_language = formatted_language if formatted_language in translations else "en"
