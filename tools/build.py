#!/usr/bin/env python3
"""Assemble les pages du site BATITECH (gabarit commun)."""
import os, sys
OUT = sys.argv[1]
ARTIFACT = len(sys.argv) > 2 and sys.argv[2] == 'artifact'
V = '4'  # cache-buster

MARK = '''<svg viewBox="0 0 30 34" aria-hidden="true"><path class="drop" d="M15 1C15 1 2 15.5 2 22.5a13 13 0 0 0 26 0C28 15.5 15 1 15 1Z" fill="#ffc21a"/><path class="bolt" d="M16.6 13 9.8 24.2h5.1l-1.6 7.2 7-11.4h-5.2l1.5-7Z" fill="#07090b"/></svg>'''
LOADER_MARK = '''<svg viewBox="0 0 30 34" aria-hidden="true"><path class="drop" d="M15 1C15 1 2 15.5 2 22.5a13 13 0 0 0 26 0C28 15.5 15 1 15 1Z"/><path class="bolt" d="M16.6 13 9.8 24.2h5.1l-1.6 7.2 7-11.4h-5.2l1.5-7Z"/></svg>'''
I_PHONE = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1Z"/></svg>'
I_WA = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3a.4.4 0 0 0 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7a2.8 2.8 0 0 0 1.8-1.3 2.3 2.3 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3Z"/></svg>'
I_ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6"/></svg>'

NAV = [('index.html','Accueil'),('plomberie.html','Plomberie'),('electricite.html','Électricité'),('forage.html','Forage'),('avant-apres.html','Avant / après'),('contact.html','Contact')]

def head(title, desc):
    return f'''<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,300..800&display=swap">
<link rel="icon" type="image/png" href="assets/img/brand/favicon.png">
<meta name="theme-color" content="#ffffff">
<link rel="stylesheet" href="assets/css/style.css?v={V}">
<script>try{{var d=document.documentElement;d.classList.add('js');if(sessionStorage.getItem('em-nav')){{d.classList.add('pt');sessionStorage.removeItem('em-nav')}}else if(!sessionStorage.getItem('em-seen')){{d.classList.add('first')}}}}catch(e){{}}setTimeout(function(){{document.documentElement.classList.remove('pt','first')}},10000)</script>'''

def header(cur):
    links = ''.join(f'<a href="{h}"{" aria-current=\"page\"" if h==cur else ""}>{t}</a>' for h,t in NAV[1:])
    mlinks = ''.join(f'<a href="{h}"{" aria-current=\"page\"" if h==cur else ""}>{t}</a>' for h,t in NAV)
    return f'''<div class="loader" aria-hidden="true"><div class="loader-in"><img class="mk" src="assets/img/brand/batitech-mark.png" alt=""><img class="wd" src="assets/img/brand/batitech-word.png" alt=""><div class="loader-bar"><i></i></div><div class="loader-pct">0 %</div></div></div>
<div class="curtain" aria-hidden="true"><img src="assets/img/brand/batitech-mark-white.png" alt=""></div>
<header class="top">
  <a class="logo" href="index.html" aria-label="BATITECH, accueil"><img class="mk" src="assets/img/brand/batitech-mark.png" alt="" width="422" height="419"><img class="wd color" src="assets/img/brand/batitech-word.png" alt="BATITECH" width="893" height="108"><img class="wd white" src="assets/img/brand/batitech-word-white.png" alt="BATITECH" width="893" height="108"></a>
  <nav class="nav" aria-label="Navigation principale">{links}</nav>
  <div class="top-actions">
    <a class="btn sm" data-tel href="#" data-magnetic>{I_PHONE}<span class="t">Appeler</span></a>
    <button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="menu"><i></i><i></i></button>
  </div>
  <i class="progress" aria-hidden="true"></i>
</header>
<div class="menu" id="menu"><nav aria-label="Menu mobile">{mlinks}</nav><div class="m-foot"><span>Urgence, devis, conseil</span><b data-phone></b><span data-address></span></div></div>'''

def cta(title='Une fuite, une panne,', lt='un projet de forage ?', text='Appelez ou écrivez sur WhatsApp. On vous répond, on se déplace, on vous fait un devis clair avant de commencer.'):
    return f'''<section class="wrap sec tight"><div class="inner"><div class="cta"><img class="ghost-mark" src="assets/img/brand/batitech-mark-white.png" alt="" aria-hidden="true">
  <div><h2 class="d2" data-split>{title}<span class="lt">{lt}</span></h2><p style="margin:18px 0 0;max-width:46ch">{text}</p></div>
  <div class="actions" style="margin:0"><a class="btn" data-tel href="#" data-magnetic>{I_PHONE}<span data-phone></span></a><a class="btn ghost" data-wa="Bonjour BATITECH, j'ai besoin d'un devis." href="#">{I_WA}WhatsApp</a></div>
</div></div></section>'''

def footer():
    links = ''.join(f'<li><a href="{h}">{t}</a></li>' for h,t in NAV)
    return f'''<footer class="wrap foot"><div class="inner">
  <div class="foot-grid">
    <div><a class="logo" href="index.html"><img class="mk" src="assets/img/brand/batitech-mark.png" alt="" width="422" height="419"><img class="wd color" src="assets/img/brand/batitech-word.png" alt="BATITECH" width="893" height="108"><img class="wd white" src="assets/img/brand/batitech-word-white.png" alt="BATITECH" width="893" height="108"></a>
      <p class="muted" style="max-width:34ch;margin:18px 0 0">Plomberie, électricité et forage de puits. Basés à Amadahomé, au service de Lomé et de ses environs.</p></div>
    <div><h4>Pages</h4><ul>{links}</ul></div>
    <div><h4>Nous joindre</h4><div class="phone" data-phone></div><p class="muted" style="margin:6px 0 14px" data-address></p>
      <a class="btn sm" data-wa="Bonjour BATITECH," href="#">{I_WA}WhatsApp</a></div>
  </div>
  <div class="giant" aria-hidden="true">Batitech</div>
  <div class="foot-bottom"><span>© <span data-year></span> BATITECH</span><span>Plomberie · Électricité · Forage — Lomé</span></div>
</div></footer>
<a class="wa-float" data-wa="Bonjour BATITECH," href="#" aria-label="Écrire sur WhatsApp">{I_WA}</a>
<script src="assets/js/config.js?v={V}"></script>
<script src="assets/js/main.js?v={V}"></script>'''

def film(seq, count, caps, steps, labels, focus='.5', zoom='1.06,1', remap=None, counter=None, hint=True, fid=None):
    capshtml = ''
    for i,(a,b,kick,h,lt,p,extra) in enumerate(caps):
        tag = 'h1' if (i==0 and fid=='hero') else 'h2'
        capshtml += f'''<div class="cap{' first' if i==0 else ''}" data-from="{a}" data-to="{b}">
  <p class="kicker">{kick}</p><{tag} class="d1" data-split>{h}<span class="lt">{lt}</span></{tag}>
  {f'<p class="lede">{p}</p>' if p else ''}{extra}
</div>'''
    tl = ''.join(f'<span{" class=\"on\"" if i==0 else ""}>{l}</span>' for i,l in enumerate(labels))
    cnt = f'<div class="counter" aria-hidden="true"><div class="n"><span data-counter>00</span><small>%</small></div><div class="l">{counter}</div></div>' if counter else ''
    rm = f' data-remap="{remap}"' if remap else ''
    return f'''<section class="film"{f' id="{fid}"' if fid else ''} data-seq="assets/frames/{seq}" data-count="{count}" data-focus="{focus}" data-zoom="{zoom}"{rm}>
<div class="stage"><canvas aria-hidden="true"></canvas><div class="scrim"></div>{cnt}
<div class="caps">{capshtml}</div>
{'<div class="scroll-hint" aria-hidden="true">Faites défiler<i></i></div>' if hint else ''}
<div class="tl" data-steps="{steps}" aria-hidden="true"><i class="fill"></i>{tl}</div>
</div></section>'''

def band(items):
    return '<div class="band" aria-hidden="true"><div class="band-track">' + ''.join(f'<span>{x}</span>' for x in items) + '</div></div>'

def actions_call():
    return f'<div class="actions"><a class="btn" data-tel href="#" data-magnetic>{I_PHONE}Appeler maintenant</a><a class="btn ghost" data-wa="Bonjour BATITECH, j\'ai besoin d\'une intervention." href="#">{I_WA}Écrire sur WhatsApp</a></div>'

def services(items):
    return '<div class="services">' + ''.join(f'<article class="service rv"><h3>{t}</h3><p>{d}</p></article>' for t,d in items) + '</div>'

def steps(items):
    return f'<div class="steps" style="--n:{len(items)}">' + ''.join(f'<div class="step rv"><div class="num">{i+1:02d}</div><h3>{t}</h3><p>{d}</p></div>' for i,(t,d) in enumerate(items)) + '</div>'

def faq(items):
    return '<div class="faq">' + ''.join(f'<details><summary>{q}<i aria-hidden="true"></i></summary><div class="a"><div><p>{a}</p></div></div></details>' for q,a in items) + '</div>'

def sec_head(kick, h, lt, lede):
    return f'<div class="sec-head"><div><p class="kicker">{kick}</p><h2 class="d2" data-split>{h}<span class="lt">{lt}</span></h2></div><p class="lede rv">{lede}</p></div>'

def page(fname, title, desc, body):
    h = head(title, desc)
    content = header(fname) + '\n<main>\n' + body + '\n</main>\n' + footer()
    if ARTIFACT and fname == 'index.html':
        html = h + '\n' + content
    else:
        html = f'<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n{h}\n</head>\n<body>\n{content}\n</body>\n</html>\n'
    open(os.path.join(OUT, fname), 'w').write(html)

# ======================= ACCUEIL =======================
home = film('fuite', 99, [
  (-1,.24,'Plomberie, électricité et forage à Lomé','L’eau et le courant,','sans mauvaise surprise.','BATITECH dépanne, installe et entretient vos réseaux d’eau et d’électricité, et réalise vos forages de puits.', actions_call()),
  (.26,.5,'Le problème','Une fuite, un court-circuit,','une pompe qui lâche ?','On se déplace, on coupe ce qu’il faut couper et on trouve l’origine de la panne avant de toucher à quoi que ce soit.',''),
  (.52,.76,'La réparation','Réparé avec du matériel','qui tient dans le temps.','Raccords, joints, vannes, câbles, disjoncteurs : la pièce usée est remplacée, pas bricolée.',''),
  (.78,2,'Le résultat','Propre, sec,','et contrôlé.','On remet en eau ou sous tension devant vous et on vérifie que tout fonctionne avant de partir.',f'<div class="actions"><a class="btn" href="contact.html" data-magnetic>Demander un devis{I_ARROW}</a></div>'),
], '.26,.52,.78', ['Panne','Réparation','Contrôle'], focus='.62', zoom='1.08,1', remap='0:0 .25:.12 .5:.3 .76:.62 1:1', fid='hero')
home += band(['Plomberie','Électricité','Forage de puits','Dépannage','Pompes immergées','Salles de bains','Tableaux électriques','Devis gratuit'])
home += f'''
<section class="wrap sec"><div class="inner">
{sec_head('Nos métiers','Trois métiers,','une seule équipe.','L’eau qui arrive, l’eau qui s’évacue, le courant qui alimente la pompe : chez vous, tout est lié. Un seul interlocuteur s’occupe de l’ensemble.')}
<div class="trades">
  <a class="trade rv-img" href="plomberie.html"><img src="assets/img/plomberie.webp" alt="Plomberie chromée neuve avec raccord en laiton" loading="lazy"><div class="body"><h3 class="d3">Plomberie<span class="lt">fuites, sanitaires, salles de bains</span></h3><ul><li>Recherche et réparation de fuites</li><li>Débouchage et évacuations</li><li>Salles de bains complètes</li></ul><span class="go">Voir la plomberie{I_ARROW}</span></div></a>
  <a class="trade rv-img" href="electricite.html"><img src="assets/img/electricite.webp" alt="Tableau électrique neuf avec disjoncteurs alignés" loading="lazy"><div class="body"><h3 class="d3">Électricité<span class="lt">installation, dépannage, tableaux</span></h3><ul><li>Installation neuve et rénovation</li><li>Tableaux et disjoncteurs</li><li>Pannes et courts-circuits</li></ul><span class="go">Voir l’électricité{I_ARROW}</span></div></a>
  <a class="trade rv-img" href="forage.html"><img src="assets/img/forage.webp" alt="Foreuse au crépuscule, l’eau jaillit du forage" loading="lazy"><div class="body"><h3 class="d3">Forage<span class="lt">puits, pompes, réservoirs</span></h3><ul><li>Étude du terrain et foration</li><li>Pompe immergée ou solaire</li><li>Château d’eau et raccordement</li></ul><span class="go">Voir le forage{I_ARROW}</span></div></a>
</div></div></section>

<section class="wrap sec" style="padding-top:0"><div class="inner">
{sec_head('Comment on travaille','Du premier appel','à la remise en service.','Vous savez à chaque étape ce qui va être fait, combien ça coûte et quand on intervient.')}
{steps([('Vous nous contactez','Par téléphone ou WhatsApp. Une photo du problème nous aide à préparer le bon matériel.'),('Diagnostic et devis','On passe voir, on identifie la cause et on vous remet un devis détaillé avant tout travail.'),('Intervention','On travaille proprement, on protège les lieux et on remplace ce qui doit l’être.'),('Contrôle et conseils','Essai devant vous, explications, et conseils pour éviter que la panne revienne.')])}
</div></section>

<section class="wrap sec" style="padding-top:0"><div class="inner">
<div class="zone">
  <div><p class="kicker">Zone d’intervention</p><h2 class="d2" data-split>Basés à Amadahomé,<span class="lt">au service du Grand Lomé.</span></h2><p class="lede rv" style="margin-top:20px">Vous êtes plus loin ? Appelez-nous : pour un forage ou un gros chantier, on se déplace au-delà de Lomé sur devis.</p></div>
  <ul class="rv"><li class="home">Amadahomé</li><li>Agoè</li><li>Adidogomé</li><li>Avédji</li><li>Totsi</li><li>Tokoin</li><li>Bè</li><li>Hédzranawoé</li><li>Djidjolé</li><li>Baguida</li><li>Kégué</li><li>Légbassito</li><li>Sanguéra</li><li>Zanguéra</li></ul>
</div></div></section>
{cta()}'''
page('index.html','BATITECH','Plomberie, électricité et forage de puits à Lomé. Dépannage, installation, salles de bains, tableaux électriques, forages et pompes. Basés à Amadahomé.', home)

# ======================= PLOMBERIE =======================
plo = film('sdb', 99, [
  (-1,.26,'Plomberie et sanitaire','Du mur brut','à la salle de bains finie.','Création et rénovation de salles de bains, réseaux d’eau et évacuations, dépannage de fuites.', actions_call()),
  (.28,.56,'Avant le carrelage','Le travail qu’on ne voit pas,','fait dans les règles.','Arrivées d’eau et évacuations posées avec les bonnes pentes, étanchéité sous les revêtements, réseau testé avant fermeture.',''),
  (.58,.84,'Les finitions','Vasque, robinetterie,','tout est posé de niveau.','Chaque élément est choisi avec vous et raccordé proprement, sans joint qui dépasse.',''),
  (.86,2,'La livraison','Livré propre,','prêt à servir.','',f'<div class="actions"><a class="btn" href="contact.html" data-magnetic>Parler de mon projet{I_ARROW}</a></div>'),
], '.28,.58,.86', ['Gros œuvre','Réseaux','Finitions'], focus='.5', zoom='1.04,1', counter='avancement du chantier', fid='hero')
plo += band(['Fuites','Débouchage','Sanitaires','Salles de bains','Chauffe-eau','Surpresseurs','Réservoirs'])
plo += f'''
<section class="wrap sec"><div class="inner">
{sec_head('Prestations','Ce qu’on fait','en plomberie.','Du simple robinet qui goutte à la salle de bains complète, avec le même soin.')}
{services([('Recherche et réparation de fuites','Fuite visible ou cachée, compteur qui tourne sans raison : on localise et on répare.'),('Débouchage','Éviers, lavabos, douches, WC et canalisations bouchés.'),('Installation sanitaire','Pose de lavabos, WC (classiques ou suspendus), douches, éviers et robinetterie.'),('Salle de bains complète','Plomberie, étanchéité, carrelage et finitions, coordonnés par un seul interlocuteur.'),('Chauffe-eau','Installation, remplacement et entretien de chauffe-eau électriques et solaires.'),('Surpresseurs et réservoirs','Pression trop faible, cuve, polytank ou château d’eau : installation et raccordement.'),('Raccordement au réseau','Branchement de votre installation intérieure au compteur de la Togolaise des Eaux.'),('Évacuations et fosses','Pose et reprise des évacuations, regards, raccordement à la fosse septique.'),('Entretien','Contrôle de l’installation, joints, détartrage, pour éviter les mauvaises surprises.')])}
</div></section>
<section class="wrap sec" style="padding-top:0"><div class="inner">
{sec_head('Questions fréquentes','Avant de nous','appeler.','Les réponses aux questions qu’on nous pose le plus souvent.')}
{faq([('Intervenez-vous en urgence ?','Oui. Appelez directement : une fuite importante ne doit pas attendre. En attendant notre arrivée, fermez le robinet général d’arrivée d’eau.'),('Le devis est-il payant ?','Non, le devis est gratuit. On vous le remet après avoir vu le problème sur place.'),('Fournissez-vous le matériel ?','Oui, ou on pose celui que vous avez déjà acheté. On vous conseille sur les références qui tiennent dans le temps.'),('Combien de temps pour une salle de bains complète ?','Cela dépend de la surface et des finitions choisies. Le planning est indiqué dans le devis, avant le début du chantier.')])}
</div></section>
{cta('Une fuite ?','On arrive.','Fermez l’arrivée d’eau, puis appelez-nous ou envoyez une photo sur WhatsApp.')}'''
page('plomberie.html','Plomberie — BATITECH','Plombier à Lomé : fuites, débouchage, installations sanitaires, salles de bains complètes, chauffe-eau, surpresseurs. Devis gratuit.', plo)

# ======================= ÉLECTRICITÉ =======================
ele = film('elec', 99, [
  (-1,.26,'Électricité générale','Des fils qui chauffent,','un disjoncteur qui saute ?','Installation, rénovation et dépannage électrique pour maisons, boutiques et bureaux.', actions_call()),
  (.28,.56,'La mise en sécurité','On coupe, on trace,','on refait proprement.','Câbles de bonne section, connexions serrées, circuits séparés : on élimine ce qui provoque chauffes et étincelles.',''),
  (.58,.84,'Le tableau','Un tableau clair,','chaque circuit protégé.','Disjoncteurs adaptés, différentiel pour protéger les personnes, repérage de chaque circuit.',''),
  (.86,2,'Le résultat','Le courant revient,','en sécurité.','',f'<div class="actions"><a class="btn" href="contact.html" data-magnetic>Demander un devis{I_ARROW}</a></div>'),
], '.28,.58,.86', ['Panne','Mise en sécurité','Tableau'], focus='.66', zoom='1.08,1', fid='hero')
ele += band(['Installation','Rénovation','Tableaux','Dépannage','Éclairage','Prises et circuits','Mise en sécurité'])
ele += f'''
<section class="wrap sec"><div class="inner">
{sec_head('Prestations','Ce qu’on fait','en électricité.','Une installation électrique bien faite, c’est moins de pannes, moins d’appareils grillés et moins de risques d’incendie.')}
{services([('Installation neuve','Villa, appartement, boutique ou bureau : de la saignée au tableau, prête pour le raccordement.'),('Rénovation et mise en sécurité','Remplacement des vieux câbles, des connexions fondues et des prises dangereuses.'),('Tableau électrique','Pose ou remplacement du tableau, disjoncteurs adaptés et différentiel de protection.'),('Dépannage','Coupures, courts-circuits, disjoncteur qui saute, prises ou lampes qui ne marchent plus.'),('Éclairage','Éclairage intérieur, extérieur et de façade, interrupteurs, va-et-vient, détecteurs.'),('Circuits dédiés','Lignes séparées pour climatiseurs, chauffe-eau, pompes et cuisinières.'),('Alimentation des pompes','Câblage et protection des pompes de forage et des surpresseurs, en lien avec nos équipes plomberie et forage.'),('Préparation au raccordement CEET','Installation intérieure conforme et prête pour le branchement au compteur.'),('Contrôle d’installation','Vérification complète avant achat, location ou après des pannes répétées.')])}
</div></section>
<section class="wrap sec" style="padding-top:0"><div class="inner">
{sec_head('Questions fréquentes','Avant de nous','appeler.','Les réponses aux questions qu’on nous pose le plus souvent.')}
{faq([('Mon disjoncteur saute sans arrêt, que faire ?','Débranchez les appareils du circuit concerné et ne forcez pas le réarmement. Un disjoncteur qui saute signale une surcharge ou un défaut : appelez-nous pour le diagnostic.'),('Une prise chauffe ou sent le brûlé, est-ce grave ?','Oui. Coupez le circuit au tableau et n’utilisez plus la prise. C’est un risque d’incendie à traiter rapidement.'),('Le devis est-il payant ?','Non, le devis est gratuit et remis après visite.'),('Pouvez-vous alimenter une pompe de forage ?','Oui. On câble et on protège la pompe, et on coordonne avec l’équipe forage si le puits est aussi à réaliser.')])}
</div></section>
{cta('Une panne de courant ?','On la trouve.','Coupez le disjoncteur concerné, puis appelez-nous ou envoyez une photo de votre tableau sur WhatsApp.')}'''
page('electricite.html','Électricité — BATITECH','Électricien à Lomé : installation électrique neuve, rénovation et mise en sécurité, tableaux, dépannage, éclairage. Devis gratuit.', ele)

# ======================= FORAGE =======================
forg = film('forage', 99, [
  (-1,.24,'Forage de puits','Pas d’eau courante,','ou pas assez ?','On réalise votre forage et on l’équipe pour que l’eau arrive au robinet, toute l’année.', actions_call()),
  (.26,.52,'La foration','On fore','jusqu’à la nappe.','Implantation choisie après étude du terrain, puis foration et pose du tubage pour protéger l’ouvrage.',''),
  (.54,.8,'L’eau','L’eau jaillit.','Elle est à vous.','Développement du forage et essai de débit pour connaître ce que votre puits peut fournir.',''),
  (.82,2,'L’équipement','Pompe, réservoir,','robinet.','Pompe immergée ou solaire, château d’eau et raccordement à la maison, câblés par nos électriciens.',f'<div class="actions"><a class="btn" href="contact.html" data-magnetic>Étudier mon terrain{I_ARROW}</a></div>'),
], '.26,.54,.82', ['Foration','Eau','Équipement'], focus='.62', zoom='1.06,1', fid='hero')
forg += band(['Forage','Pompes immergées','Pompage solaire','Châteaux d’eau','Polytanks','Réhabilitation'])
forg += f'''
<section class="wrap sec"><div class="inner">
{sec_head('Les étapes','Un forage,','étape par étape.','Chaque étape conditionne la qualité et la durée de vie de votre puits. Aucune n’est sautée.')}
{steps([('Étude du terrain','Visite, choix de l’emplacement et estimation de la profondeur à atteindre.'),('Foration','Forage jusqu’à la nappe avec une machine adaptée au sol.'),('Équipement du puits','Tubage, crépines, massif filtrant et cimentation de la tête du forage.'),('Essai de débit','Développement du forage et mesure du débit disponible.'),('Pompe et réseau','Pompe, réservoir, câblage et raccordement jusqu’à vos robinets.')])}
</div></section>
<section class="wrap sec" style="padding-top:0"><div class="inner">
{sec_head('Prestations','Ce qu’on fait','autour de votre eau.','Du trou dans le sol au robinet de la cuisine, un seul interlocuteur.')}
{services([('Forage domestique','Pour une maison ou une concession : eau pour la cuisine, la douche et l’arrosage.'),('Forage professionnel','Boutiques, ateliers, fermes et petites exploitations avec des besoins plus importants.'),('Pompe immergée','Choix, pose, câblage et protection électrique de la pompe.'),('Pompage solaire','Pompe alimentée par panneaux solaires pour ne plus dépendre du réseau électrique.'),('Château d’eau et réservoirs','Pose de polytanks et de réservoirs surélevés, raccordement à la maison.'),('Réhabilitation','Forage qui donne moins d’eau ou de l’eau trouble : diagnostic, nettoyage et remise en service.')])}
</div></section>
<section class="wrap sec" style="padding-top:0"><div class="inner">
{sec_head('Questions fréquentes','Avant de lancer','votre forage.','Les réponses aux questions qu’on nous pose le plus souvent.')}
{faq([('À quelle profondeur faut-il forer ?','Cela dépend de la nappe sous votre terrain. On l’estime lors de l’étude, et la profondeur prévue est indiquée dans le devis.'),('Combien coûte un forage ?','Le prix dépend surtout de la profondeur, du sol et de l’équipement choisi (pompe, réservoir, solaire). Le devis est gratuit après visite.'),('L’eau sera-t-elle potable ?','Un forage bien réalisé protège la nappe, mais seule une analyse confirme la potabilité. On vous conseille sur l’analyse et le traitement si nécessaire.'),('Combien de temps durent les travaux ?','La foration elle-même est rapide. L’équipement et le raccordement dépendent de votre installation. Le planning figure dans le devis.')])}
</div></section>
{cta('Un projet de forage ?','Parlons de votre terrain.','Envoyez la localisation de votre terrain sur WhatsApp, on organise l’étude.')}'''
page('forage.html','Forage — BATITECH','Forage de puits à Lomé et environs : étude du terrain, foration, pompe immergée ou solaire, château d’eau et raccordement.', forg)

# ======================= AVANT / APRÈS =======================
def ba(key, title, sub):
    return f'''<figure class="ba rv"><div class="ba-frame"><img src="assets/img/{key}-avant.webp" alt="{title}, avant" loading="lazy"><img class="after" src="assets/img/{key}-apres.webp" alt="{title}, après" loading="lazy"><span class="tag l">Avant</span><span class="tag r">Après</span><i class="handle"><b>‹ ›</b></i><input type="range" min="0" max="100" value="50" aria-label="Comparer avant et après : {title}"></div><figcaption><b>{title}</b><span>{sub}</span></figcaption></figure>'''
bap = f'''<section class="wrap page-hero"><div class="inner">
<p class="kicker">Avant / après</p><h1 class="d1" data-split>Glissez pour voir<span class="lt">la différence.</span></h1>
<p class="lede" style="margin-top:22px">Faites glisser le curseur sur chaque image pour comparer l’état avant et après l’intervention.</p>
</div></section>
<section class="wrap sec" style="padding-top:0"><div class="inner">
<div class="ba-grid">
{ba('fuite','Réparation de fuite','Plomberie')}
{ba('elec','Mise en sécurité électrique','Électricité')}
{ba('sdb','Salle de bains complète','Plomberie et finitions')}
{ba('forage','Forage de puits','Forage')}
</div>
<p class="note">Visuels d’illustration. Remplacez-les par les photos de vos propres chantiers (dossier assets/img, même nom de fichier).</p>
</div></section>
{cta()}'''
page('avant-apres.html','Avant / après — BATITECH','Avant et après nos interventions en plomberie, électricité et forage à Lomé.', bap)

# ======================= CONTACT =======================
con = f'''<section class="wrap page-hero"><div class="inner">
<p class="kicker">Contact</p><h1 class="d1" data-split>Parlons de<span class="lt">votre problème d’eau ou de courant.</span></h1>
</div></section>
<section class="wrap sec" style="padding-top:0"><div class="inner contact">
  <div class="c-card">
    <div class="c-line"><small>Téléphone et WhatsApp</small><span class="big" data-phone></span>
      <div class="row"><a class="btn" data-tel href="#" data-magnetic>{I_PHONE}Appeler</a><a class="btn ghost" data-wa="Bonjour BATITECH," href="#">{I_WA}WhatsApp</a><button class="btn ghost" type="button" data-copy>Copier le numéro</button></div></div>
    <div class="c-line"><small>Adresse</small><span style="font-size:20px;font-weight:700" data-address></span><span class="muted">Interventions dans tout le Grand Lomé.</span></div>
    <div class="c-line" style="border:0"><small>En cas d’urgence</small><p style="margin:0">Fuite : fermez le robinet général d’arrivée d’eau.<br>Panne électrique : coupez le disjoncteur principal.<br>Puis appelez-nous.</p></div>
  </div>
  <form class="cf" novalidate>
    <h2 class="d3">Décrivez votre besoin<span class="lt">on vous répond sur WhatsApp</span></h2>
    <div class="field"><label>Service concerné</label><div class="chips">
      <label><input type="radio" name="service" value="Plomberie" checked><span>Plomberie</span></label>
      <label><input type="radio" name="service" value="Électricité"><span>Électricité</span></label>
      <label><input type="radio" name="service" value="Forage"><span>Forage</span></label>
      <label><input type="radio" name="service" value="Plusieurs / autre"><span>Plusieurs / autre</span></label></div></div>
    <div class="two"><div class="field"><label for="f-nom">Votre nom</label><input id="f-nom" name="nom" autocomplete="name" required></div>
      <div class="field"><label for="f-tel">Votre numéro</label><input id="f-tel" name="tel" type="tel" autocomplete="tel" inputmode="tel" placeholder="+228 …"></div></div>
    <div class="two"><div class="field"><label for="f-q">Quartier</label><input id="f-q" name="quartier" placeholder="Ex. Agoè, Adidogomé…"></div>
      <div class="field"><label>Urgent ?</label><div class="chips"><label><input type="radio" name="urgence" value="Non" checked><span>Non</span></label><label><input type="radio" name="urgence" value="Oui, urgent"><span>Oui, urgent</span></label></div></div></div>
    <div class="field"><label for="f-msg">Votre besoin</label><textarea id="f-msg" name="message" required placeholder="Ex. fuite sous l’évier de la cuisine depuis ce matin."></textarea></div>
    <div class="actions" style="margin-top:4px"><button class="btn" type="submit">Préparer mon message</button><a class="btn ghost" id="wa-send" href="#" target="_blank" rel="noopener" hidden>{I_WA}Ouvrir WhatsApp</a></div>
    <p class="form-msg" role="status" aria-live="polite"></p>
  </form>
</div></section>'''
page('contact.html','Contact — BATITECH','Contactez BATITECH à Amadahomé, Lomé : téléphone, WhatsApp, demande de devis.', con)
print('ok')
