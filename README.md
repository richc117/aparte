<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/swell-dark.svg">
    <img src="docs/swell-light.svg" alt="The Aparté mark: five nested lines rising into a single peak" width="300">
  </picture>
</p>

<h1 align="center">Aparté</h1>

<p align="center"><em>Dictation that keeps to itself.</em></p>

Hold a shortcut, speak, and let go. Aparté turns your voice into text on your Mac and copies it to the clipboard. It never connects to the internet.

<p align="center"><strong><a href="https://github.com/richc117/aparte/releases/latest/download/Aparte.zip">Download Aparté for Mac</a></strong></p>

<p align="center"><sub>Version 0.1.1, 453 MB. For Macs with Apple Silicon running macOS 14 or later. English only.</sub></p>

<p align="center"><a href="https://richc117.github.io/aparte/">richc117.github.io/aparte</a></p>

## How it works

**Hold.** Press and hold <kbd>Control</kbd> <kbd>Option</kbd> <kbd>Space</kbd> together. You can choose a different shortcut in Settings.

**Speak.** Say what you want written. Aparté listens only while the shortcut is held.

**Release.** Let go, and a soft sound tells you the text is on your clipboard. Paste it wherever you like.

If you would rather not hold a key, Settings has a mode where you press once to start and again to stop. Recordings end on their own after five minutes.

Aparté lives in the menu bar. From there you can open a history of your dictations, and a list of fix-up words for names and terms you want spelled your way.

## Privacy

**No network.** Aparté has no permission to connect to the internet, so it cannot send your voice or your text anywhere. The speech model is inside the app, and nothing is downloaded when you open it.

**Audio stays in memory.** Your recording is turned into text and then discarded. It is never saved to disk.

**The clipboard copy stays local.** It is not shared with your other Apple devices, and clipboard managers are asked to skip it.

**History stays on your Mac.** Saved dictations live in the app's own folder, are left out of Time Machine backups, and are deleted after 30 days unless you choose otherwise. You can delete one or all of them at any time, or turn history off.

**It does not type into other apps.** Aparté only writes to the clipboard, so the one permission it asks for is the microphone.

You can check the no-network claim yourself. This prints the app's permissions:

```
codesign -d --entitlements :- /Applications/Aparte.app
```

Two entries appear, `com.apple.security.app-sandbox` and `com.apple.security.device.audio-input`. There is no network entry.

## Install

1. [Download `Aparte.zip`](https://github.com/richc117/aparte/releases/latest/download/Aparte.zip), open it, and drag Aparté into your Applications folder.
2. Open it. macOS may ask you to confirm an app downloaded from the internet. Apple has checked this release for malicious software, so choose Open.
3. The first launch prepares the speech model for your Mac. A window shows its progress and tells you when Aparté is ready. This takes up to a minute, and later launches take seconds.
4. Allow microphone access when macOS asks.

Aparté never checks for updates by itself. New versions appear under [Releases](https://github.com/richc117/aparte/releases).

## Feedback

Questions, ideas and problems are welcome. [Open an issue on GitHub](https://github.com/richc117/aparte/issues/new).

Issues are public, so please leave out anything private, including dictated text.

## Credits

Aparté is built on the work of others.

- **Parakeet TDT 0.6B v2**, the speech recognition model inside Aparté, created by NVIDIA and released under the [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/) license. Aparté uses the CoreML conversion made by FluidInference, which is the only change to the original. [Original model](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v2), [CoreML conversion](https://huggingface.co/FluidInference/parakeet-tdt-0.6b-v2-coreml).
- **FluidAudio**, the Swift library that runs the model on your Mac's Neural Engine, by FluidInference, under the Apache License 2.0. [Project](https://github.com/FluidInference/FluidAudio), [license text](licenses/FluidAudio-LICENSE.txt).
- **KeyboardShortcuts**, which lets you choose your own shortcut, by Sindre Sorhus, under the MIT License. [Project](https://github.com/sindresorhus/KeyboardShortcuts), [license text](licenses/KeyboardShortcuts-LICENSE.txt).
- **Instrument Serif** and **Instrument Sans**, the typefaces on the Aparté website and in its wordmark, by the Instrument project under the SIL Open Font License 1.1. [Instrument Serif](https://github.com/Instrument/instrument-serif) ([license](fonts/OFL-Instrument-Serif.txt)), [Instrument Sans](https://github.com/Instrument/instrument-sans) ([license](fonts/OFL-Instrument-Sans.txt)).

---

Aparté is a personal project by Richard Caballero. Provided as is, without warranty.
