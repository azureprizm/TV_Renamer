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
![GitHub stars](https://img.shields.io/github/stars/azureprizm/TV_Renamer)
![GitHub issues](https://img.shields.io/github/issues/azureprizm/TV_Renamer)

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
- Folder reconfiguration command
- Windows standalone EXE support
- Anime/Split Mode for long MKV files
- Automatic chapter-based anime split detection
- Optional local IMDb dataset runtime fallback
- Optional ffmpeg black-frame/silence refinement
- Runtime-based anime split fallback when chapter markers are missing
- Manual timestamp splitting fallback
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

Then run:

```text
TV_Renamer.exe
```

This is the simplest setup method for most users.

---

## Option 2 - Run From Python Source

Requirements:

- Python 3.10+
- MakeMKV
- watchdog Python package

Install watchdog:

```bash
pip install watchdog
```

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

IMDb runtimes are usually listed in minutes, so they are best used as a smart guide rather than exact frame-accurate cut points.

IMDb dataset terms and downloads are available here:

```text
https://developer.imdb.com/non-commercial-datasets/
```

## Optional ffmpeg Refinement

If `ffmpeg.exe` is available in PATH, TV Renamer will try to refine IMDb-based and runtime-based split points by scanning near each proposed boundary for black frames or silence.

To verify ffmpeg is available, open a new PowerShell window and run:

```powershell
ffmpeg -version
```

If this command works, TV Renamer will use ffmpeg automatically when it helps. If ffmpeg is missing, TV Renamer simply skips this refinement step.

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
10. Ask for confirmation before splitting.
11. Rename and move each split episode sequentially.

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
Look up the episode runtimes for [SHOW NAME], season [SEASON NUMBER].
Use IMDb or another reliable episode guide if IMDb is incomplete.
Return only the episodes in season order.
Include each episode number, title if available, listed runtime, and cumulative split point.
If sources disagree, mention the difference briefly.
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

Download:

```text
TV_Renamer.exe
```

Then double-click the executable.

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

# License

Apache License 2.0

See [LICENSE.md](LICENSE.md) for details.
