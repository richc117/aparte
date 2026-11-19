# Maintaining the Aparté site

Notes for whoever updates the website and the downloads. The README is the product page.

The site is plain HTML and two stylesheets. No JavaScript, no analytics, no third-party
requests: the fonts are served from this repository and the pages carry a
Content-Security-Policy that allows nothing else. Aparté's source code is not here. It
stays in a private repository.

## Files

| Path | What it is |
|---|---|
| `index.html` | The page: statement, how it works, privacy, install, feedback |
| `credits.html` | Credits and licenses for the model, libraries and fonts |
| `styles.css` | All styling. Dark by default, light when the visitor's system is set to light |
| `animation.css` | The animated scene in How it works (CSS and SVG, no JavaScript). Built from `tools/animation/`, see below |
| `tools/animation/` | `build.py` and `static.css`: edit the timing or the look there, then run `python3 tools/animation/build.py` to rewrite `animation.css` |
| `fonts/` | Instrument Serif and Instrument Sans (Latin subsets, woff2) and their OFL licenses |
| `licenses/` | License texts for FluidAudio and KeyboardShortcuts |
| `favicon.svg`, `apple-touch-icon.png` | From the app's brand kit |
| `docs/` | This file, and the two images the README shows |
| `README.md` | The GitHub front page: a copy of the site's content, so keep the two in step |

Every link is relative, so the site works at `richc117.github.io/aparte/` without changes.

## Look at it locally

```
python3 -m http.server 8000 --bind 127.0.0.1
```

Then open http://127.0.0.1:8000. (Opening the files directly with `file://` shows
fallback fonts, because the Content-Security-Policy treats local files as a different
origin.)

## Where it lives

The site is live at https://richc117.github.io/aparte/ (GitHub Pages, `main` branch, root
folder). A push to `main` updates it within a minute or two. The v0.1.0 Release holds the
download. The repository's "About" link and the README both point at the site.

## Each new release

1. In the app repository, from a clean committed tree: `./scripts/package.sh --release`.
   It prints the SHA-256 and writes `dist/Aparte.zip`.
2. Create a new GitHub Release here with `Aparte.zip` attached (`gh release create vX.Y.Z
   dist/Aparte.zip`). Keep the file named exactly `Aparte.zip`, and do not mark it a
   pre-release, because the Download button links to `releases/latest/download/Aparte.zip`
   and "latest" skips pre-releases.
3. Update the version and the size in the fine print under the Download button, in both
   `index.html` and `README.md`.
4. Commit and push. The site updates within a minute or two.

The zip is about 450 MB, so it must never be committed to the repository (GitHub rejects
files over 100 MB). Release attachments are the right place for it.

## Not done yet

- A social preview image (`og:image`) for link previews. Decided not needed for now.
- A statement of the app's license terms. The footer says only "Provided as is,
  without warranty."

## The How it works animation

A 14-second loop of the three steps: keys press, the menu bar icon changes state (the
app's real Ready, Listening and Transcribing icons), the five lines move like a voice,
and on release a ring leaves the icon and the text lands on the clipboard. The steps on
the left light up in step with it. Everything runs on one shared timeline, so change
times only in `tools/animation/build.py`.

- With "reduce motion" on, nothing moves: the page shows the finished state.
- The voice lines are illustration. The app itself has no live waveform.
- The sentence on the clipboard is placeholder text.
- Every animation must start at 0 and end at 14 seconds. A missing end keyframe makes the
  browser animate toward the element's own style, which once made the lines flash at the
  end of the loop. `build.py` refuses to build if one is missing.
