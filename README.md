# vitomengers.github.io

Source of my personal academic website, [vitomengers.github.io](https://vitomengers.github.io).

Built with [Jekyll](https://jekyllrb.com/) on the [al-folio](https://github.com/alshedivat/al-folio) theme and deployed with GitHub Pages.

## Where things live

| Content                    | Location                                     |
| -------------------------- | -------------------------------------------- |
| About page                 | `_pages/about.md`                            |
| Publications               | `_bibliography/papers.bib`                   |
| Publication preview images | `assets/img/publication_preview/`            |
| News                       | `_news/`                                     |
| Talks & posters            | `_talks/`                                    |
| Outreach                   | `_outreach/`                                 |
| Teaching & supervision     | `_teachings/`                                |
| CV data                    | `_data/cv.yml` (PDF built by `build-cv.yml`) |

Preview GIFs are shown at about 200px wide, so keep them small (roughly 320px wide, 8–10 fps, a few MB at most), for example:

```bash
ffmpeg -i in.gif -vf "fps=10,scale=320:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64:stats_mode=diff[p];[b][p]paletteuse=dither=none:diff_mode=rectangle" -loop 0 out.gif
```

## Local development

See the theme's [INSTALL.md](INSTALL.md), [CUSTOMIZE.md](CUSTOMIZE.md) and [FAQ.md](FAQ.md). With Docker:

```bash
docker compose pull && docker compose up
```

## License

The theme is available under the [MIT license](LICENSE).
