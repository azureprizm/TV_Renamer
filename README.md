# TV Renamer

A lightweight automated TV episode renamer and Jellyfin organizer designed specifically for physical media TV ripping workflows using MakeMKV.

TV Renamer watches a dedicated MakeMKV output folder, waits for completed `.mkv` files, then automatically:

- determines the next episode number
- renames episodes sequentially
- moves files into a Jellyfin-compatible folder structure
- preserves numbering across multiple discs

---

# Why This Exists

Most media automation tools were built around downloaded media files, not physical DVD/Blu-ray box sets.

Traditional TV ripping workflows often require:

- manual renaming
- drag/drop sorting
- FileBot passes
- metadata matching
- Sonarr imports
- temporary staging folders

TV Renamer simplifies the workflow by assuming:

```text
rip order == episode order
```

If you manually select only valid episode titles in MakeMKV and rip them sequentially, then episode numbering becomes deterministic.

No metadata scraping is required.

---

# Features

- Automatic sequential episode numbering
- Multi-disc support
- Jellyfin-compatible naming
- Real-time folder monitoring
- Automatic next-episode detection
- File completion/stability detection
- No metadata scraping
- No TMDB dependency
- No Sonarr required
- No paid software required

---

# Requirements

- Python 3.10+
- MakeMKV
- watchdog Python package

Install watchdog:

```bash
pip install watchdog
```

---

# Recommended Folder Structure

```text
DVD Backups/
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

- `Incoming/` is used only for fresh MakeMKV rips
- TV Renamer watches `Incoming/`
- Completed files are moved into show season folders automatically
- Jellyfin scans the organized folders normally

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
C:\Users\your_username\Videos\DVD Backups\Incoming
```

In MakeMKV, set the export/output folder to this location.

This folder is important because:

- MakeMKV writes files progressively while ripping
- TV Renamer monitors this folder in real time
- completed files are automatically moved into your Jellyfin library

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

Run:

```bash
cd "C:\Users\your_username\file_path_for_tv_renamer.py_file"
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

1. Scans the existing season folder
2. Detects the highest episode already present
3. Determines the next episode number
4. Watches the incoming folder
5. Waits for completed MKV files
6. Renames and moves episodes automatically

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

- metadata scraping
- API lookups
- duration matching
- title fingerprinting
- external databases

TV Renamer intentionally avoids these systems.

The workflow already contains the necessary intelligence:

- the user manually selects correct episode titles
- episodes are ripped sequentially
- filesystem state determines the next episode number

This makes the workflow deterministic, lightweight, and reliable.

---

# License

MIT License

See LICENSE file for details.
