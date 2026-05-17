# TV Renamer Architecture

TV Renamer is moving toward a backend-first design so the same media processing logic can support both the current console workflow and a future desktop GUI.

## Current Direction

The console app should remain a thin interface over reusable backend behavior.

```text
CLI or GUI
  -> application/session controller
  -> media processing functions
  -> external tools and filesystem
```

The important rule is that media logic should not depend on `input()` or terminal-only behavior.

## First Refactor Step

`tv_renamer.py` no longer starts the interactive workflow at import time.

This means future code can import backend functions such as:

- `detect_anime_split_timestamps()`
- `split_mkv_by_timestamps()`
- `refine_split_points_with_ffmpeg()`
- `get_imdb_episode_runtimes()`

without immediately prompting for show name, season, or mode.

The console workflow now starts through:

```python
main()
```

which calls:

```python
initialize_cli_session()
```

## Planned Module Boundaries

Future cleanup should split the current script into focused modules:

```text
tvrenamer/
  config.py
  imdb_cache.py
  imdb_dataset.py
  media_metadata.py
  naming.py
  split_math.py
  models.py
  media_tools.py
  split_detection.py
  processor.py
  cli.py
```

Suggested ownership:

- `config.py`: config data structure plus load/save helpers. This module now exists. CLI folder selection still lives in `tv_renamer.py`.
- `models.py`: show/session/file processing data structures
- `naming.py`: episode filename, destination folder, and next-episode logic. This module now exists.
- `imdb_cache.py`: per-series JSON cache for IMDb lookup results. This module now exists.
- `imdb_dataset.py`: local IMDb TSV parsing and runtime lookup. This module now exists.
- `media_metadata.py`: duration parsing and chapter/duration extraction from MKV metadata. This module now exists.
- `split_math.py`: split point calculations such as runtime-weighted IMDb fallback. This module now exists.
- `media_tools.py`: `mkvmerge` and `ffmpeg` wrappers
- `split_detection.py`: chapters, IMDb runtime fallback, runtime fallback, refinement
- `processor.py`: file stability, queue processing, move/split orchestration
- `cli.py`: prompts, commands, and terminal output

## GUI Path

The first GUI front end now lives in:

```text
tv_renamer_gui.py
```

It is a dependency-free Tkinter desktop window for session setup, folder selection, timer-based incoming-folder watching, queued processing, live logs, and split confirmation dialogs.

Future GUI work should continue moving behavior into backend modules so the window calls backend functions through a controller instead of duplicating processing logic.

Useful GUI surfaces:

- richer configuration window
- current show/season/status panel
- visible incoming file queue
- processing log
- split confirmation dialog
- split preview timeline

The split preview timeline is the long-term killer feature. It can show:

- chapter markers
- IMDb/runtime predicted split points
- black-frame markers
- silence markers
- draggable final split boundaries

## Compatibility Goal

The CLI should keep working while the GUI is developed.

This keeps TV Renamer usable during the transition and gives the backend an easy test harness.

## Current Backend Modules

The first backend package modules are:

```text
tvrenamer/
  __init__.py
  config.py
  imdb_cache.py
  imdb_dataset.py
  media_metadata.py
  naming.py
  split_math.py
```

`tv_renamer.py` still owns the console workflow, folder picker prompts, watcher, and file-processing orchestration, but no longer contains config file serialization, the raw IMDb TSV parser, IMDb series cache handling, split-point math, naming helpers, or MKV metadata parsing helpers.

## IMDb Cache

IMDb fallback now uses a cache-first flow:

```text
show/year lookup
  -> per-series JSON cache
  -> IMDb .tsv.gz scan only on cache miss
  -> cache write after successful series extraction
```

The cache stores localized series data rather than gzip row numbers or byte offsets. This keeps the cache resilient when IMDb publishes updated dataset files and leaves room for a later SQLite backend.
