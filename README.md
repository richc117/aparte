# Aparté website

The public site for Aparté, a private dictation app for Mac. Plain HTML and two
stylesheets. No JavaScript, no analytics, no third-party requests: the fonts are served
from this folder and the pages carry a Content-Security-Policy that allows nothing else.

The app's source code is not here. It stays in a private repository.

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

Every link is relative, so the site works at `richc117.github.io/aparte/` without changes.

## Look at it locally

```
python3 -m http.server 8000 --bind 127.0.0.1
```

Then open http://127.0.0.1:8000. (Opening the files directly with `file://` shows
fallback fonts, because the Content-Security-Policy treats local files as a different
origin.)

## Publishing (once)

1. Create a public GitHub repo named `aparte` under `richc117`.
2. Push this folder to it.
3. Settings, Pages: deploy from the `main` branch, root folder.
4. The site appears at `https://richc117.github.io/aparte/`.

The same repo hosts the downloads (Releases) and feedback (Issues). Turn on Issues in
Settings if they are off.

## Each new release

1. In the app repository, from a clean committed tree: `./scripts/package.sh --release`.
   It prints the SHA-256 and writes `dist/Aparte.zip`.
2. Attach `Aparte.zip` to a GitHub Release in this repo. Keep the file named exactly
   `Aparte.zip`, because the Download button links to
   `releases/latest/download/Aparte.zip`.
3. In `index.html`, update the version, the size, and the SHA-256 in the Install section.
4. Commit and push. Pages updates within a minute or two.

The zip is 448 MB, so it must never be committed to the repository (GitHub rejects
files over 100 MB). Release attachments are the right place for it.

## Not done yet

- A social preview image (`og:image`) for link previews.
- A statement of the app's license terms. The footer says only "Provided as is,
  without warranty."
- The next app release must include the Credits window (commit `b7ffb4f` in the app
  repository). Build 27, the zip currently in `dist/`, predates it.

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
