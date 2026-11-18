# -*- coding: utf-8 -*-
import os, json, shutil, html
from datetime import date
from content import ARTICLES, FAQ_HOME, SOURCES, UPDATED, COUNTRIES

DOMAIN = os.environ.get("DOMAIN", "berespa.com")
BASE = f"https://{DOMAIN}"
SITE = "Guía GTA 6"
TAG = "Guía de GTA 6 en español"
ADSENSE = os.environ.get("ADSENSE_CLIENT", "ca-pub-4678189251158514")  # ej. ca-pub-1234567890123456
OUT = "dist"
RELEASE_ISO = "2026-11-19T00:00:00+01:00"

MONTHS = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
def fecha(iso):
    y,m,d = map(int, iso.split("-")); return f"{d} de {MONTHS[m-1]} de {y}"

NAV = [("/","Inicio"),("/hora-lanzamiento-gta-6-por-paises/","Hora por países"),("/precio-gta-6-ediciones/","Precio"),
       ("/personajes-gta-6/","Personajes"),("/mapa-gta-6-leonida/","Mapa"),("/noticias/","Noticias")]

def esc(s): return html.escape(s, quote=True)

def head(title, desc, path, og_type="website", jsonld=None):
    url = BASE + path
    ld = "".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in (jsonld or []))
    ads = (f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE}" crossorigin="anonymous"></script>'
           if ADSENSE else "")
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<link rel="alternate" hreflang="es" href="{url}"><link rel="alternate" hreflang="x-default" href="{url}">
<meta name="theme-color" content="#0d0a14">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:locale" content="es_ES"><meta property="og:locale:alternate" content="es_MX"><meta property="og:locale:alternate" content="es_AR"><meta property="og:locale:alternate" content="es_CO">
<meta property="og:site_name" content="{SITE}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/og.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/style.css">
{ld}{ads}
</head>
<body>
<a class="skip" href="#main">Saltar al contenido</a>
<header class="top"><div class="wrap">
<a class="logo" href="/" aria-label="Inicio"><span class="dot"></span><span>GUÍA <b>GTA 6</b></span></a>
<button class="menu-btn" aria-expanded="false" aria-controls="nav" onclick="var n=document.getElementById('nav');n.classList.toggle('open');this.setAttribute('aria-expanded',n.classList.contains('open'))">Menú</button>
<nav id="nav"><ul>{"".join(f'<li><a href="{h}"{" aria-current=page" if h==path else ""}>{t}</a></li>' for h,t in NAV)}</ul></nav>
</div></header>
<main id="main">
"""

def foot():
    year = date.today().year
    return f"""</main>
<footer><div class="wrap">
<div class="cols">
<div><a class="logo" href="/"><span class="dot"></span><span>GUÍA <b>GTA 6</b></span></a>
<p>{TAG}: fecha, precio, personajes, mapa y todas las novedades de Grand Theft Auto VI, explicado claro y sin rodeos.</p></div>
<div><h5>Guías</h5><ul>
<li><a href="/fecha-lanzamiento-gta-6/">Fecha y hora de lanzamiento</a></li>
<li><a href="/precio-gta-6-ediciones/">Precio y ediciones</a></li>
<li><a href="/tamano-descarga-precarga-gta-6/">Tamaño y precarga</a></li>
<li><a href="/gta-6-pc/">GTA 6 en PC</a></li>
<li><a href="/noticias/">Todas las noticias</a></li></ul></div>
<div><h5>Información</h5><ul>
<li><a href="/sobre-nosotros/">Sobre nosotros</a></li>
<li><a href="/contacto/">Contacto</a></li>
<li><a href="/aviso-legal/">Aviso legal</a></li>
<li><a href="/privacidad/">Política de privacidad</a></li>
<li><a href="/cookies/">Política de cookies</a></li></ul></div>
</div>
<p class="disc">© {year} {SITE}. Web de fans <strong>no oficial</strong>, sin relación con Rockstar Games ni Take-Two Interactive. Grand Theft Auto, GTA y Grand Theft Auto VI son marcas registradas de Take-Two Interactive Software, Inc. Todas las ilustraciones de esta web son originales.</p>
</div></footer>
</body></html>"""

def ad_slot():
    if not ADSENSE: return '<div class="ad"></div>'
    return (f'<div class="ad"><ins class="adsbygoogle" style="display:block" data-ad-client="{ADSENSE}" '
            'data-ad-format="auto" data-full-width-responsive="true"></ins>'
            '<script>(adsbygoogle=window.adsbygoogle||[]).push({});</script></div>')

def faq_html(faq):
    return '<section class="faq"><h2>Preguntas frecuentes</h2>' + "".join(
        f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q,a in faq) + "</section>"

def faq_ld(faq):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}

def crumbs_ld(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":i+1,"name":n,"item":BASE+p} for i,(n,p) in enumerate(items)]}

def card(a):
    return f"""<article class="card">
<a class="cover" href="/{a['slug']}/" aria-hidden="true" tabindex="-1"><div class="cov {a['cover']}">{esc(a['cover_txt'])}</div></a>
<div class="body"><span class="cat">{a['cat']}</span>
<h3><a href="/{a['slug']}/">{esc(a['title'])}</a></h3>
<p>{esc(a['desc'])}</p><time datetime="{UPDATED}">Actualizado el {fecha(UPDATED)}</time></div></article>"""


def country_table(limit=None):
    rows=[]
    for name,flag,off,note in (COUNTRIES[:limit] if limit else COUNTRIES):
        es = (24 + 1 - off) % 24   # hora peninsular (UTC+1) cuando allí son las 00:00 del 19
        day = "18 nov" if off > 1 else ("19 nov" if es < 24 else "")
        esh = f"{es:02d}:00 ({day})"
        n = f' <small style="color:var(--orange)">· {note}</small>' if note else ""
        rows.append(f'<tr><td>{flag} {esc(name)}{n}</td><td>00:00 del 19 nov</td><td>{esh}</td><td class="cc" data-off="{off}">–</td></tr>')
    return ('<div class="ctab"><table><thead><tr><th>País</th><th>Hora local</th><th>Hora en España</th><th>Falta</th></tr></thead><tbody>'
            + "".join(rows) + '</tbody></table></div>')

COUNTRY_JS = """<script>
(function(){var c=document.querySelectorAll('.cc');if(!c.length)return;var base=Date.UTC(2026,10,19,0,0,0);
function p(n){return n<10?'0'+n:n}
function t(){var now=Date.now();c.forEach(function(e){var s=Math.floor((base-(+e.dataset.off)*3600000-now)/1000);
if(s<=0){e.innerHTML='<b style="color:var(--teal)">¡Ya disponible!</b>';return}
var d=Math.floor(s/86400),h=Math.floor(s%86400/3600),m=Math.floor(s%3600/60);
e.textContent=(d?d+'d ':'')+p(h)+':'+p(m)+':'+p(s%60)});setTimeout(t,1000)}t()})();
</script>"""

def write(path, content):
    d = os.path.join(OUT, path.strip("/"))
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f: f.write(content)

PALMS = """<svg class="palms" viewBox="0 0 1440 220" preserveAspectRatio="none" aria-hidden="true"><g fill="#0d0a14">
<path d="M0 220V170c120-10 240 6 360-4s260-26 400-14 300 22 420 8 200-18 260-10v70z"/>
<path d="M190 175c4-50 8-95 22-140l6 2c-12 44-16 90-18 138z"/><path d="M215 40c-30-12-62-8-88 10 26-6 56-6 84 0zm0 0c22-26 54-36 86-30-30 4-58 16-80 34zm0 0c-14-28-40-44-70-46 26 10 48 28 62 52zm0 0c34-4 64 8 86 30-26-14-56-22-84-24zm0 0c-36 4-60 24-74 52 18-24 44-40 72-46z"/>
<path d="M1180 172c2-56 10-104 26-150l6 2c-14 46-20 94-22 148z"/><path d="M1209 26c-32-10-64-4-90 16 28-8 58-10 86-4zm0 0c20-28 52-40 86-36-32 6-60 20-82 40zm0 0c-12-30-38-48-70-52 28 12 50 32 64 56zm0 0c36-2 66 12 86 36-26-16-58-26-86-28zm0 0c-38 6-62 28-74 58 18-26 44-44 72-52z"/>
<path d="M1290 180c2-36 6-66 16-96l5 2c-9 30-12 60-13 94z"/><path d="M1308 86c-22-7-44-3-62 11 19-5 40-7 59-3zm0 0c14-19 36-27 59-25-22 4-41 14-56 28zm0 0c-8-21-26-33-48-36 19 8 34 22 44 39zm0 0c25-1 45 8 59 25-18-11-40-18-59-19z"/>
</g></svg>"""

def build():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    for f in os.listdir("static"): shutil.copy(os.path.join("static", f), OUT)

    # ---------- HOME ----------
    site_ld = {"@context":"https://schema.org","@type":"WebSite","name":SITE,"url":BASE+"/","inLanguage":"es-ES",
               "description":"Guía de GTA 6 en español: fecha, precio, personajes, mapa y noticias."}
    org_ld = {"@context":"https://schema.org","@type":"Organization","name":SITE,"url":BASE+"/","logo":BASE+"/apple-touch-icon.png"}
    game_ld = {"@context":"https://schema.org","@type":"VideoGame","name":"Grand Theft Auto VI","alternateName":"GTA 6",
               "author":{"@type":"Organization","name":"Rockstar Games"},"publisher":{"@type":"Organization","name":"Rockstar Games"},
               "gamePlatform":["PlayStation 5","Xbox Series X|S"],"genre":["Acción","Mundo abierto"],"datePublished":"2026-11-19",
               "contentRating":"PEGI 18","url":"https://www.rockstargames.com/VI",
               "offers":[{"@type":"Offer","name":"Standard Edition","price":"79.99","priceCurrency":"EUR"},
                         {"@type":"Offer","name":"Ultimate Edition","price":"99.99","priceCurrency":"EUR"}]}
    t = "GTA 6: fecha, hora en España, precio, personajes y mapa | Guía GTA 6"
    d = "Todo sobre GTA 6 en español: sale el 19 de noviembre de 2026 a las 00:00 en España. Precio (79,99 €), ediciones, tamaño (212 GB), personajes, mapa de Leonida, PC y online."
    h = head(t, d, "/", jsonld=[site_ld, org_ld, game_ld, faq_ld(FAQ_HOME)])
    h += f"""<section class="hero"><div class="sun"></div>{PALMS}<div class="wrap">
<span class="kicker">Actualizado {fecha(UPDATED)}</span>
<h1>Todo sobre <span>GTA 6</span>, explicado en español</h1>
<p class="lead">Grand Theft Auto VI sale el <strong>jueves 19 de noviembre de 2026</strong> en PS5 y Xbox Series X|S. En España se desbloquea a las <strong>00:00</strong>.</p>
<div class="countdown" id="cd" aria-live="polite">
<div><b id="cd-d">–</b><small>días</small></div><div><b id="cd-h">–</b><small>horas</small></div>
<div><b id="cd-m">–</b><small>min</small></div><div><b id="cd-s">–</b><small>seg</small></div></div>
<a class="btn" href="/fecha-lanzamiento-gta-6/">Hora exacta de lanzamiento</a><a class="btn ghost" href="/precio-gta-6-ediciones/">Precio y ediciones</a>
</div></section>
<div class="wrap"><div class="facts">
<div class="fact"><small>Lanzamiento</small><strong>19 nov 2026 · 00:00</strong></div>
<div class="fact"><small>Plataformas</small><strong>PS5 · Xbox Series X|S</strong></div>
<div class="fact"><small>Precio</small><strong>79,99 € / 99,99 €</strong></div>
<div class="fact"><small>Tamaño</small><strong>Hasta 212 GB</strong></div>
<div class="fact"><small>Edad</small><strong>PEGI 18</strong></div>
</div></div>
<section class="block"><div class="wrap">
<h2 class="sec">Cuenta atrás de GTA 6 por países</h2><p class="sub">GTA 6 se desbloquea a las 00:00 hora local de cada país. <a href="/hora-lanzamiento-gta-6-por-paises/">Ver todos los países y detalles →</a></p>
<div class="prose">{country_table()}</div>
</div></section>
<section class="block" style="padding-top:0"><div class="wrap">
<h2 class="sec">Guías y noticias de GTA 6</h2><p class="sub">Información contrastada y actualizada, sin rumores disfrazados de noticias.</p>
<div class="grid">{"".join(card(a) for a in ARTICLES)}</div>
{ad_slot()}
</div></section>
<section class="block" style="padding-top:0"><div class="wrap prose" style="max-width:820px">
<h2 class="sec">GTA 6 en 30 segundos</h2>
<p><strong>Grand Theft Auto VI</strong> es la nueva entrega de la saga de Rockstar Games, la primera en 13 años desde GTA V. La historia sigue a <a href="/personajes-gta-6/">Jason Duval y Lucia Caminos</a>, una pareja criminal en el estado de <a href="/mapa-gta-6-leonida/">Leonida</a>, inspirado en Florida, con Vice City como gran ciudad. Lucia es la primera protagonista femenina jugable de un GTA principal.</p>
<p>Sale el 19 de noviembre de 2026 solo en consolas actuales; <a href="/gta-6-pc/">no hay versión de PC anunciada</a>. Es una experiencia para un jugador y <a href="/gta-6-online-multijugador/">no tiene modo online anunciado</a>. Cuesta <a href="/precio-gta-6-ediciones/">79,99 € (Standard) o 99,99 € (Ultimate)</a> y ocupa <a href="/tamano-descarga-precarga-gta-6/">hasta 212 GB</a>.</p>
{faq_html(FAQ_HOME)}
</div></section>
<script>
(function(){{var t=new Date("{RELEASE_ISO}").getTime(),el=document.getElementById("cd");
function p(n){{return n<10?"0"+n:n}}
function tick(){{var s=Math.floor((t-Date.now())/1000);
if(s<=0){{el.innerHTML='<span class="live">¡GTA 6 ya está disponible en España!</span>';return}}
document.getElementById("cd-d").textContent=Math.floor(s/86400);
document.getElementById("cd-h").textContent=p(Math.floor(s%86400/3600));
document.getElementById("cd-m").textContent=p(Math.floor(s%3600/60));
document.getElementById("cd-s").textContent=p(s%60);setTimeout(tick,1000)}}tick()}})();
</script>
{COUNTRY_JS}
"""
    write("/", h + foot())

    # ---------- ARTICLES ----------
    for a in ARTICLES:
        path = f"/{a['slug']}/"
        art_ld = {"@context":"https://schema.org","@type":"Article","headline":a["title"],"description":a["desc"],
                  "inLanguage":"es-ES","datePublished":UPDATED,"dateModified":UPDATED,"mainEntityOfPage":BASE+path,
                  "image":BASE+"/og.png","author":{"@type":"Organization","name":SITE,"url":BASE+"/sobre-nosotros/"},
                  "publisher":{"@type":"Organization","name":SITE,"logo":{"@type":"ImageObject","url":BASE+"/apple-touch-icon.png"}}}
        bc = [("Inicio","/"),("Noticias","/noticias/"),(a["title"],path)]
        related = [r for r in ARTICLES if r["slug"] != a["slug"]][:6]
        h = head(a["seo_title"], a["desc"], path, "article", [art_ld, crumbs_ld(bc), faq_ld(a["faq"])])
        h += f"""<div class="wrap">
<div class="crumbs"><a href="/">Inicio</a> › <a href="/noticias/">Noticias</a> › {esc(a['cat'])}</div>
<div class="art"><article>
<header><span class="kicker">{a['cat']}</span><h1>{esc(a['title'])}</h1>
<div class="meta">Por la redacción de {SITE} · Actualizado el <time datetime="{UPDATED}">{fecha(UPDATED)}</time></div></header>
<div class="tldr"><strong>En resumen:</strong> {a['tldr']}</div>
{ad_slot()}
<div class="prose">{a['body'].replace('{{COUNTRY_TABLE}}', country_table())}
{ad_slot()}
{faq_html(a['faq'])}
<p class="note">Fuentes: {" · ".join(f'<a href="{u}" rel="nofollow noopener" target="_blank">{esc(n)}</a>' for n,u in SOURCES)}. Datos comprobados el {fecha(UPDATED)}; actualizamos este artículo cuando hay novedades oficiales.</p>
</div></article>
<aside><div class="box"><h4>Más sobre GTA 6</h4><ul>
{"".join(f'<li><a href="/{r["slug"]}/">{esc(r["title"])}</a></li>' for r in related)}
</ul></div></aside>
</div></div>{COUNTRY_JS if '{{COUNTRY_TABLE}}' in a['body'] else ''}"""
        write(path, h + foot())

    # ---------- NOTICIAS ----------
    path = "/noticias/"
    h = head("Noticias y guías de GTA 6 en español | Guía GTA 6",
             "Todas las noticias y guías de GTA 6: lanzamiento, precio, precarga, personajes, mapa, PC, online, banda sonora y más.",
             path, jsonld=[crumbs_ld([("Inicio","/"),("Noticias",path)])])
    h += f"""<section class="block"><div class="wrap">
<div class="crumbs" style="padding:0 0 10px"><a href="/">Inicio</a> › Noticias</div>
<h1 class="sec" style="font-size:2.4rem;margin:0 0 6px">Noticias y guías de GTA 6</h1>
<p class="sub">Todo lo que necesitas saber sobre Grand Theft Auto VI, ordenado por temas.</p>
<div class="grid">{"".join(card(a) for a in ARTICLES)}</div></div></section>"""
    write(path, h + foot())

    # ---------- PÁGINAS LEGALES / INFO ----------
    def page(path, title, desc, body, index=True):
        hh = head(f"{title} | {SITE}", desc, path)
        if not index: hh = hh.replace('content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"', 'content="noindex,follow"')
        hh += f'<div class="wrap" style="max-width:820px;padding:30px 20px 60px"><h1 style="font-size:2.2rem">{title}</h1><div class="prose">{body}</div></div>'
        write(path, hh + foot())

    page("/sobre-nosotros/", "Sobre nosotros", f"Qué es {SITE} y cómo elaboramos nuestras guías de GTA 6.", f"""
<p><strong>{SITE}</strong> es una web independiente hecha por fans de Grand Theft Auto para el público hispanohablante. Nuestro objetivo es simple: explicar todo lo importante sobre GTA 6 de forma clara, en español y sin titulares engañosos.</p>
<h2>Cómo trabajamos</h2>
<ul><li>Partimos de la información oficial de Rockstar Games, Take-Two y las tiendas de PlayStation y Xbox.</li>
<li>Contrastamos los datos con medios especializados de referencia y citamos las fuentes en cada artículo.</li>
<li>Distinguimos siempre entre lo <strong>confirmado</strong> y lo que son <strong>rumores o estimaciones</strong>.</li>
<li>Cada artículo indica su fecha de última actualización y lo revisamos cuando hay novedades.</li></ul>
<h2>Independencia</h2>
<p>No tenemos ninguna relación con Rockstar Games ni con Take-Two Interactive. La web se financia con publicidad, que nunca influye en el contenido.</p>
<p>¿Has visto un error? <a href="/contacto/">Escríbenos</a> y lo corregimos.</p>""")

    page("/contacto/", "Contacto", f"Cómo contactar con {SITE}.", """
<p>Para correcciones, sugerencias o cualquier consulta, escríbenos a:</p>
<p style="font-size:1.2rem"><strong>[EMAIL DE CONTACTO]</strong></p>
<p>Respondemos normalmente en 48-72 horas laborables.</p>""")

    page("/aviso-legal/", "Aviso legal", "Aviso legal e información del titular del sitio web.", f"""
<p>En cumplimiento de la Ley 34/2002, de Servicios de la Sociedad de la Información y de Comercio Electrónico (LSSI-CE), se informa de los datos del titular de este sitio web:</p>
<ul><li><strong>Titular:</strong> [NOMBRE Y APELLIDOS]</li><li><strong>NIF:</strong> [NIF]</li>
<li><strong>Domicilio:</strong> [DIRECCIÓN]</li><li><strong>Email:</strong> [EMAIL DE CONTACTO]</li><li><strong>Sitio web:</strong> {DOMAIN}</li></ul>
<h2>Objeto</h2><p>{SITE} es una web informativa sobre videojuegos, en particular sobre Grand Theft Auto VI. Es una web de fans no oficial.</p>
<h2>Propiedad intelectual e industrial</h2><p>Los textos e ilustraciones de esta web son originales. Grand Theft Auto, GTA, Grand Theft Auto VI, Rockstar Games y sus logotipos son marcas de Take-Two Interactive Software, Inc., y se mencionan con fines exclusivamente informativos. Esta web no está patrocinada ni respaldada por ellos.</p>
<h2>Responsabilidad</h2><p>El titular procura que la información sea exacta y esté actualizada, pero no garantiza la ausencia de errores ni se responsabiliza de los contenidos de webs enlazadas.</p>
<h2>Legislación aplicable</h2><p>Este aviso se rige por la legislación española.</p>""", index=False)

    page("/privacidad/", "Política de privacidad", "Cómo tratamos tus datos personales.", f"""
<p>Última actualización: {fecha(UPDATED)}.</p>
<h2>Responsable del tratamiento</h2><p>[NOMBRE Y APELLIDOS], NIF [NIF], email [EMAIL DE CONTACTO].</p>
<h2>Qué datos tratamos</h2>
<ul><li><strong>Si nos escribes por email:</strong> tu dirección y el contenido del mensaje, solo para responderte (base legal: tu consentimiento y nuestro interés legítimo en atender consultas).</li>
<li><strong>Publicidad:</strong> esta web puede mostrar anuncios de Google AdSense. Google y sus socios pueden usar cookies e identificadores para mostrar anuncios, personalizados o no, según el consentimiento que des en el aviso de cookies. Más información en <a href="https://policies.google.com/technologies/ads?hl=es" rel="nofollow noopener" target="_blank">cómo usa Google las cookies en publicidad</a>.</li>
<li><strong>Registros técnicos:</strong> el proveedor de alojamiento puede registrar datos técnicos (como la IP) por seguridad.</li></ul>
<h2>Conservación</h2><p>Conservamos los datos el tiempo necesario para la finalidad para la que se recogieron.</p>
<h2>Tus derechos</h2><p>Puedes ejercer tus derechos de acceso, rectificación, supresión, oposición, limitación y portabilidad escribiendo a [EMAIL DE CONTACTO]. También puedes reclamar ante la Agencia Española de Protección de Datos (aepd.es).</p>
<h2>Transferencias internacionales</h2><p>Algunos proveedores (alojamiento, Google) pueden tratar datos fuera del Espacio Económico Europeo, con las garantías previstas en el RGPD.</p>""", index=False)

    page("/cookies/", "Política de cookies", "Información sobre las cookies que utiliza esta web.", f"""
<p>Última actualización: {fecha(UPDATED)}.</p>
<h2>¿Qué son las cookies?</h2><p>Pequeños archivos que los sitios web guardan en tu navegador para recordar información sobre tu visita.</p>
<h2>Cookies que usamos</h2>
<ul><li><strong>Técnicas:</strong> esta web no necesita cookies propias para funcionar.</li>
<li><strong>Publicidad (Google AdSense):</strong> si se muestran anuncios, Google puede instalar cookies para servir, medir y, si lo aceptas, personalizar anuncios. Solo se usan con tu consentimiento, que se gestiona mediante el aviso de consentimiento de Google que aparece al entrar.</li></ul>
<h2>Cómo cambiar tu elección</h2><p>Puedes cambiar tu consentimiento desde el enlace de preferencias de privacidad del aviso, o borrar y bloquear las cookies desde la configuración de tu navegador.</p>""", index=False)

    # 404
    hh = head(f"Página no encontrada | {SITE}", "Esta página no existe.", "/404/").replace('content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"','content="noindex"')
    hh += '<div class="wrap" style="padding:80px 20px;text-align:center"><h1 style="font-size:3rem">404</h1><p>Esta página se ha perdido por Leonida.</p><a class="btn" href="/">Volver al inicio</a></div>'
    with open(os.path.join(OUT,"404.html"),"w",encoding="utf-8") as f: f.write(hh+foot())

    # ---------- SEO FILES ----------
    urls = ["/","/noticias/"] + [f"/{a['slug']}/" for a in ARTICLES] + ["/sobre-nosotros/","/contacto/"]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        sm += f"<url><loc>{BASE}{u}</loc><lastmod>{UPDATED}</lastmod><changefreq>daily</changefreq><priority>{'1.0' if u=='/' else '0.8'}</priority></url>\n"
    sm += "</urlset>\n"
    open(os.path.join(OUT,"sitemap.xml"),"w").write(sm)
    open(os.path.join(OUT,"robots.txt"),"w").write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    pub = ADSENSE.replace("ca-","") if ADSENSE else ""
    open(os.path.join(OUT,"ads.txt"),"w").write(
        f"google.com, {pub}, DIRECT, f08c47fec0942fa0\n" if pub else "# Añade aquí tu línea de AdSense: google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0\n")
    json.dump({"cleanUrls":True,"trailingSlash":True,
               "headers":[{"source":"/(.*)\\.(css|svg|png)","headers":[{"key":"Cache-Control","value":"public, max-age=604800"}]}]},
              open(os.path.join(OUT,"vercel.json"),"w"))
    open(os.path.join(OUT,"32f75d6286d3068c29bb53b0dffd3d78.txt"),"w").write("32f75d6286d3068c29bb53b0dffd3d78")
    open(os.path.join(OUT,"CNAME"),"w").write(DOMAIN+"\n")
    open(os.path.join(OUT,".nojekyll"),"w").write("")
    print("OK", len(urls), "URLs")

if __name__ == "__main__":
    build()
