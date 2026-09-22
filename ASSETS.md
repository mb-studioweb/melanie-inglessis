# Images du portfolio — statut & mode d’emploi

> Concept privé uniquement. Ces fichiers sont des **mock-ups temporaires**.  
> Un lancement public exige droits / autorisations (magazines, photographes, talents).

## Comment remplacer une image (toi-même)

1. Ouvre l’URL source ci-dessous.
2. Télécharge la meilleure image (clic droit → Enregistrer, ou export Models.com / page presse).
3. Remplace le fichier local **en gardant le même chemin et le nom `hero.jpg`**.
4. Format conseillé : JPEG, portrait ~1600×2000 (ou plus), visage/makeup bien cadrés.
5. Relance le site (`python3 -m http.server` dans `template/`) — pas besoin de rebuild si le chemin est identique.

Exemple :
```bash
# remplace juste le fichier
cp ~/Downloads/vogue-mexico-hero.jpg template/images/projects/vogue-mexico-jenna-ortega-2025/hero.jpg
```

Métadonnées techniques : `template/images/SOURCES.json`

---

## Statut actuel

### Projets — images récupérées automatiquement
| Fichier | Projet | Source |
|---|---|---|
| `images/projects/esquire-us-jenna-ortega-2026/hero.jpg` | Esquire U.S. | [Models.com](https://models.com/work/esquire-us-jenna-ortega-wont-stop-taking-risks-no-matter-how-big-wednesday-gets) |
| `images/projects/vogue-mexico-jenna-ortega-2025/hero.jpg` | Vogue Mexico | [Models.com](https://models.com/work/vogue-mexico-un-espiritu-libre) |
| `images/projects/vogue-24-goth-hours-2025/hero.jpg` | 24 Goth Hours | [Vogue](https://www.vogue.com/article/24-goth-hours-with-jenna-ortega) |
| `images/projects/netflix-wednesday-s2-2025/hero.jpg` | Netflix × Wednesday S2 | [Models.com](https://models.com/work/netflix-netflix-x-wednesday) |
| `images/projects/the-cut-jenna-ortega-2025/hero.jpg` | The Cut | [Models.com](https://models.com/work/the-cut-jenna-ortega-knows-best-1) |
| `images/projects/wwd-weekend-ana-de-armas-2025/hero.jpg` | WWD Weekend | [Models.com](https://models.com/work/wwd-wwd-weekend-may-2025-cover) |
| `images/projects/wednesday-s2-premiere-2025/hero.jpg` | Wednesday S2 premiere | [Vogue UK](https://www.vogue.co.uk/article/jenna-ortega-glam-wednesday-season-2) |
| `images/projects/met-gala-jenna-ortega-2025/hero.jpg` | Met Gala 2025 | [Vogue US — ruler dress](https://www.vogue.com/article/jenna-ortega-metal-ruler-dress-2025-met-gala) *(corrigé : ancienne image Vogue France incorrecte)* |
| `images/projects/academy-museum-gala-2025/hero.jpg` | Academy Museum Gala | [Vogue MX](https://www.vogue.mx/articulo/jenna-ortega-top-plateado-y-falda-cafe-academy-museum-gala-2025) |
| `images/projects/instyle-imagemaker-2025/hero.jpg` | InStyle ImageMaker | [Vogue](https://www.vogue.com/article/jenna-ortega-pauses-goth-glam-for-something-more-soft) |
| `images/projects/sundance-the-gallerist-2026/hero.jpg` | Sundance 2026 | [Vogue](https://www.vogue.com/article/jenna-ortega-lightens-up-her-gothic-glam-for-sundance) |
| `images/projects/actor-awards-2026/hero.jpg` | Actor Awards 2026 | [Allure](https://www.allure.com/story/jenna-ortega-actor-awards-dark-brows) |
| `images/projects/no-time-to-die-premiere-2021/hero.jpg` | No Time to Die | [Vogue](https://www.vogue.com/article/ana-de-armas-bond-premiere-getting-ready) |
| `images/projects/blonde-premiere-2022/hero.jpg` | Blonde premiere | [Vogue](https://www.vogue.com/slideshow/ana-de-armas-blonde-premiere-marilyn-monroe) |
| `images/projects/golden-globes-ana-de-armas-2023/hero.jpg` | Golden Globes 2023 | [Vogue](https://www.vogue.com/slideshow/ana-de-armas-golden-globes-louis-vuitton-dress) |
| `images/projects/motion-taste-jenna-ortega/hero.jpg` | Taste (motion) | YouTube thumb FA / Taste — [Forward Artists motion](https://www.forwardartists.com/makeup/melanie-inglessis-motion) |
| `images/projects/motion-armani-luminous-silk/hero.jpg` | Armani Luminous Silk | Forward Artists motion |
| `images/projects/motion-doritos-dina-mita/hero.jpg` | Doritos Dina & Mita | Forward Artists motion |
| `images/projects/motion-only-natural-diamonds/hero.jpg` | Only Natural Diamonds | Forward Artists / YouTube |
| `images/projects/motion-la-mer-ana-de-armas/hero.jpg` | La Mer | Forward Artists motion |
| `images/projects/motion-loreal-longoria-king/hero.jpg` | L’Oréal Paris | Forward Artists motion |
| `images/projects/motion-britney-slumber-party/hero.jpg` | Slumber Party | Forward Artists motion |
| `images/projects/motion-britney-make-me/hero.jpg` | Make Me | Forward Artists motion |

### People
| Fichier | Personne | Note |
|---|---|---|
| `images/people/jenna-ortega/hero.jpg` | Jenna Ortega | Models.com (Vogue Mexico) |
| `images/people/ana-de-armas/hero.jpg` | Ana de Armas | Models.com (WWD) |
| `images/people/olivia-wilde/hero.jpg` | Olivia Wilde | Wikimedia — portrait d’identité (pas un credit makeup Mélanie) |
| `images/people/kate-hudson/hero.jpg` | Kate Hudson | Wikimedia — portrait d’identité |
| `images/people/karlie-kloss/hero.jpg` | Karlie Kloss | Wikimedia — portrait d’identité |
| `images/people/ruth-negga/hero.jpg` | Ruth Negga | Wikimedia — portrait d’identité |
| `images/people/rosamund-pike/hero.jpg` | Rosamund Pike | ELLE og:image |
| `images/people/natalie-portman/hero.jpg` | Natalie Portman | Wikimedia — portrait d’identité |
| `images/people/lea-michele/hero.jpg` | Lea Michele | Wikimedia — portrait d’identité |
| `images/people/britney-spears/hero.jpg` | Britney Spears | Billboard og:image |

### À améliorer manuellement (recommandé)
Les pages People sans collaboration photographiée dans les PDF (Olivia, Kate, Karlie, Ruth, Natalie, Lea) utilisent des **portraits Wikimedia d’identité**.  
Idéal : remplacer par une image **beauté / red carpet** issue d’un article qui crédite Mélanie (voir le PDF People).

Pour Models.com : ouvrir le work → télécharger la plus grande preview disponible (parfois meilleure que le `800w` récupéré automatiquement).
