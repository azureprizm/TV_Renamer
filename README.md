# TV_Renamer

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

---

# First Launch Configuration

The first time TV Renamer is launched, it opens folder selection windows.

You will be asked to select:

- your MakeMKV `Incoming` folder
- your main TV library root folder

Example:

```text
Incoming Folder:
C:\Users\your_username\Videos\TV_Shows\Incoming

TV Library Root:
C:\Users\your_username\Videos\TV_Shows
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
5. Show the proposed split timestamps.
6. Ask for confirmation before splitting.
7. Rename and move each split episode sequentially.

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

Manual timestamp example:

```text
00:24:10,00:48:22
```

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
