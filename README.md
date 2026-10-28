# BATITECH — site web

Site vitrine de **BATITECH** (plomberie, électricité et forage de puits — Amadahomé, Lomé).
Site 100 % statique : HTML, CSS et JavaScript, sans framework ni étape de build obligatoire.

## Pages

| Fichier | Contenu |
|---|---|
| `index.html` | Accueil : film « fuite réparée » au scroll, les trois métiers, méthode, zone d'intervention |
| `plomberie.html` | Film chantier salle de bains (compteur %), prestations, FAQ |
| `electricite.html` | Séquence panne → nouveau tableau, prestations, FAQ |
| `forage.html` | Séquence foration → l'eau jaillit, étapes d'un forage, prestations, FAQ |
| `avant-apres.html` | Comparateurs avant / après à faire glisser |
| `contact.html` | Coordonnées et formulaire qui prépare un message WhatsApp |

## Modifier les coordonnées

Tout est dans **`assets/js/config.js`** (téléphone, WhatsApp, adresse). Les valeurs sont injectées
automatiquement dans l'en-tête, les pages, le pied de page et le formulaire.

## Structure

```
assets/
  css/style.css        styles (couleurs en variables en haut du fichier)
  js/config.js         coordonnées
  js/main.js           titres animés mot par mot, fondus légers, séquences au scroll,
                       menu mobile, FAQ, avant/après, formulaire WhatsApp
  frames/<film>/       images des séquences (0001.webp → 0099.webp)
  img/                 visuels des cartes et des comparateurs avant/après
  img/brand/           logo (symbole B + mot BATITECH, couleur et blanc), favicon
tools/build.py         générateur des pages (gabarit commun en-tête / pied) — optionnel
```

## Films au scroll

Chaque section `.film` lit une séquence d'images (`data-seq`, `data-count`) et l'affiche dans un
`<canvas>` plein écran selon la position du scroll ; les légendes (`data-from` / `data-to`) se relaient et leurs titres apparaissent mot par mot.
Les images ne sont chargées qu'à l'approche de la section. Pour remplacer une séquence :

1. générer une vidéo courte, caméra fixe ;
2. la découper : `ffmpeg -i video.mp4 -vf "fps=15,scale=1440:-2" -c:v libwebp -q:v 62 assets/frames/<nom>/%04d.webp`
3. mettre à jour `data-count` si le nombre d'images change.

## Images

Les visuels actuels sont des illustrations générées par IA. Remplacez-les par de vraies photos de
chantier en gardant les mêmes noms de fichiers dans `assets/img/`.

## Mise en ligne

Aucun build : servez le dossier tel quel (GitHub Pages, Netlify, Vercel, hébergement mutualisé).
Pour GitHub Pages : *Settings → Pages → Deploy from a branch → `main` / root*.

Les pages contiennent tout le HTML : `tools/build.py` n'est utile que pour régénérer les six pages
après une modification du gabarit commun (`python3 tools/build.py .`).

## Version précédente

La version « cinéma » (films plein écran, rideau, préchargement) est conservée dans la branche `v1-cinema`.
