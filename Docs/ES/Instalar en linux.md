## Instalación en Linux

Descarga el archivo `Linux.7z` y extráelo.
Abre la configuración de Wine ejecutando lo siguiente en la terminal:

```bash
winecfg
```

Ve a la pestaña `Integración con el escritorio`, luego en Tema selecciona `(Sin Tema)` y haz clic en Aceptar.

![winecfg](../PT-BR/img/winecfg.png)

Después de eso, ve a la carpeta `themes` dentro del archivo `.7z` extraído y elige el tema **Breeze** o **Dark**. Puedes ver la diferencia entre ellos a continuación:

| Dark                     | Breeze                       |
| ------------------------ | ---------------------------- |
| ![Dark](../img/dark.png) | ![Breeze](../img/breeze.png) |

Copia el texto del archivo `.txt` del tema que elegiste.
Luego, abre tu archivo `user.reg` de Wine, generalmente se encuentra en la carpeta `.wine`.
Dentro de `user.reg`, encuentra la sección `[Control Panel\Colors]`, reemplaza su contenido con el del archivo `.txt` y guarda `user.reg`.

![user.reg](../PT-BR/img/userreg.png)

Pega las carpetas del directorio `dll` en la carpeta `common` de tu biblioteca de Steam. Para la versión Flatpak de Steam, la ruta suele ser:

* `~/.var/app/com.valvesoftware.Steam/.steam/steam/steamapps/common`

Si estás usando la versión de Windows de Steam a través de Wine o una configuración diferente, pega los archivos en la carpeta `common` donde se encuentran tus juegos para Hammer++.
