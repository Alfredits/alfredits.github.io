"""Genera la Bóveda de la comunidad (alfredits.github.io/comunidad/).

Uso: python _fuentes/build_comunidad.py   (desde la carpeta "Pagina web")
La carpeta _fuentes no se publica (GitHub Pages ignora las carpetas que empiezan por _).
Para añadir un recurso: agrega un dict a RECURSOS y vuelve a ejecutar.
"""

from html import escape
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
OUT = RAIZ / "comunidad"
SITIO = "https://alfredits.github.io"
IG = "https://www.instagram.com/alfredits.ia/"
TT = "https://www.tiktok.com/@alfredits.ia"
FECHA = "2026-11-19"


# ---------------------------------------------------------------- piezas comunes

def code(cid, label, texto, scroll=False):
    cls = "code code--scroll" if scroll else "code"
    return (f'<div class="{cls}"><div class="code__bar"><span class="label">{escape(label)}</span>'
            f'<button class="copy" type="button" data-copy="{cid}">Copiar</button></div>'
            f'<pre id="{cid}">{escape(texto.strip())}</pre></div>')


def nota(texto):
    return f'<div class="note"><span class="label">Nota de Alfredo</span><p>{texto}</p></div>'


def head(titulo, desc, ruta, nivel):
    pre = "../" * nivel
    url = f"{SITIO}/{ruta}"
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(titulo)}</title>
<meta name="description" content="{escape(desc)}">
<meta name="author" content="Alfredo Navea">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0A0A0F">
<meta name="color-scheme" content="dark">
<link rel="icon" href="{pre}../assets/img/isotipo-color.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{pre}../assets/img/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Alfredits">
<meta property="og:title" content="{escape(titulo)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="es_ES">
<meta property="og:image" content="{SITIO}/assets/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="{pre}../assets/fonts/Coolvetica-Rg.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap">
<link rel="stylesheet" href="{pre}assets/comunidad.css?v=2">
</head>"""


def barra(nivel):
    pre = "../" * nivel
    return f"""<header class="top"><div class="wrap top__in">
  <a class="top__brand" href="{pre or './'}"><img src="{pre}../assets/img/isotipo-color.svg" alt="" width="26" height="26">Bóveda · Alfredits</a>
  <nav class="top__links" aria-label="Secciones">
    <a href="{pre}#gratis">Recursos</a>
    <a href="{pre}guia/">Guía</a>
    <a class="hide-sm" href="{pre}../">Mi web</a>
  </nav>
</div></header>"""


def pie(nivel):
    pre = "../" * nivel
    return f"""<footer class="foot"><div class="wrap foot__in">
  <span>Hecho por Alfredo Navea · <a href="{IG}" rel="noopener">@alfredits.ia</a></span>
  <span><a href="{pre or './'}">Bóveda</a> · <a href="{pre}../">Mi web</a> · <a href="{TT}" rel="noopener">TikTok</a></span>
</div></footer>
<script src="{pre}assets/comunidad.js?v=1" defer></script>
</body>
</html>
"""


def cierre(slug, frase_amigo):
    otros = [r for r in RECURSOS if r["slug"] != slug][:3]
    links = "".join(f'<a href="../{r["slug"]}/"><span>{escape(r["titulo"])}</span><span>{r["palabra"]} →</span></a>' for r in otros)
    return f"""<section class="cta">
  <span class="tc">00:00:59:29 · fin</span>
  <h2>¿Te sirvió? Pásaselo a {escape(frase_amigo)}.</h2>
  <p>Cada semana regalo una herramienta nueva para editar con IA. Sígueme para no perderte la próxima.</p>
  <div class="btns">
    <a class="btn" href="{IG}" rel="noopener">Seguir en Instagram</a>
    <a class="btn btn--ghost" href="{TT}" rel="noopener">Seguir en TikTok</a>
    <button class="btn btn--ghost" type="button" data-copy="url-{slug}">Copiar enlace</button>
  </div>
  <span id="url-{slug}" hidden>{SITIO}/comunidad/{slug}/</span>
</section>
<section class="block"><h2>Más recursos gratis</h2><div class="more">{links}</div></section>"""


# ---------------------------------------------------------------- contenido

GANCHO_PROMPT = """Eres un editor de reels experto en retención. Voy a pasarte el guion de un reel de [DURACIÓN, por ejemplo 35] segundos para [PLATAFORMA: Instagram / TikTok]. Mi público es [QUIÉN TE VE, por ejemplo: editores que empiezan].

Escríbeme 10 ganchos para el primer segundo del reel. Reglas:
- Máximo 12 palabras cada uno, en español natural, como lo diría una persona a cámara.
- Usa 10 tipos distintos, uno por gancho: cifra concreta, pregunta, resultado primero, error común, contradicción con lo que todos creen, antes y después, "yo ya no…", reto o apuesta, secreto de oficio y advertencia.
- Solo usa cifras y datos que estén en mi guion. No inventes resultados.
- Nada de clickbait que el video no cumpla: el gancho tiene que prometer lo que el reel entrega.

Para cada gancho dame:
1. La frase.
2. Qué se ve en el primer segundo (la imagen o el plano exacto).
3. El texto en pantalla (máximo 5 palabras).

Al final, marca los 3 que más retendrían y explica en una línea por qué cada uno.

Guion:
[PEGA AQUÍ TU GUION]"""

SUBS_PROMPT = """Eres mi editor de subtítulos. En la carpeta Brutos está mi video [NOMBRE DEL VIDEO].

1. Transcríbelo en mi computadora con Whisper (faster-whisper), con el tiempo de cada palabra. Idioma: [español].
2. Crea subtítulos estilo karaoke: bloques de 2 a 4 palabras; la frase aparece en gris claro y cada palabra se enciende en [COLOR, por ejemplo #19D3C5] justo cuando la digo.
3. Fuente [FUENTE], grande y fácil de leer, sin fondo y con una sombra suave. Colócalos a la altura del pecho, nunca encima de la cara, y dentro de la zona segura de un video vertical de 1080×1920.
4. Máximo una palabra clave por frase puede ir un poco más grande. Sin puntos finales.
5. Antes de renderizar, revisa la transcripción y enséñame las palabras dudosas para corregirlas.
6. Renderiza con FFmpeg (subtítulos ASS quemados en el video) y guárdalo en Exportados como [NOMBRE]-subs-v1.mp4. Guarda también el archivo .ass por si quiero cambiar algo.

Si te falta una herramienta (FFmpeg, Python o faster-whisper), instálala pidiéndome permiso antes."""

RITMO_PROMPT = """Quiero quitar los silencios de mi voz en off y acelerarla un poco.

1. Revisa si tengo Python y FFmpeg instalados. Si falta alguno, instálalo pidiéndome permiso.
2. Crea en esta carpeta el archivo voz_ritmo.py con el código que te pego abajo, sin cambiarlo.
3. Ejecútalo con mi audio: python voz_ritmo.py Brutos/[MI-AUDIO].mp3 Exportados/[MI-AUDIO]-rapida.wav
4. Dime cuánto duraba antes y cuánto dura ahora.

Código:
[PEGA AQUÍ EL SCRIPT]"""

TEXTO_PROMPT = """Quiero transcribir mis videos gratis en mi computadora.

1. Revisa si tengo Python 3.10 o superior y FFmpeg. Si falta alguno, instálalo pidiéndome permiso.
2. Instala el paquete faster-whisper con pip. Si tengo tarjeta NVIDIA, configúralo para usarla; si no, que funcione en el procesador.
3. Crea en esta carpeta el archivo transcribir.py con el código que te pego abajo, sin cambiarlo.
4. Pruébalo con mi video: python transcribir.py Brutos/[MI-VIDEO].mp4 --idioma es
5. Enséñame las primeras líneas del .srt para comprobar que salió bien.

Código:
[PEGA AQUÍ EL SCRIPT]"""

CODEX_DELEGAR = """## Trabajo con Codex
- Cuando una tarea sea escribir mucho código (armar el proyecto de un video, animaciones, scripts largos o arreglos grandes), pásasela a Codex con /codex:rescue y un brief claro: qué hay que hacer, en qué archivos y cómo se ve terminado.
- Tú (Claude) decides, escribes el brief y revisas lo que devuelve Codex antes de enseñármelo. Si algo está mal, se lo devuelves a Codex con las correcciones en una sola tanda.
- Las tareas cortas (una edición pequeña, una pregunta) las haces tú directamente."""

MEMORIA_TEMPLATE = """# CLAUDE.md · mi forma de editar
Lee este archivo antes de cualquier tarea. Si te corrijo algo que sirva para siempre, añádelo aquí.

## Quién soy
- Edito [reels / TikToks / shorts] para [tipo de clientes o tu propio contenido], en [idioma].
- Trabajo en [CapCut / Premiere / DaVinci]. Tú me ayudas con lo pesado: cortar, transcribir, subtítulos y animaciones.

## Carpetas
- Brutos: lo que grabo. Nunca borres nada de aquí.
- Referencias: videos que me gustan.
- Exportados: lo terminado. Cada cambio es una versión nueva (v1, v2, v3); nunca sobrescribas la anterior.

## Formato
- Vertical 1080×1920, 30 fps. Audio normalizado a −14 LUFS.
- Duración habitual: [30–60] s.

## Ritmo
- Gancho en el primer segundo, con la mejor imagen. Nada de intros.
- Algo nuevo cada 1–2 segundos: corte, zoom, texto o b-roll.
- Silencios de más de 0,3 s fuera.

## Subtítulos
- Bloques cortos (2 a 4 palabras) con la palabra clave destacada en [color].
- Fuente [fuente], sin fondo, a la altura del pecho. Nunca encima de la cara.
- Una palabra clave por frase como máximo.

## Colores y marca
- Colores: [#2F6BFF, #19D3C5…]. Fuentes: [títulos / texto].

## Nunca hacer
- [Ejemplo: glow en los subtítulos.]
- [Ejemplo: música más alta que la voz.]
- [Aquí van los errores que ya te corregí.]

## Cómo trabajamos
- Antes de un cambio grande, dime el plan en 3 líneas.
- Al terminar, dime qué hiciste y qué no pudiste comprobar."""

RECURSOS = [
    dict(
        slug="gancho", palabra="GANCHO", tipo="Prompt", titulo="10 ganchos para tu reel",
        linea="Pega tu guion y Claude (o ChatGPT) te devuelve 10 ganchos distintos, con la imagen del primer segundo y el texto en pantalla.",
        meta=["Prompt", "Claude o ChatGPT", "2 minutos", "Gratis"],
        amigo="ese amigo que se queda media hora pensando cómo empezar su video",
        pasos=["Copia el prompt de abajo.", "Pégalo en Claude o ChatGPT y cambia lo que va entre [corchetes].", "Pega tu guion al final y envíalo."],
        cuerpo=lambda: (
            '<section class="block"><h2>El prompt</h2>' + code("p-gancho", "Escríbele a Claude o ChatGPT", GANCHO_PROMPT) + '</section>'
            '<section class="block"><h2>Cómo elegir</h2><ul>'
            '<li><b>No uses el gancho tal cual.</b> Elige el que dirías en voz alta y cámbialo con tus palabras.</li>'
            '<li>Graba 2 o 3 versiones y quédate con la que suene más natural.</li>'
            '<li>Si el final del video no cumple lo que promete el gancho, cambia el gancho, no el video.</li>'
            '</ul>' + nota("La IA me da las opciones; el criterio lo pongo yo. De los 10, casi siempre termino mezclando dos.") + '</section>'
        ),
    ),
    dict(
        slug="subs", palabra="SUBS", tipo="Prompt", titulo="Subtítulos karaoke con Claude",
        linea="El prompt exacto para que Claude transcriba tu video y le ponga subtítulos que se encienden palabra por palabra.",
        meta=["Prompt", "Claude Code o Codex", "Unos minutos", "Gratis"],
        amigo="ese amigo que todavía hace los subtítulos a mano",
        pasos=["Abre Claude Code (o Codex) en la carpeta de tu proyecto.", "Copia el prompt y cambia lo que va entre [corchetes].", "Revisa las palabras dudosas que te enseña y deja que renderice."],
        cuerpo=lambda: (
            '<section class="block"><h2>El prompt</h2>' + code("p-subs", "Escríbele a Claude Code o Codex", SUBS_PROMPT) + '</section>'
            '<section class="block"><h2>Antes de empezar</h2><ul>'
            '<li>Necesitas <b>Claude Code</b> (plan Pro de Claude) o <b>Codex</b> (incluido en ChatGPT, también en el plan gratis). Si no lo tienes, empieza por <a href="../guia/">la guía de tu primer video</a>.</li>'
            '<li>Ten tu carpeta con las subcarpetas <b>Brutos</b> y <b>Exportados</b>.</li>'
            '<li>¿No tienes tarjeta NVIDIA? Funciona igual, solo tarda más en transcribir.</li>'
            '</ul>' + nota("Lo que antes me tomaba una hora en CapCut, palabra por palabra, ahora son minutos. El secreto está en el punto 5: revisar las palabras dudosas antes de renderizar.") + '</section>'
        ),
    ),
    dict(
        slug="estilo", palabra="ESTILO", tipo="Checklist", titulo="Checklist de retención",
        linea="Las 3 reglas que aplico en cada reel, en una lista para repasar antes de exportar. Se marca aquí mismo.",
        meta=["Checklist", "CapCut, Premiere o cualquiera", "5 minutos por video", "Gratis"],
        amigo="alguien que edite y quiera que vean sus videos completos",
        pasos=["Abre tu reel terminado, antes de exportar.", "Repasa cada casilla y márcala aquí.", "Si una queda sin marcar, arréglala antes de publicar."],
        cuerpo=lambda: estilo_cuerpo(),
    ),
    dict(
        slug="ritmo", palabra="RITMO", tipo="Script", titulo="Quita los silencios de tu voz",
        linea="Un script que deja cada pausa en una décima de segundo y acelera la voz un 10 % sin que suene rara.",
        meta=["Script", "Python + FFmpeg", "Segundos", "Gratis"],
        amigo="ese amigo que sigue cortando silencios a mano",
        pasos=["Copia el prompt y el script.", "Pégalos en Claude Code o Codex: él instala lo que falte y lo ejecuta.", "Arrastra el audio nuevo a CapCut."],
        cuerpo=lambda: (
            '<section class="block"><h2>1 · El prompt (Claude instala todo por ti)</h2>' + code("p-ritmo", "Escríbele a Claude Code o Codex", RITMO_PROMPT) + '</section>'
            '<section class="block"><h2>2 · El script</h2><p>Pégalo donde dice [PEGA AQUÍ EL SCRIPT], o descárgalo.</p>'
            + code("s-ritmo", "voz_ritmo.py", (OUT / "ritmo" / "voz_ritmo.py").read_text(encoding="utf-8"), scroll=True)
            + '<div class="dl"><a class="btn btn--ghost" href="voz_ritmo.py" download>Descargar voz_ritmo.py</a></div></section>'
            '<section class="block"><h2>Qué hace exactamente</h2><ul>'
            '<li>Busca las pausas de más de <b>0,22 s</b> y las deja en <b>0,1 s</b>.</li>'
            '<li>Acelera la voz a <b>1,1×</b> sin cambiar el tono.</li>'
            '<li>Te devuelve un .wav limpio para editar.</li>'
            '</ul>' + nota("Funciona solo con audio: úsalo con tu voz en off. Si lo usas con un video donde hablas a cámara, el audio se recorta pero la imagen no, y se desincronizan.") + '</section>'
        ),
    ),
    dict(
        slug="texto", palabra="TEXTO", tipo="Script", titulo="Transcribe gratis en tu computadora",
        linea="Whisper en tu computadora: cada palabra con su tiempo exacto, más un .srt listo para CapCut. Sin pagar suscripciones.",
        meta=["Script", "Python + Whisper", "Mac y Windows", "Gratis"],
        amigo="ese amigo que sigue pagando por transcribir",
        pasos=["Copia el prompt y el script.", "Pégalos en Claude Code o Codex: él instala Whisper y lo prueba contigo.", "Usa el .srt en CapCut o el .json para cortes y subtítulos precisos."],
        cuerpo=lambda: (
            '<section class="block"><h2>1 · El prompt (Claude instala todo por ti)</h2>' + code("p-texto", "Escríbele a Claude Code o Codex", TEXTO_PROMPT) + '</section>'
            '<section class="block"><h2>2 · El script</h2><p>Pégalo donde dice [PEGA AQUÍ EL SCRIPT], o descárgalo.</p>'
            + code("s-texto", "transcribir.py", (OUT / "texto" / "transcribir.py").read_text(encoding="utf-8"), scroll=True)
            + '<div class="dl"><a class="btn btn--ghost" href="transcribir.py" download>Descargar transcribir.py</a></div></section>'
            '<section class="block"><h2>Qué te devuelve</h2><ul>'
            '<li><b>mi-video.srt</b>: subtítulos por frases. En CapCut: Texto → Subtítulos → Importar subtítulos (o arrástralo).</li>'
            '<li><b>mi-video.palabras.json</b>: cada palabra con su inicio y su fin. Es lo que necesita Claude para cortar silencios y sincronizar subtítulos y animaciones.</li>'
            '<li>Con tarjeta NVIDIA tarda segundos; en el procesador, unos minutos.</li>'
            '</ul>' + nota("Así transcribo todos mis videos. La primera vez descarga el modelo (unos cientos de MB); después funciona sin internet.") + '</section>'
        ),
    ),
    dict(
        slug="codex", palabra="CODEX", tipo="Guía", titulo="Conecta Codex a Claude y ahorra límite",
        linea="Instala el plugin oficial de Codex en Claude Code: Claude dirige y revisa, Codex escribe el código pesado con su propio límite.",
        meta=["Guía", "Claude Code + ChatGPT", "10 minutos", "Gratis"],
        amigo="ese amigo que siempre se queda sin límite",
        pasos=["Abre Claude Code en tu carpeta.", "Pega los 3 comandos, uno por uno.", "Añade las reglas a tu CLAUDE.md para que Claude delegue solo."],
        cuerpo=lambda: (
            '<section class="block"><h2>Lo que necesitas</h2><ul>'
            '<li><b>Claude Code</b> (en la app de escritorio de Claude, pestaña Code; pide el plan Pro).</li>'
            '<li>Una <b>cuenta de ChatGPT</b>. Codex está incluido en todos los planes, también en el gratis, con límites distintos.</li>'
            '</ul></section>'
            '<section class="block"><h2>1 · Añade el plugin</h2><p>Escribe en Claude Code:</p>'
            + code("c1", "En Claude Code", "/plugin marketplace add openai/codex-plugin-cc") + code("c2", "En Claude Code", "/plugin install codex@openai-codex") +
            '<p>Es el plugin oficial de OpenAI. Si te pregunta dónde instalarlo, elige el ámbito de usuario para tenerlo en todas tus carpetas. Si después no te aparecen los comandos /codex, cierra y vuelve a abrir la app de Claude.</p></section>'
            '<section class="block"><h2>2 · Prepara Codex</h2>' + code("c3", "En Claude Code", "/codex:setup") +
            '<p>Revisa si tienes Codex instalado; si no, te ofrece instalarlo (necesita Node.js: si no lo tienes, pídele a Claude «instala Node.js» y acepta). Cuando te lo pida, <b>inicia sesión con tu cuenta de ChatGPT</b>.</p></section>'
            '<section class="block"><h2>3 · Pásale trabajo</h2>' + code("c4", "En Claude Code", "/codex:rescue Arma el proyecto del reel siguiendo el brief de BRIEF.md") +
            '<p>Con <b>/codex:rescue</b> Claude le pasa la tarea a Codex y te trae el resultado. También tienes <b>/codex:review</b> para que Codex revise lo que hizo Claude.</p></section>'
            '<section class="block"><h2>4 · Que Claude delegue solo</h2><p>Pega esto en tu CLAUDE.md (¿no lo tienes? <a href="../memoria/">aquí está la plantilla</a>):</p>'
            + code("c5", "Añade a tu CLAUDE.md", CODEX_DELEGAR) +
            nota("Así trabajo: Claude decide, escribe el brief y revisa; Codex construye. Es como tener dos editores, uno dirige y el otro ejecuta. Cada uno gasta el límite de su propia cuenta.") + '</section>'
        ),
    ),
    dict(
        slug="memoria", palabra="MEMORIA", tipo="Plantilla", titulo="Plantilla de CLAUDE.md para editores",
        linea="El archivo que Claude lee al empezar cada sesión. Escribe una vez cómo editas y deja de repetirlo.",
        meta=["Plantilla", "Claude Code y Codex", "15 minutos", "Gratis"],
        amigo="ese amigo que le explica lo mismo a Claude todos los días",
        pasos=["Copia la plantilla.", "Guárdala como CLAUDE.md en la carpeta de tu proyecto y rellena los [corchetes].", "Cada vez que corrijas algo, dile: «guarda esto en CLAUDE.md»."],
        cuerpo=lambda: (
            '<section class="block"><h2>La plantilla</h2>' + code("m1", "CLAUDE.md", MEMORIA_TEMPLATE, scroll=True) + '</section>'
            '<section class="block"><h2>Por qué funciona</h2><ul>'
            '<li>Cada sesión de Claude empieza de cero. El CLAUDE.md es lo primero que lee, siempre.</li>'
            '<li>Cada corrección que guardas se convierte en una regla: no repites el mismo error dos veces.</li>'
            '<li><b>¿Usas Codex?</b> Guarda el mismo contenido como <b>AGENTS.md</b>: es el archivo que lee Codex.</li>'
            '</ul>' + nota("Mi sección favorita es «Nunca hacer». Ahí va cada error que ya corregí; con el tiempo es lo que hace que la IA edite como tú.") + '</section>'
        ),
    ),
]

PROXIMOS = [
    dict(palabra="SKILLS", titulo="Las 3 skills que instalo para editar", linea="Con su guía de instalación paso a paso.", fecha="25 nov"),
]


def estilo_cuerpo():
    reglas = [
        ("Regla 1 · El gancho en el primer segundo, con la mejor imagen", [
            "El primer cuadro ya es la imagen más fuerte del video. Nada de logos, intros ni «hola, ¿cómo están?».",
            "La primera frase se dice en el segundo 0, sin respirar antes.",
            "Hay un texto en pantalla de 5 palabras como máximo que se entiende sin sonido.",
            "El gancho promete algo que el video cumple.",
            "Prueba del pulgar: con el sonido apagado, ¿te quedarías después del primer segundo?",
        ]),
        ("Regla 2 · Algo nuevo cada segundo, nada quieto", [
            "Ningún plano dura más de 2–3 segundos sin un cambio: corte, zoom, texto, b-roll o gráfico.",
            "Las pausas dentro de una frase no pasan de 0,3 s.",
            "Zoom-in (de 100 % a 106–112 %) en las frases importantes, no en todas.",
            "Cada b-roll o gráfico aparece justo en la palabra que lo nombra.",
            "Cada efecto de sonido acompaña una acción en pantalla.",
            "La música va por debajo de la voz: la voz siempre se entiende.",
        ]),
        ("Regla 3 · Subtítulos que guían la mirada a la palabra clave", [
            "Frases cortas: de 2 a 4 palabras por bloque, al ritmo de la voz.",
            "Una sola fuente y un tamaño base; las palabras clave más grandes y en color (máximo 5 o 6 en todo el video).",
            "Los subtítulos no tapan la cara, la boca ni el producto, y quedan dentro de la zona segura.",
            "Sin punto final y sin errores de los subtítulos automáticos.",
            "Ningún texto repite el subtítulo en otra parte de la pantalla.",
        ]),
        ("Antes de exportar", [
            "El video termina justo después de la última palabra.",
            "Hay un solo llamado a la acción, claro.",
            "Exportas en 1080×1920 y 30 fps.",
        ]),
    ]
    html = ""
    n = 0
    for titulo, items in reglas:
        lis = ""
        for it in items:
            n += 1
            lis += f'<li><label><input type="checkbox" id="e{n}"><span>{escape(it)}</span></label></li>'
        html += f'<section class="block"><h2>{escape(titulo)}</h2><ul class="check" data-key="estilo">{lis}</ul></section>'
    html += '<section class="block">' + nota("Estas tres reglas no son un efecto mágico: son las mismas en cada video que edito. Lo que cambia es cómo las aplicas a cada material. Tus marcas se guardan en este navegador.") + '</section>'
    return html


# ---------------------------------------------------------------- páginas

def pagina_recurso(r):
    pasos = "".join(f"<li>{escape(p)}</li>" for p in r["pasos"])
    meta = "".join(f"<span>{escape(m)}</span>" for m in r["meta"])
    titulo = f'{r["titulo"]} · Bóveda Alfredits'
    html = head(titulo, r["linea"], f'comunidad/{r["slug"]}/', 1) + "\n<body>\n" + barra(1) + f"""
<main class="wrap wrap--narrow">
  <p class="crumb"><a href="../">← Bóveda de la comunidad</a></p>
  <section class="res-head">
    <span class="kw">Palabra clave <b>{r["palabra"]}</b></span>
    <h1>{escape(r["titulo"])}</h1>
    <p>{escape(r["linea"])}</p>
    <div class="meta">{meta}</div>
  </section>
  <section class="block"><h2>Cómo usarlo</h2><ol class="how">{pasos}</ol></section>
  {r["cuerpo"]()}
  {cierre(r["slug"], r["amigo"])}
</main>
""" + pie(1)
    d = OUT / r["slug"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(html, encoding="utf-8")


GUIA_PASOS = [
    ("app", "Descarga la app de Claude", """
<p>Baja la <b>app de escritorio de Claude</b> desde <a href="https://claude.ai/download" rel="noopener">claude.ai/download</a> (Mac o Windows) e inicia sesión.</p>
<ul><li>Necesitas el <b>plan Pro de Claude ($20 al mes)</b>: Claude Code no viene en el plan gratis.</li>
<li>Claude Code vive en la pestaña <b>Code</b> de la app, no en el navegador.</li>
<li>Funciona en computadora (Mac o Windows 10/11). En el celular no.</li></ul>"""),
    ("carpeta", "Crea tu carpeta de edición", """
<p>Crea una carpeta llamada <b>Editor IA</b> y, dentro, tres carpetas:</p>
<ul><li><b>Brutos</b>: lo que grabas.</li><li><b>Referencias</b>: videos que te inspiran.</li><li><b>Exportados</b>: lo terminado.</li></ul>
<div data-os-show="mac"><p>En el Finder, entra en Documentos y crea cada carpeta con <b>Cmd + Shift + N</b>.</p></div>
<div data-os-show="win"><p>En el Explorador de archivos, entra en Documentos y crea cada carpeta con <b>Ctrl + Shift + N</b>.</p></div>"""),
    ("abrir", "Abre la carpeta en Claude Code", """
<p>En la pestaña Code, abre una <b>sesión nueva</b>, elige <b>Local</b> y selecciona tu carpeta <b>Editor IA</b>. Ahora Claude puede ver y crear archivos ahí.</p>
<p>Antes de instalar o cambiar algo te pide permiso: lee lo que te pide y acepta.</p>
<div data-os-show="win"><p>Si en Windows te pide Git, instala <a href="https://git-scm.com/downloads/win" rel="noopener">Git para Windows</a> (siguiente, siguiente, finalizar) y vuelve a abrir la app.</p></div>"""),
    ("herramientas", "Dale herramientas", """
<p>Son programas gratis: <b>FFmpeg</b> corta y exporta, y <b>Whisper</b> transcribe cada palabra con su tiempo. No los instalas tú: pega esto y Claude lo hace.</p>
""" + code("g1", "Escríbele a Claude", "Instala en mi computadora FFmpeg, Python y el paquete faster-whisper. Verifica que cada uno funcione y avísame cuando esté listo. Pídeme permiso antes de cada instalación.") + """
<p>Tarda unos minutos. Si algo falla, copia el error y pégaselo a Claude.</p>"""),
    ("estilo", "Enséñale tu estilo", """
<p>Claude lee siempre un archivo llamado <b>CLAUDE.md</b> al empezar. Ahí van tus reglas de edición, para no repetirlas cada vez.</p>
""" + code("g2", "Escríbele a Claude", "Crea un archivo CLAUDE.md en esta carpeta con mi forma de editar: videos verticales 1080×1920 a 30 fps, gancho en el primer segundo, sin silencios de más de 0,3 s, subtítulos en bloques cortos con la palabra clave destacada, nunca encima de la cara, y cada versión nueva en Exportados sin borrar la anterior. Léelo antes de cada tarea.") + """
<p>¿Quieres una plantilla completa? Usa la de <a href="../memoria/">MEMORIA</a>.</p>"""),
    ("codex", "Conecta Codex para ahorrar límite", """
<p>Opcional, pero es lo que yo hago. Codex es el agente de ChatGPT y <b>sirve tu cuenta de ChatGPT, incluso la gratis</b>. Lo conectas a Claude Code con su plugin oficial y Claude le pasa el código pesado; así gastas menos límite de Claude.</p>
<p>Los comandos están en la guía <a href="../codex/">CODEX</a>: son 3 y se pegan en 5 minutos.</p>"""),
    ("pedir", "Graba, pídeselo y termina en CapCut", """
<p>Graba con tu celular, como siempre, y deja el archivo en <b>Brutos</b>. Luego pídele:</p>
""" + code("g3", "Escríbele a Claude", "Toma el video que dejé en Brutos: transcríbelo con Whisper, quita los silencios y los errores, ponle subtítulos siguiendo CLAUDE.md y expórtalo en Exportados como v1.") + """
<p>Si algo no te convence, díselo con tus palabras: «el gancho más grande», «menos pausa al final». Cuando esté bien, llévalo a <b>CapCut</b> para la música, los efectos y tu toque final. La IA hace lo pesado; el criterio lo pones tú.</p>"""),
]

GUIA_FAQ = [
    ("No me aparece la pestaña Code", "Actualiza la app de Claude y revisa que tu cuenta tenga el plan Pro o superior. El plan gratis no incluye Claude Code."),
    ("Claude no ve mi carpeta", "Abre una sesión nueva, elige Local y selecciona otra vez la carpeta Editor IA (la de arriba, no una de las de adentro)."),
    ("Se me acaba el límite", "Conecta Codex (paso 6): Claude le pasa el código pesado y gasta menos. Y pide cambios en una sola tanda, no uno por uno."),
    ("Una herramienta no se instala", "Pídele a Claude: «revisa por qué no se instaló y arréglalo». Si sigue fallando, copia el error completo y pégaselo."),
    ("El video no se exporta", "Casi siempre falta FFmpeg. Pídele a Claude que lo revise y lo instale de nuevo."),
]


# Cuando el video esté en YouTube, pon aquí su ID (lo que va después de watch?v=) y vuelve a generar.
YOUTUBE_ID = ""


def video_html():
    if YOUTUBE_ID:
        return (f'<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{YOUTUBE_ID}?rel=0" '
                'title="Tu primer video con Claude + Codex" loading="lazy" allow="accelerometer; encrypted-media; '
                'gyroscope; picture-in-picture; fullscreen" allowfullscreen></iframe></div>')
    return ('<div class="video video--soon"><div><span class="tc">16:9 · voz en off + motion</span>'
            '<b>El video explicativo llega pronto</b><span>Mientras tanto, la guía escrita ya funciona completa.</span></div></div>')


def pagina_guia():
    pasos = ""
    for i, (sid, titulo, cuerpo) in enumerate(GUIA_PASOS, 1):
        pasos += f"""<section class="step" id="paso-{i}" data-step="{sid}">
  <div class="step__head"><span class="step__num">{i:02d}</span><h2>{escape(titulo)}</h2></div>
  {cuerpo}
  <button class="btn btn--ghost done-btn" type="button">Listo, siguiente paso</button>
</section>"""
    faq = "".join(f"<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>" for q, a in GUIA_FAQ)
    n = len(GUIA_PASOS)
    desc = "Guía gratis: edita tu primer video con Claude Code (plan Pro) y Codex, y termínalo en CapCut. Paso a paso, en Mac y Windows."
    html = head("Tu primer video con Claude + Codex · Bóveda Alfredits", desc, "comunidad/guia/", 1) + '\n<body data-guide="primer-video">\n' + barra(1) + f"""
<main class="wrap wrap--narrow">
  <p class="crumb"><a href="../">← Bóveda de la comunidad</a></p>
  <section class="res-head">
    <span class="kw">Palabra clave <b>GUIA</b></span>
    <h1>Tu primer video con Claude + Codex</h1>
    <p>En {n} pasos instalas Claude Code, le enseñas tu estilo, le conectas Codex para ahorrar límite y le pides tu primer video con palabras. Después lo terminas en CapCut.</p>
    <div class="meta"><span>{n} pasos</span><span>30 minutos</span><span>Mac y Windows</span><span>Claude Pro ($20/mes)</span></div>
    <div class="btns"><a class="btn" href="#video">Ver el video</a><a class="btn btn--ghost" href="#paso-1">Empezar la guía ↓</a></div>
  </section>
  <section class="block" id="video">
    <h2>Mírala en video</h2>
    <p>Todo el proceso de principio a fin, en unos 2 minutos. Después sigue los pasos de abajo a tu ritmo.</p>
    {video_html()}
  </section>
  <section class="block" id="pasos">
    <h2>Hazlo conmigo</h2>
    <p>Elige tu sistema una vez y la guía se adapta. Marca cada paso al terminarlo: tu avance se guarda en este navegador.</p>
    <div class="os" role="group" aria-label="Sistema"><button type="button" data-os="mac" aria-pressed="false">Mac</button><button type="button" data-os="win" aria-pressed="false">Windows</button></div>
    <div class="progress"><div class="progress__bar"><i></i></div><span class="progress__txt"><b>0</b> de {n} pasos</span></div>
  </section>
  {pasos}
  <section class="block"><h2>¿Algo falló?</h2>{faq}
  {nota("Así empecé yo: Claude para el criterio y Codex para el código pesado. La guía es gratis; lo único que pagas es el plan Pro de Claude.")}</section>
  <section class="cta" id="siguiente">
    <span class="tc">siguiente nivel · próximamente</span>
    <h2>Esto es solo el comienzo: crea tu propio estilo de edición con IA</h2>
    <p>Con esta guía sacas tu primer video. En el ebook te enseño a montar tu flujo completo desde cero, especializado en edición: tus reglas, tus skills y tus prompts para que Claude y Codex editen como tú.</p>
    <div class="price">$15<small>precio de lanzamiento</small></div>
    <div class="btns"><a class="btn" href="{IG}" rel="noopener">Avísame cuando salga</a><a class="btn btn--ghost" href="../#ebook">Ver qué incluye</a></div>
  </section>
  {cierre("guia", "ese amigo que quiere empezar a editar con IA")}
</main>
""" + pie(1)
    d = OUT / "guia"
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(html, encoding="utf-8")


def pagina_hub():
    cards = ""
    for i, r in enumerate(RECURSOS):
        cards += f"""<a class="card" href="{r['slug']}/">
  <div class="card__top"><span class="label">{r['tipo']}</span><span class="tc">{r['palabra']}</span></div>
  <h3>{escape(r['titulo'])}</h3>
  <p>{escape(r['linea'])}</p>
  <div class="card__go"><span>Abrir</span><span>→</span></div>
</a>"""
    for p in PROXIMOS:
        cards += f"""<div class="card card--soon">
  <div class="card__top"><span class="label">Llega el {p['fecha']}</span><span class="tc">{p['palabra']}</span></div>
  <h3>{escape(p['titulo'])}</h3>
  <p>{escape(p['linea'])}</p>
  <div class="card__go"><span>Próximamente</span><span></span></div>
</div>"""
    n_guia = len(GUIA_PASOS)
    desc = "Recursos gratis para editar video con IA: prompts, scripts, plantillas y guías de Alfredo (@alfredits.ia). Sin registro."
    html = head("Bóveda de la comunidad · Alfredits", desc, "comunidad/", 0) + "\n<body>\n" + barra(0) + f"""
<main class="wrap">
  <section class="hero">
    <div class="who"><img src="assets/alfredo.webp" alt="Alfredo Navea" width="64" height="64"><div><div class="who__name">Alfredo Navea</div><div class="who__handle">Editor de video · @alfredits.ia</div></div></div>
    <h1>La Bóveda de la <em>comunidad</em></h1>
    <p class="hero__lead">Los prompts, scripts y guías que uso para editar con IA. Gratis y sin registro: copias, pegas y editas.</p>
    <nav class="hero__nav" aria-label="En esta página">
      <a class="pill" href="#guia">Guía</a><a class="pill" href="#gratis">Material gratis</a><a class="pill" href="#banco">Banco de recursos</a><a class="pill" href="#trabajos">Mis trabajos</a><a class="pill" href="#ebook">Ebook</a>
    </nav>
  </section>

  <section class="sec" id="guia">
    <div class="sec__head"><span class="tc">00:00:01 · empieza aquí</span></div>
    <a class="feature" href="guia/">
      <div class="feature__txt">
        <span class="kw">Palabra clave <b>GUIA</b></span>
        <h3>Tu primer video con Claude + Codex</h3>
        <p>Claude Code corta, transcribe y subtitula; Codex le ayuda con el código pesado. Tú lo terminas en CapCut. Paso a paso, en Mac o Windows.</p>
        <span class="btn" style="justify-self:start">Empezar la guía</span>
      </div>
      <div class="stats">
        <div class="stat"><b>{n_guia}</b><span>pasos</span></div>
        <div class="stat"><b>30</b><span>minutos</span></div>
        <div class="stat"><b>$20</b><span>Claude Pro al mes</span></div>
        <div class="stat"><b>Mac · Win</b><span>sistemas</span></div>
      </div>
    </a>
  </section>

  <section class="sec" id="gratis">
    <div class="sec__head">
      <span class="tc">00:00:08 · material gratis</span>
      <h2>Prompts, scripts y plantillas</h2>
      <p>Cada recurso tiene su palabra clave: si la comentaste en un reel, aquí está. Todos se usan igual: copias, pegas en Claude o ChatGPT y listo.</p>
    </div>
    <div class="grid">{cards}</div>
  </section>

  <section class="sec" id="banco">
    <div class="sec__head">
      <span class="tc">00:00:21 · banco de recursos</span>
      <h2>Animaciones editables, por estilo</h2>
      <p>Un banco de animaciones que uso en mis reels: con su video de muestra, el proyecto editable y el prompt para adaptarlas a tu marca. Lo estoy armando: sígueme para saber cuándo abre.</p>
    </div>
    <div class="btns"><a class="btn btn--ghost" href="{IG}" rel="noopener">Avísame en Instagram</a></div>
  </section>

  <section class="sec" id="trabajos">
    <div class="duo">
      <div class="panel">
        <span class="tc">00:00:34 · mis trabajos</span>
        <h3>Lo que edito</h3>
        <p>Reels para clientes de Estados Unidos y Latinoamérica, en español e inglés. Más de 1.000 videos en 2 años.</p>
        <div class="btns"><a class="btn btn--ghost" href="../">Ver mi web y portafolio</a></div>
      </div>
      <div class="panel" id="ebook">
        <span class="tc">00:00:47 · próximamente</span>
        <h3>Ebook: crea tu estilo de edición con IA</h3>
        <p>Paso a paso para montar tu propio flujo con Claude + Codex desde cero: tus reglas, tus skills y tus prompts, especializado en edición de video.</p>
        <div class="price">$15<small>precio de lanzamiento</small></div>
        <div class="btns"><a class="btn" href="{IG}" rel="noopener">Quiero que me avises</a></div>
      </div>
    </div>
  </section>
</main>
""" + pie(0)
    (OUT / "index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for r in RECURSOS:
        pagina_recurso(r)
    pagina_guia()
    pagina_hub()
    print("Bóveda generada:", ", ".join(["comunidad/"] + [f"comunidad/{r['slug']}/" for r in RECURSOS] + ["comunidad/guia/"]))
