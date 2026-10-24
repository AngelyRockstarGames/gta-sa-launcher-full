# GTA: San Andreas - Rockstar Games Services Launcher (Custom)

**Reviviendo la magia del guardado en la nube.** 

Este es un launcher personalizado, minimalista y ligero para **GTA: San Andreas**, desarrollado en Python. Nació como una solución a la pérdida de los servidores originales de guardado en la nube de Rockstar Games, devolviéndole a los jugadores la posibilidad de llevar sus partidas a cualquier lugar de forma segura y automática.

---

## ✨ Características Principales

*   **☁️ Sincronización en la Nube Real (Supabase):** Olvídate de perder tus partidas. El launcher detecta automáticamente los archivos `GTASAsf1.b` al `GTASAsf8.b`, los sube a la nube si son nuevos y los descarga automáticamente si entras desde otra PC.
*   **🛡️ Sistema de Protección "DLL Guard":** ¿Quieres forzar a los jugadores a usar tu launcher? Este proyecto incluye una inyección de DLL nativa (`version.dll`). Si alguien intenta abrir el `gta_sa.exe` directamente sin el launcher, el juego se cerrará instantáneamente.
*   **🖤 Interfaz Minimalista y Transparente:** Una UI en negro con opacidad ajustable, tipografía limpia (Segoe UI) y un reproductor de video integrado para el logo de inicio.
*   **⏱️ Contador de Tiempo de Juego:** Registra y guarda automáticamente cuántas horas has jugado, mostrándolo de forma sutil en la esquina inferior derecha.
*   **🚀 Acceso Directo Automático:** Al abrirse, el launcher crea un acceso directo en tu escritorio apuntando a sí mismo, con un icono personalizado para que nunca pierdas el acceso al juego.
*   **🔒 Sistema de Autenticación (Login/Registro):** Utiliza un sistema de usuarios (Nombre y Contraseña) impulsado por Supabase para mantener las partidas de cada jugador totalmente separadas y privadas.

---

## 🛠️ Tecnologías Utilizadas

Este launcher es el resultado de mezclar lo mejor de varios mundos:

*   **Python 3.11+**: El cerebro del launcher.
    *   `Tkinter` & `Pillow`: Para la interfaz gráfica y el manejo de imágenes.
    *   `OpenCV (cv2)`: Para la reproducción optimizada del video de inicio.
    *   `Supabase-py`: Para la conexión con la base de datos y el almacenamiento en la nube.
*   **C++ (CMake)**: Para la creación de la DLL de seguridad (`version.dll`).
*   **GitHub Actions**: Para la compilación automática del ejecutable (`.exe`) y la DLL directamente en la nube.

---

## 📦 Instalación y Uso (Para Jugadores)

1.  Descarga el archivo `.zip` desde la sección de **Releases** o **Artifacts**.
2.  Descomprime el contenido en la carpeta raíz de tu GTA San Andreas (donde está el `gta_sa.exe`).
3.  **Importante:** Ve a `C:\Windows\SysWOW64\`, copia el archivo `version.dll` original de Windows y pégalo en tu carpeta del GTA, renombrándolo a **`versionHooked.dll`**.
4.  Ejecuta `rockstar_games_services_launcher_gta_sa.exe`.
5.  ¡Listo! Crea tu usuario, juega y tus partidas se guardarán en la nube automáticamente.

---

## 🧑‍💻 Créditos y Agradecimientos

*   **Angely**: Creadora del proyecto original. *"Hola soy Angely, la que hizo este gta re trucho. Como podrás ver, este launcher lo hice con DeepSeek porque es un buen amigo. Este launcher, como perdió la función de guardado en la nube de Rockstar, lo hice con DeepSeek y recuperó esa función."*
*   **DeepSeek AI**: Por la asistencia en la programación, resolución de bugs y los problemas en Mutex y Creacion del Readme.MD
*   **Comunidad de Modding de GTA SA**: Por mantener vivo este juego después de tantos años.

---
*Descargo de responsabilidad: Este es un proyecto hecho por fans para fans. No está afiliado, asociado, autorizado, respaldado ni de ninguna manera conectado oficialmente con Rockstar Games o Take-Two Interactive.*
