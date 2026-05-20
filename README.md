# TV Renamer

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE.md)
![Platform](https://img.shields.io/badge/platform-Windows-0078D6)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Status](https://img.shields.io/badge/status-active-success)
![Jellyfin](https://img.shields.io/badge/Jellyfin-compatible-8250df)
![Plex](https://img.shields.io/badge/Plex-compatible-e5a00d)
![MakeMKV](https://img.shields.io/badge/MakeMKV-supported-red)
![MKVToolNix](https://img.shields.io/badge/MKVToolNix-supported-orange)
![Open Source](https://img.shields.io/badge/open--source-yes-brightgreen)
![GitHub release](https://img.shields.io/github/v/release/azureprizm/TV_Renamer)
![GitHub downloads](https://img.shields.io/github/downloads/azureprizm/TV_Renamer/total)
![GitHub Downloads (latest)](https://img.shields.io/github/downloads/azureprizm/TV_Renamer/latest/total)
![GitHub stars](https://img.shields.io/github/stars/azureprizm/TV_Renamer)
![GitHub issues](https://img.shields.io/github/issues/azureprizm/TV_Renamer)

---
## Stable Usage

Most users should use the packaged release from the Releases page. [Download version 1.2.0](https://github.com/azureprizm/TV_Renamer/releases/tag/v1.2.0)

The source branch may contain active development changes, refactors, broken or experimental features that are not yet reflected in the standalone EXE.

---

TV Renamer is a lightweight Windows utility for organizing physical-media TV rips from MakeMKV into Jellyfin- and Plex-friendly season folders.

It watches a dedicated MakeMKV output folder, waits for completed `.mkv` files, then automatically:

- determines the next episode number
- renames episodes sequentially
- moves episodes into the correct show/season folder
- preserves numbering across multiple discs
- optionally splits long anime MKV files into individual episodes

---

# Why This Exists

Most media automation tools were built around downloaded files, metadata scraping, and import queues. Physical DVD and Blu-ray TV workflows are different.

When ripping a box set, the most reliable information is often the order you choose valid episode titles in MakeMKV.

TV Renamer is built around a simple assumption:

```text
rip order == episode order
```

If you select only real episode titles and rip them sequentially, episode numbering becomes deterministic. No online lookup is required.

---

# Why TV Renamer?

TV Renamer is intentionally designed for physical media workflows.

Unlike Sonarr/FileBot-style workflows, TV Renamer:

- does not require metadata scraping
- does not require internet lookups
- does not require drag/drop importing
- does not require a manual renaming pass
- does not try to identify episodes by title or fingerprint

If your workflow already preserves episode order, deterministic sequential numbering is simpler and more predictable.

---

# Designed For

TV Renamer is ideal for:

- DVD TV box sets
- Blu-ray TV collections
- anime discs with multi-episode MKV titles
- Jellyfin libraries
- Plex libraries
- archival workflows
- offline media libraries
- users who rip episodes sequentially

---

# Not Intended For

TV Renamer is not designed for:

- downloaded scene releases
- automatic metadata matching
- anime absolute numbering
- mixed or reordered episode layouts
- bonus feature identification
- replacing a full media manager

Anime splitting is supported when a long MKV has useful chapter markers near episode boundaries. If chapter data is missing or unusual, TV Renamer falls back to manual timestamp entry.

---

# Features

- Automatic sequential episode numbering
- Multi-disc support
- Jellyfin-compatible naming
- Plex-compatible naming
- Real-time folder monitoring
- File completion/stability detection
- Automatic next-episode detection
- Interactive season switching
- Interactive show switching
- Runtime mode switching
- Live status command
- Desktop GUI front end for session setup, folder watching, queueing, and logs
- Sanitized shareable processing reports
- GUI MakeMKV launch helper
- Folder reconfiguration command
- Windows standalone EXE support
- Anime/Split Mode for long MKV files
- Automatic chapter-based anime split detection
- Optional local IMDb dataset runtime fallback
- Optional ffmpeg black-frame/silence refinement
- Optional ffmpeg frame preview around split boundaries
- Runtime-based anime split fallback when chapter markers are missing
- Manual timestamp splitting fallback
- GUI split confirmation timeline with draggable split markers
- Console progress updates for long-running scans/refinement
- No metadata scraping
- No TMDB dependency
- No Sonarr required
- No paid software required

---

# Requirements

TV Renamer supports two installation methods.

---

## Option 1 - Windows EXE

No Python installation is required.

Download the latest release from:

```text
GitHub -> Releases
```

For most users, download the GUI release zip, extract it to a normal folder such as:

```text
C:\Users\your_username\Apps\TV_Renamer
```

The recommended release zip contains:

```text
TV_Renamer_GUI.exe
README.md
LICENSE.md
RELEASE_NOTES_v1.2.0.md
tv_renamer.ico
create_gui_desktop_shortcut.ps1
```

Then run:

```text
TV_Renamer_GUI.exe
```

On first use:

1. Choose your incoming MakeMKV folder.
2. Choose your TV library root folder.
3. Enter the show name, year, season, and mode.
4. Click `Save Session`.
5. Click `Start Watcher`.
6. Optional: click `Create Desktop Shortcut`.

TV Renamer will create local files such as `config.json` and `IMDb Cache/` beside the app as needed. Do not run the app directly from inside the zip file; extract it first.

TV Renamer also writes sanitized processing reports to:

```text
Reports/shareable/
```

These reports include filenames, selected mode, split timestamps, fallback usage, and created output filenames. They intentionally omit absolute paths, drive letters, Windows usernames, and command lines so they are safer to share in bug reports or community posts.

In the GUI, click `Open Reports` to view the generated report files.

The GUI also includes `Launch MakeMKV`, which opens MakeMKV while TV Renamer continues watching the configured incoming folder. This does not modify MakeMKV settings.

The console EXE, when provided, is named:

```text
TV_Renamer.exe
```

The GUI EXE is named:

```text
TV_Renamer_GUI.exe
```

The GUI is the simplest setup method for most users.

## Release Zip Checklist

When publishing a GUI release zip, include:

```text
TV_Renamer_GUI.exe
README.md
LICENSE.md
RELEASE_NOTES_v1.2.0.md
tv_renamer.ico
create_gui_desktop_shortcut.ps1
```

Do not include:

```text
config.json
IMDb Datasets/
IMDb Cache/
Reports/
build/
dist/
__pycache__/
```

Users should create their own folders and choose them inside the app.

## Local Build Notes

To build the console EXE locally:

```powershell
pyinstaller --onefile --clean --collect-all watchdog --name TV_Renamer tv_renamer.py
```

To build the GUI EXE locally:

```powershell
.\build_gui.ps1
```

This builds `dist\TV_Renamer_GUI.exe` and refreshes the Desktop shortcut.

To create or refresh only the GUI desktop shortcut:

```powershell
.\create_gui_desktop_shortcut.ps1
```

The GUI also includes a `Create Desktop Shortcut` button, which is the easiest option for most users.

If PyInstaller reports `PermissionError: [WinError 5] Access is denied` for a file in `dist`, close any running copy of that EXE and try again. Windows cannot replace an executable while it is still running or locked by another process.

---

## Option 2 - Run From Python Source

Requirements:

- Python 3.10+
- MakeMKV
- watchdog Python package for the console watcher

Install watchdog:

```bash
pip install watchdog
```

The GUI front end uses Python's built-in Tkinter toolkit and does not require watchdog.

---

## Anime/Split Mode Requirement

Anime/Split Mode uses MKVToolNix for splitting and automatic chapter detection.

Install MKVToolNix, then make sure this command works from a terminal:

```bash
mkvmerge --version
```

TV Renamer calls:

```text
mkvmerge.exe
```

If `mkvmerge.exe` is not available in PATH, automatic splitting and manual timestamp splitting will not work.

## Adding MKVToolNix To PATH On Windows

MKVToolNix usually installs to:

```text
C:\Program Files\MKVToolNix
```

To make `mkvmerge.exe` available to TV Renamer:

1. Press `Win`.
2. Search for `Environment Variables`.
3. Open `Edit the system environment variables`.
4. Click `Environment Variables...`.
5. Under `User variables` or `System variables`, select `Path`.
6. Click `Edit`.
7. Click `New`.
8. Add the MKVToolNix install folder:

```text
C:\Program Files\MKVToolNix
```

9. Click `OK` until all settings windows are closed.
10. Open a new PowerShell window.
11. Run:

```powershell
mkvmerge --version
```

If a version number appears, MKVToolNix is set up correctly.

If the command is not recognized, confirm that `mkvmerge.exe` exists inside the folder you added to PATH. Already-open terminals may need to be closed and reopened before they detect PATH changes.

## Optional IMDb Dataset Runtime Fallback

TV Renamer can optionally use IMDb's official non-commercial datasets as an offline fallback when an MKV has no useful chapter markers.

Download these two files from IMDb's dataset page:

```text
title.basics.tsv.gz
title.episode.tsv.gz
```

On first launch, TV Renamer can ask you to select the folder that contains those files. You can also update the folder later with the runtime command:

```text
imdb
```

Example folder layout:

```text
IMDb Datasets/
  title.basics.tsv.gz
  title.episode.tsv.gz
```

When those files are present, TV Renamer can:

- match the show name and year entered at startup
- find the selected season
- read episode runtimes
- calculate cumulative split points
- scale those split points against the actual MKV duration

After the first successful IMDb lookup for a series, TV Renamer writes a localized per-series JSON cache in:

```text
IMDb Cache/
```

Future lookups for that show and year use the cache before scanning the large compressed IMDb datasets again. The cache stores the matched series title, year, IMDb tconst, seasons, episode numbers, episode titles, and runtimes.

IMDb runtimes are usually listed in minutes, so they are best used as a smart guide rather than exact frame-accurate cut points.

IMDb dataset terms and downloads are available here:

```text
https://developer.imdb.com/non-commercial-datasets/
```

## Optional ffmpeg Refinement

If `ffmpeg.exe` is available in PATH, TV Renamer will try to refine IMDb-based and runtime-based split points by scanning near each proposed boundary for black frames or silence.

ffmpeg is optional. TV Renamer will still work without it, but split points may be less precise when chapter markers are missing.

### Installing ffmpeg On Windows

1. Download a Windows build of ffmpeg from:

```text
https://ffmpeg.org/download.html
```

2. Extract the downloaded archive.
3. Move the extracted folder somewhere permanent, for example:

```text
C:\ffmpeg
```

4. Find the `bin` folder inside it. The path usually looks like:

```text
C:\ffmpeg\bin
```

5. Add that `bin` folder to PATH:

- Press `Win`.
- Search for `Environment Variables`.
- Open `Edit the system environment variables`.
- Click `Environment Variables...`.
- Under `User variables` or `System variables`, select `Path`.
- Click `Edit`.
- Click `New`.
- Add the ffmpeg `bin` folder path.
- Click `OK` until all settings windows are closed.

To verify ffmpeg is available, open a new PowerShell window and run:

```powershell
ffmpeg -version
```

If this command works, TV Renamer will use ffmpeg automatically when it helps. If ffmpeg is missing, TV Renamer simply skips this refinement step.

If the command is not recognized, make sure `ffmpeg.exe` exists inside the folder you added to PATH, then close and reopen PowerShell.

---

# First Launch Configuration

The first time TV Renamer is launched, it opens folder selection windows.

You will be asked to select:

- your MakeMKV `Incoming` folder
- your main TV library root folder
- an optional IMDb dataset folder

Example:

```text
Incoming Folder:
C:\Users\your_username\Videos\TV_Shows\Incoming

TV Library Root:
C:\Users\your_username\Videos\TV_Shows

IMDb Dataset Folder:
D:\Metadata\IMDb Datasets
```

TV Renamer saves these locations into:

```text
config.json
```

Future launches reuse the saved configuration automatically.

---

# Recommended Folder Structure

```text
TV_Shows/
|
+-- Incoming/
|
+-- Vikings (2013)/
|   +-- Season 01/
|
+-- Breaking Bad (2008)/
    +-- Season 01/
```

Recommended setup:

- `Incoming/` is used only for fresh MakeMKV rips
- TV Renamer watches `Incoming/`
- completed files are moved into show season folders automatically
- Jellyfin or Plex scans the organized folders normally

---

# MakeMKV Setup

## 1. Enable Expert Mode

In MakeMKV:

```text
View -> Preferences
```

Then:

```text
Preferences -> General
```

Enable:

```text
Expert mode
```

This unlocks advanced filename formatting options.

---

## 2. Configure Filename Format

After enabling Expert Mode:

```text
Preferences -> Video
```

Locate:

```text
Default file name template
```

Set it to:

```text
{NAME}_t{N2}
```

Example MakeMKV output:

```text
Vikings_t00.mkv
Vikings_t01.mkv
```

TV Renamer converts those files into:

```text
Vikings - S01E01.mkv
Vikings - S01E02.mkv
```

---

## 3. Set MakeMKV Output Folder

Create a dedicated incoming folder.

Example:

```text
C:\Users\your_username\Videos\TV_Shows\Incoming
```

In MakeMKV, set the export/output folder to this location.

This folder is important because:

- MakeMKV writes files progressively while ripping
- TV Renamer monitors this folder in real time
- completed files are automatically moved into your TV library

The incoming folder acts like a processing queue.

---

## 4. Name the Disc Properly in MakeMKV

Before ripping, make sure the disc title/name in MakeMKV matches the TV show.

Example:

```text
Vikings
```

This keeps temporary MakeMKV filenames readable:

```text
Vikings_t00.mkv
```

instead of:

```text
DISC_1_t00.mkv
```

---

# How TV Renamer Works

1. Insert a disc into MakeMKV.
2. Select only actual episode titles.
3. Export `.mkv` files into `Incoming/`.
4. TV Renamer detects new files.
5. TV Renamer waits until ripping finishes.
6. The next episode number is determined automatically.
7. Files are renamed and moved into the correct season folder.

Example final structure:

```text
Vikings (2013)/
  Season 01/
    Vikings - S01E01.mkv
    Vikings - S01E02.mkv
```

---

# Anime/Split Mode

Anime/Split Mode is designed for discs where MakeMKV creates one long MKV containing multiple episodes.

When Anime/Split Mode is enabled, TV Renamer will:

1. Detect a completed MKV file.
2. Read MKV metadata using `mkvmerge -J`.
3. Estimate the number of episodes from the total runtime.
4. Look for chapter markers near expected episode boundaries.
5. Use chapter split points when they are available.
6. If chapters are missing, try local IMDb episode runtimes.
7. If IMDb data is unavailable, fall back to evenly spaced runtime splits.
8. Optionally refine fallback split points with ffmpeg.
9. Show the proposed split timestamps.
10. In the GUI, allow timeline adjustment and optional ffmpeg frame preview around split boundaries.
11. Ask for confirmation before splitting.
12. Rename and move each split episode sequentially.

Example:

```text
Automatic split points found:
00:24:10.000, 00:48:22.000

Split automatically using these timestamps? (y/n):
```

Those split points create:

```text
Episode 1 = 00:00:00 -> 00:24:10
Episode 2 = 00:24:10 -> 00:48:22
Episode 3 = 00:48:22 -> end
```

If automatic detection is unavailable, TV Renamer can still ask for manual split timestamps.

In the GUI split editor, `Load Frame Preview` uses `ffmpeg.exe` to show still frames shortly before, at, and shortly after the selected split boundary. This is optional and only works when ffmpeg is available in PATH.

IMDb fallback keeps episodes in season order and scales listed runtimes against the actual MKV duration:

```text
IMDb runtimes:
S01E01 = 24 min
S01E02 = 24 min
S01E03 = 23 min

Actual MKV duration:
01:12:40

Proposed split points:
00:24:33
00:49:06
```

Runtime fallback keeps episodes in playback order and creates continuous segments:

```text
Episode 1 = 00:00:00 -> first split point
Episode 2 = first split point -> second split point
Episode 3 = second split point -> end
```

Manual timestamp example:

```text
00:24:10,00:48:22
```

## Optional AI Runtime Check

TV Renamer does not scrape IMDb, TMDB, AniDB, or other metadata sites. This keeps the app simple, offline-friendly, and focused on deterministic file handling.

If you do not want to download the IMDb datasets, you can still ask an AI assistant such as ChatGPT to summarize episode runtimes from IMDb or another episode guide site.

This can be useful for double-checking TV Renamer's proposed split points before confirming a split.

Use this as a starting prompt:

```text
Look up the episode runtimes for [SERIES NAME] Season [X] using reliable episode and home media sources such as IMDb, TVDB, Blu-ray.com, DVD release listings, official distributor information, or verified runtime databases.

 Before generating the runtime list, first ask what media source/version the user is working with. Examples include:

 * uncut DVD box set
 * Blu-ray release
 * broadcast TV recordings
 * streaming version
 * digitally purchased episodes
 * downloaded media files
 * remastered releases
 * fan-restored versions
 * region-specific releases

 Runtime accuracy and split points should be tailored specifically to that media source whenever possible.

 Do not assume every episode is exactly the same length, and do not rely solely on generic streaming metadata.

 When determining runtimes and split points, take into account:

 * original DVD/Blu-ray disc structure
 * episodes-per-disc authoring patterns
 * actual physical media layouts
 * opening/ending variations
 * recap episodes
 * double-length or extended episodes
 * previews and bonus segments
 * practical disc runtime limits
 * differences between broadcast, streaming, and physical releases

 Prioritize the specified media version over generalized episode guides when conflicts exist.

 Return episodes only in season order.

 For each episode include:

 * episode number
 * title (if available)
 * listed or estimated runtime
 * cumulative split point
 * disc grouping when known or inferable

 Example format:

 Disc 1
 S01E01 - Episode Title - 24 min - split after 00:24:00
 S01E02 - Episode Title - 24 min - split after 00:48:00

 Disc 2
 S01E05 - Episode Title - 23 min - split after 01:59:00

 If sources disagree, briefly explain why (broadcast edit, streaming cut, DVD authoring differences, remaster timing changes, etc.).

 Do not include plot summaries.

```

Example output format to ask for:

```text
S01E01 - 24 min - split after 00:24:00
S01E02 - 24 min - split after 00:48:00
S01E03 - 23 min - split after 01:11:00
```

Those cumulative split points can be compared against TV Renamer's proposed timestamps. For discs that include intros, recaps, previews, or credits inside each episode, the MKV runtime may differ slightly from online listings, so use the AI output as a sanity check rather than an exact cutting authority.

---

# Usage

## Running The Windows EXE

Download and extract the GUI release zip, then run:

```text
TV_Renamer_GUI.exe
```

The GUI will ask you to choose folders and enter show/session details.

If you downloaded the console build instead, run:

```text
TV_Renamer.exe
```

The console version prompts for setup in the terminal.

---

## Running From Python Source

Navigate to the project folder:

```bash
cd "C:\Users\your_username\path_to_TV_Renamer"
```

Then run:

```bash
python tv_renamer.py
```

If `python` does not work on your system, try:

```bash
py tv_renamer.py
```

To run the desktop GUI from source:

```bash
python tv_renamer_gui.py
```

or:

```bash
py tv_renamer_gui.py
```

The GUI currently provides session setup, folder selection, timer-based incoming-folder watching, queued processing, live logs, and split confirmation dialogs with a draggable split timeline, optional ffmpeg still-frame previews, and an episode/start/end table. Richer video playback or waveform-style preview controls are still planned for a later GUI phase.

Example startup:

```text
Show name: Vikings
Year: 2013
Season number: 1

Rip Modes
------------------------------
1. Standard TV
2. Anime / Split Mode

Select mode:
```

TV Renamer then:

1. scans the existing season folder
2. detects the highest episode already present
3. determines the next episode number
4. watches the incoming folder
5. waits for completed MKV files
6. renames and moves episodes automatically

---

# Interactive Runtime Commands

While TV Renamer is running, the following commands are available:

```text
s       = Change season
n       = Change show
mode    = Change rip mode
status  = Show current status
config  = Reconfigure folders
imdb    = Set IMDb dataset folder
help    = Show commands
q       = Quit
```

This allows continuous ripping sessions without restarting the application.

---

# Privacy And Security

TV Renamer is designed to run locally.

The app does not:

- upload video files
- send show names to an online service
- scrape live web pages
- call IMDb, TMDB, AniDB, or Sonarr APIs
- include telemetry or analytics

The optional IMDb fallback reads only local `.tsv.gz` dataset files that you choose. The optional ffmpeg refinement analyzes only the MKV file being processed.

External tools are launched without a shell, using explicit argument lists. This avoids shell command interpolation and keeps filenames from being treated as commands.

TV Renamer only writes to:

- the configured TV library destination
- temporary split folders created by the operating system
- `config.json`

Temporary split files are moved into the destination folder after successful splitting. TV Renamer does not intentionally retain duplicate temporary episode files.

Security recommendations:

- download MKVToolNix and ffmpeg from trusted sources
- keep `config.json` private because it contains local folder paths
- do not commit IMDb datasets or personal library paths to GitHub
- verify proposed split timestamps before confirming automatic splitting

---

# Example Standard TV Workflow

## Existing Library

```text
Vikings (2013)/
  Season 01/
    Vikings - S01E01.mkv
    Vikings - S01E02.mkv
```

## New Disc Rip

MakeMKV creates:

```text
Incoming/
  Vikings_t00.mkv
  Vikings_t01.mkv
```

TV Renamer converts them into:

```text
Vikings (2013)/
  Season 01/
    Vikings - S01E03.mkv
    Vikings - S01E04.mkv
```

---

# Example Anime Split Workflow

MakeMKV creates one long file:

```text
Incoming/
  ExampleAnime_t10.mkv
```

TV Renamer detects chapter-based split points and creates:

```text
Example Anime (2024)/
  Season 01/
    Example Anime - S01E01.mkv
    Example Anime - S01E02.mkv
    Example Anime - S01E03.mkv
```

---

# Philosophy

Most TV ripping workflows overcomplicate episode handling with:

- metadata scraping
- API lookups
- duration matching
- title fingerprinting
- external databases
- import queues

TV Renamer intentionally avoids those systems.

The workflow already contains the necessary intelligence:

- the user selects the correct episode titles
- episodes are ripped sequentially
- filesystem state determines the next episode number
- chapter markers can identify split points for many anime discs

This makes the workflow deterministic, lightweight, and reliable.

---

# Architecture

TV Renamer is being refactored toward a backend-first design so the current console workflow and a future desktop GUI can share the same processing logic.

See [ARCHITECTURE.md](ARCHITECTURE.md) for the current direction.

See [DESIGN_PHILOSOPHY.md](DESIGN_PHILOSOPHY.md) for the project philosophy around deterministic, offline-first physical-media workflows.

Roadmap and community issue drafts are available in [.github/ISSUE_DRAFTS](.github/ISSUE_DRAFTS).

---

# License

Apache License 2.0

See [LICENSE.md](LICENSE.md) for details.
