import locale

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
    "ru": {
        # main
        "no game": "Нет выбранных игр",
        "please select": "Пожалуйста, выберите минимум одну игру для продолжения.",
        # welcome screen
        "title 1": "ДОБРО ПОЖАЛОВАТЬ В DARKER++",
        "subtitle 1": "Настройте ваш Hammer++ в темную тему легко.",
        "continue": "Продолжить",
        # Pop up
        "atention": "ВНИМАНИЕ",
        "info": "Darker++ изпользует Ultrauxtheme <br> для применения темной темы. <br> Продолжайте только если вы <br> установили это и перезапустили компьютер.",
        # selection screen
        "title 2": "ИГРЫ НАЙДЕНЫ",
        "subtitle 2": "Нажмите на папку игры чтобы выбрать её.",
        "install": "Установить",
        # Pop ups
        "path": "Путь обновлен",
        "path 2": "Путь к {game_name} успешно обновлен.",
        "invalid": "Invalid Path",
        "invalid 2": "Выбранный путь не имеет ожидаемую игру.",
        "select": "Выберите директорию {game_name}.",
        # end screen
        "title 3": "ГОТОВО!",
        "subtitle 3": "Наслаждайтесь вашим Hammer++ в темном режиме.",
        "close": "Закрыть",
    },
    "es-es": {
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
    },
    "hu-hu": {
        # main
        "no game": "Nincs játék kiválasztva",
        "please select": "Egy játékot válasszon ki a folytatáshoz",
        # welcome screen
        "title 1": "ÜDVÖZÖLJÜK A DARKER++-ban",
        "subtitle 1": "Állítsa át a Hammer++-t sötét módra egyszerűen.",
        "continue": "Folytatás",
        # Pop up
        "atention": "FIGYELEM",
        "info": "Darker++ az Ultrauxtheme-et használja <br> hogy a sötét módot alkalmazza. <br> Csak akkor folytassa, ha már <br> letöltötte és újraindította a számítógépet.",
        # selection screen
        "title 2": "JÁTÉKOK TALÁLVA",
        "subtitle 2": "Nyomjon egy játékra hogy manuálisan kiválassza a mappáját.",
        "install": "Telepítés",
        # Pop ups
        "path": "Útvonal frissítve",
        "path 2": "{game_name} útvonala sikeresen frissítve.",
        "invalid": "Helytelen Útvonal",
        "invalid 2": "A kiválasztott útvonal nem tartalmazza a várható játékot.",
        "select": "Válassza ki a {game_name} könyvtárat.",
        # end screen
        "title 3": "KÉSZ!",
        "subtitle 3": "Élvezze a Hammer++-t sötét módban.",
        "close": "Bezárás",
    }
}

# Detectar o idioma do sistema operacional
system_language = locale.getdefaultlocale()[0]

# Converter o idioma para o formato usado nas traduções (ex: 'pt-br')
if system_language:
    formatted_language = system_language.replace('_', '-').lower()
else:
    formatted_language = "en"  # Idioma padrão em caso de erro

# Verificar se o idioma detectado possui tradução disponível
current_language = formatted_language if formatted_language in translations else "en"

print(f"idioma: {formatted_language}")
