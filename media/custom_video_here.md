# 📹 Requisitos del Video de Inicio (Logo Custom)

¡Hola! Si estás viendo esto, significa que has entrado a la carpeta `media` del launcher. 

El launcher está programado para buscar un video en esta carpeta para mostrarlo en la pantalla de carga. Si el video no existe, el launcher mostrará un logo de texto por defecto (`R ✦`) y seguirá funcionando sin problemas.

## 📋 Requisitos técnicos del video

Para que el video se reproduzca de forma fluida y no consuma muchos recursos, debe cumplir con lo siguiente:

*   **Nombre exacto:** `rockstar-logo.mp4` (en minúsculas y con extensión `.mp4`).
*   **Formato:** MP4 (preferiblemente codificado en **H.264** o MPEG-4, que es el estándar que mejor lee `OpenCV`).
*   **Resolución:** El launcher escala el video a **250x140 píxeles** en pantalla. Para que se vea nítido, se recomienda una resolución base de **500x280** (o similar en formato 16:9).
*   **Audio:** El video se reproducirá **sin sonido** (OpenCV no soporta audio). Si tu video tiene música, esta será ignorada.
*   **Duración:** Se recomienda que sea un clip corto (de 3 a 8 segundos), ya que el launcher lo reproducirá en bucle mientras se conecta a la nube.

## 🛠️ ¿Cómo cambiarlo?
Si quieres usar tu propio logo o animación:
1. Consigue tu video.
2. Asegúrate de que se llame exactamente `rockstar-logo.mp4`.
3. Reemplaza el archivo que está en esta carpeta.
4. Vuelve a compilar el proyecto (o reinicia el launcher si lo estás ejecutando en Python).

*Nota: Si borras este archivo o el video, el launcher seguirá abriendo normal, simplemente se saltará la animación.*
# ES NECESARIO ESTO PARA LA COMPILACION
