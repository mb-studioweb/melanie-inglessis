# Mélanie Inglessis — portfolio concept

Independent concept portfolio for celebrity makeup artist **Mélanie Inglessis**, built from the Untitled Film Framer visual language and verified research PDFs in this repository.

## Content sources

- `Melanie_Inglessis_Portfolio_Content_Brief.pdf`
- `Melanie_Inglessis_Artists_People_10.pdf`

## Local preview

```bash
cd template && python3 -m http.server 8080
```

Open http://localhost:8080

## Rebuild pages from data

```bash
python3 scripts/build-site.py
```

Centralized data lives in:

- `template/data/site.json`
- `template/data/projects.json`
- `template/data/people.json`

## GitHub Pages

Publish root: `template/`

1. [Settings → Pages](https://github.com/mb-studioweb/melanie-inglessis/settings/pages)
2. Source: **Deploy from a branch** → `gh-pages` / `/(root)`

URL: https://mb-studioweb/melanie-inglessis → `https://mb-studioweb.github.io/melanie-inglessis/`

## Images

See `template/ASSETS.md`. Current heroes are concept placeholders pending licensed editorial assets.
