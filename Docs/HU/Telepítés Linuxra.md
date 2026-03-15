## Telepítés Linuxra

Töltsd le a `Linux.7z` fájlt és csomagold ki.
Nyisd meg a Wine beállításait (futtasd a következő parancsokat a terminálban:)

```bash
winecfg
```

Menj a `Desktop Integration` tabra, és a Theme alatt, válaszd a `(No Theme)` lehetőséget, és nyomj az OK-ra.

Ezután menj a `themes` mappába ami a kicsomagolt `.7z` fájlban található, és válaszd vagy a **Breeze** vagy a **Dark** témát. A kettő közötti különbség itt található:

| Dark                     | Breeze                       |
| ------------------------ | ---------------------------- |
| ![Dark](img/dark.png) | ![Breeze](img/breeze.png) |

Másold ki a szöveget a kiválasztott téma `.txt` fájlából.
Ezután nyisd meg a Wine `user.reg` fájlodat, ami általában a `.wine` mappában található.
Az `user.reg`-ben, keresd meg a `[Control Panel\Colors]` részt, cseréld ki a tartalmát a `.txt` fájl tartalmára, és mentsd el a `user.reg`-et.

Másold át a mappákat a `dll` könyvtárból a Steam `common` mappájába. A Flatpak verziós Steam-nek, az útvonal általában a következő:

* `~/.var/app/com.valvesoftware.Steam/.steam/steam/steamapps/common`

Ha a Steam Windows-os verzióját használod Wine-on vagy más beállításon keresztül, másold át a fájlokat a `common` mappába ahol a Hammer++-os játékaid találhatók.
