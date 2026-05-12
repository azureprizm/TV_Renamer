# TV Renamer

A lightweight automated TV episode renamer and Jellyfin organizer designed specifically for physical media TV ripping workflows using MakeMKV.

TV Renamer watches a dedicated MakeMKV output folder, waits for completed `.mkv` files, then automatically:

* determines the next episode number
* renames episodes sequentially
* moves files into a Jellyfin-compatible folder structure
* preserves numbering across multiple discs

---

# Why This Exists

Most media automation tools were built around downloaded media files, not physical DVD/Blu-ray box sets.

Traditional TV ripping workflows often require:

* manual renaming
* drag/drop sorting
* FileBot passes
* metadata matching
* Sonarr imports
* temporary staging folders

TV Renamer simplifies the workflow by assuming:

```text
rip order == episode order
```

If you manually select only valid episode titles in MakeMKV and rip them sequentially, then episode numbering becomes deterministic.

No metadata scraping is required.

---

# Features

* Automatic sequential episode numbering
* Multi-disc support
* Jellyfin-compatible naming
* Plex-compatible naming
* Real-time folder monitoring
* Automatic next-episode detection
* File completion/stability detection
* Interactive season switching
* Interactive show switching
* Live status commands
* Windows standalone EXE support
* No metadata scraping
* No TMDB dependency
* No Sonarr required
* No paid software required

---

# Requirements

TV Renamer now supports two installation methods:

---

## Option 1 — Windows EXE (Recommended)

No Python installation required.

Download the latest release from:

```text
GitHub → Releases
```

Then run:

```text
TV_Renamer.exe
```

This is the simplest setup method for most users.

---

## Option 2 — Run From Python Source

Requirements:

* Python 3.10+
* MakeMKV
* watchdog Python package

Install watchdog:

````bash
pip install watchdog
````

---
## First Launch Configuration

The first time TV Renamer is launched, it will open folder selection windows.

You will be asked to select:

* your MakeMKV `Incoming` folder
* your main TV library root folder

Example:

```text
Incoming Folder:
C:\Users\your_username\Videos\TV_Shows\Incoming

TV Library Root:
C:\Users\your_username\Videos\TV_Shows
```

TV Renamer automatically saves these locations into:

```text
config.json
```

Future launches will reuse the saved configuration automatically.
---

# Recommended Folder Structure

```text
TV_Shows/
│
├── Incoming/
│
├── Vikings (2013)/
│   └── Season 01/
│
└── Breaking Bad (2008)/
    └── Season 01/
```

Recommended setup:

* `Incoming/` is used only for fresh MakeMKV rips
* TV Renamer watches `Incoming/`
* Completed files are moved into show season folders automatically
* Jellyfin scans the organized folders normally

---

# MakeMKV Setup

## 1. Enable Expert Mode

In MakeMKV:

```text
View → Preferences
```

Then:

```text
Preferences → General
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
Preferences → Video
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

TV Renamer will later convert these into:

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

* MakeMKV writes files progressively while ripping
* TV Renamer monitors this folder in real time
* completed files are automatically moved into your Jellyfin library

The incoming folder acts like a processing queue.

---

## 4. Name the Disc Properly in MakeMKV

Before ripping, make sure the disc title/name in MakeMKV matches the TV show.

Example:

```text
Vikings
```

This ensures temporary MakeMKV filenames remain clean and readable.

Example:

```text
Vikings_t00.mkv
```

instead of:

```text
DISC_1_t00.mkv
```

---

# How TV Renamer Works

1. You insert a disc into MakeMKV
2. You select only actual episode titles
3. MakeMKV exports `.mkv` files into `Incoming/`
4. TV Renamer detects new files
5. TV Renamer waits until ripping finishes
6. The next episode number is determined automatically
7. Files are renamed and moved into Jellyfin folders

Example final structure:

```text
Vikings (2013)/
  Season 01/
    Vikings - S01E01.mkv
    Vikings - S01E02.mkv
```

---

# Usage

## Running The Windows EXE

Download:

```text
TV_Renamer.exe
```

Then simply double-click the executable.

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
```

TV Renamer automatically:

1. Scans the existing season folder as long as you directed the 
2. Detects the highest episode already present
3. Determines the next episode number
4. Watches the incoming folder
5. Waits for completed MKV files
6. Renames and moves episodes automatically

---

# Interactive Runtime Commands

While TV Renamer is running, the following commands are available:

```text
s       = Change season
n       = New show
status  = Show current status
help    = Show commands
q       = Quit
```

This allows continuous ripping sessions without restarting the application.

---

# Example Workflow

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

TV Renamer automatically converts them into:

```text
Vikings (2013)/
  Season 01/
    Vikings - S01E03.mkv
    Vikings - S01E04.mkv
```

---

# Philosophy

Most TV ripping workflows overcomplicate episode handling using:

* metadata scraping
* API lookups
* duration matching
* title fingerprinting
* external databases

TV Renamer intentionally avoids these systems.

The workflow already contains the necessary intelligence:

* the user manually selects correct episode titles
* episodes are ripped sequentially
* filesystem state determines the next episode number

This makes the workflow deterministic, lightweight, and reliable.

---

# License

MIT License

See LICENSE file for details.



---

## LICENSE

```text
Apache License
Version 2.0, January 2004
http://www.apache.org/licenses/

Copyright 2026 Joshua Holmes 

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

See the License for the specific language governing permissions and
limitations under the License.
````

---
