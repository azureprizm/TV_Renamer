# TV Renamer v1.2.0

TV Renamer v1.2.0 adds Anime/Split Mode support for long MKV files, including automatic chapter-based split detection powered by MKVToolNix.

This release is focused on physical-media anime workflows where a disc may rip as one long MKV containing multiple episodes.

---

# What's New

## Desktop GUI

TV Renamer now includes a desktop GUI build:

```text
TV_Renamer_GUI.exe
```

For release downloads, extract the GUI zip first, then run the EXE. The GUI lets users choose incoming/library folders, enter show/session details, start or stop watching, view logs, process queued files, confirm split points, and create a Desktop shortcut from inside the app.

Recommended GUI release zip contents:

```text
TV_Renamer_GUI.exe
README.md
LICENSE.md
RELEASE_NOTES_v1.2.0.md
tv_renamer.ico
create_gui_desktop_shortcut.ps1
```

User-specific files such as `config.json`, `IMDb Datasets/`, and `IMDb Cache/` are not bundled. Users create or choose their own folders after launching the app.

## Anime/Split Mode

TV Renamer now includes an Anime/Split Mode at startup and through the runtime `mode` command.

When enabled, TV Renamer can process long MKV files that contain multiple episodes instead of treating every MKV as a single episode.

## Automatic Chapter-Based Split Detection

For long anime MKV files, TV Renamer now attempts to:

- read MKV metadata using `mkvmerge -J`
- estimate the expected episode count from total runtime
- find chapter markers near expected episode boundaries
- propose split timestamps automatically
- ask for confirmation before splitting

Example:

```text
Automatic split points found:
00:24:10.000, 00:48:22.000

Split automatically using these timestamps? (y/n):
```

## Runtime-Based Split Fallback

If an MKV has no chapter markers, or the chapter markers do not line up with expected episode boundaries, TV Renamer now falls back to evenly spaced runtime splitting.

This keeps output episodes in playback order and avoids manual timestamp entry for many no-chapter anime rips.

## Local IMDb Dataset Runtime Fallback

TV Renamer can optionally use IMDb's official non-commercial datasets when chapter markers are unavailable.

If `title.basics.tsv.gz` and `title.episode.tsv.gz` are available in the configured IMDb dataset folder, TV Renamer can match the show name, year, season, and next episode number entered by the user, then calculate runtime-weighted split points from IMDb episode runtimes.

The calculated split points are scaled against the actual MKV duration rather than copied directly from IMDb minute values.

## Optional ffmpeg Split Refinement

If `ffmpeg.exe` is available in PATH, TV Renamer will scan near IMDb-based and runtime-based split points for black frames or silence and use the closest reasonable boundary.

If ffmpeg is not installed, this refinement step is skipped automatically.

## Manual Timestamp Fallback

If automatic detection is unavailable, TV Renamer can still split files using manually entered timestamps.

Example:

```text
00:24:10,00:48:22
```

## MKVToolNix Integration

TV Renamer now uses `mkvmerge.exe` for:

- reading MKV metadata
- detecting chapters
- splitting MKV files safely

Users who want Anime/Split Mode should install MKVToolNix and make sure `mkvmerge.exe` is available in PATH.

---

# Improvements

- Added startup mode selection for Standard TV vs Anime/Split Mode.
- Added runtime `mode` command for switching modes without restarting.
- Added automatic MakeMKV title number detection from filenames like `_t10`.
- Added long-title hints for likely multi-episode anime MKV files.
- Added optional IMDb dataset lookup for offline episode runtimes.
- Added per-series IMDb JSON cache files so repeated runtime fallback lookups do not keep rescanning the compressed IMDb datasets.
- Added first-launch IMDb dataset folder selection.
- Added runtime `imdb` command for changing the IMDb dataset folder.
- Added proportional split calculation based on the actual MKV duration.
- Added optional ffmpeg black-frame/silence refinement.
- Added runtime-based automatic splitting when chapter markers are unavailable.
- Added visible progress updates during file stability checks, IMDb dataset scans, and ffmpeg refinement.
- Added initial `tv_renamer_gui.py` desktop GUI for session setup, folder watching, queued processing, logs, and split confirmation dialogs.
- Added `TV_Renamer_GUI.spec` for building the GUI as a separate windowed EXE.
- Added `build_gui.ps1` to build the GUI EXE and refresh the Desktop shortcut in one command.
- Added `create_gui_desktop_shortcut.ps1` for creating a Desktop shortcut to the GUI EXE.
- Added a GUI button for creating the Desktop shortcut without running a script manually.
- Increased file stability detection from 30 seconds to 60 seconds to better handle slower disc rips.
- Fixed the `q` command so it shuts down the watcher and exits the app instead of only stopping the command thread.
- Added clearer `ACTION REQUIRED` prompts before split confirmation.
- Tightened external tool launching by resolving MKVToolNix and ffmpeg from PATH before execution.
- Removed import-time CLI prompts so backend functions can be imported by future GUI code.
- Added initial `tvrenamer` backend package.
- Moved config file load/save helpers into `tvrenamer.config`.
- Added `tvrenamer.imdb_cache` for cache-first per-series IMDb runtime lookup.
- Moved raw IMDb TSV parsing into `tvrenamer.imdb_dataset`.
- Moved episode naming and next-episode detection helpers into `tvrenamer.naming`.
- Moved duration parsing and MKV chapter/duration extraction helpers into `tvrenamer.media_metadata`.
- Moved weighted split-point math into `tvrenamer.split_math`.
- Added initial architecture notes for a backend-first GUI transition.
- Added safer split confirmation before creating episode files.
- Preserved existing sequential episode numbering after split operations.

---

# Notes

Automatic anime splitting works best when the MKV contains chapter markers at or near episode boundaries.

If a disc has missing, unusual, or poorly placed chapters, TV Renamer will use runtime-based split points and ask for confirmation before cutting.

IMDb dataset support requires local copies of `title.basics.tsv.gz` and `title.episode.tsv.gz`. These datasets are not bundled with TV Renamer. Users can choose the dataset folder during setup or change it later with the `imdb` command.

---

# Requirements

Standard TV mode:

- MakeMKV
- TV Renamer

Anime/Split Mode:

- MakeMKV
- TV Renamer
- MKVToolNix with `mkvmerge.exe` available in PATH

Optional Anime/Split Mode enhancements:

- IMDb non-commercial datasets in the configured IMDb dataset folder
- ffmpeg with `ffmpeg.exe` available in PATH

Python source users also need:

- Python 3.10+
- watchdog

---

# Compatibility

This release continues to support:

- Windows
- MakeMKV physical-media workflows
- Jellyfin-compatible naming
- Plex-compatible naming
- multi-disc sequential episode organization
- standalone EXE usage
- Python source usage

---

# Upgrade Notes

Existing `config.json` files remain compatible.

No library migration is required. Existing renamed episodes are still used to determine the next episode number automatically.
