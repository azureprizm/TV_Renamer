# ============================================================
# TV_Renamer
#
# Copyright (c) 2026 Joshua Holmes
#
# MIT License
#
# Permission is hereby granted, free of charge, to any
# person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the
# Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the
# Software, subject to the following conditions:
#
# The above copyright notice and this permission notice
# shall be included in all copies or substantial portions
# of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED.
# ============================================================

# tv_renamer.py
#
# Requirements:
#   pip install watchdog
#
# Workflow:
#
#   1. Start script
#   2. Enter:
#        - show name
#        - year
#        - season
#
#   3. Script scans existing Jellyfin season folder
#      and automatically determines next episode number
#
#   4. MakeMKV rips into:
#        D:\Rips\Incoming
#
#   5. Script watches for completed MKVs,
#      renames sequentially,
#      and moves directly into Jellyfin library
#
# Example final output:
#
#   D:\TV Shows\Vikings (2013)\Season 01\
#       Vikings - S01E01.mkv
#       Vikings - S01E02.mkv

import re
import shutil
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


# ============================================================
# CONFIG
# ============================================================

INCOMING_DIR = Path(r"C:\User\your_username\Videos\TV_Shows\Incoming")
TV_ROOT = Path(r"C:\User\you_username\Videos\TV_Shows")

# How long file size must remain unchanged
STABLE_TIME = 30

# Poll interval while checking rip completion
POLL_INTERVAL = 2


# ============================================================
# USER INPUT
# ============================================================

show_name = input("Show name: ").strip()
year = input("Year: ").strip()
season = int(input("Season number: ").strip())


# ============================================================
# PATH SETUP
# ============================================================

show_folder = f"{show_name} ({year})"
season_folder = f"Season {season:02d}"

DESTINATION_DIR = (
    TV_ROOT
    / show_folder
    / season_folder
)

DESTINATION_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# DETERMINE NEXT EPISODE
# ============================================================

EPISODE_PATTERN = re.compile(
    rf"S{season:02d}E(\d+)",
    re.IGNORECASE
)

existing_episodes = []

for file in DESTINATION_DIR.glob("*.mkv"):
    match = EPISODE_PATTERN.search(file.name)

    if match:
        existing_episodes.append(int(match.group(1)))

if existing_episodes:
    next_episode = max(existing_episodes) + 1
else:
    next_episode = 1


# ============================================================
# HELPERS
# ============================================================

def build_episode_filename(ep_num):
    return (
        f"{show_name} - "
        f"S{season:02d}"
        f"E{ep_num:02d}.mkv"
    )


def wait_for_file_complete(file_path):
    """
    Wait until file size stops changing.
    """

    stable_for = 0
    last_size = -1

    while stable_for < STABLE_TIME:
        try:
            current_size = file_path.stat().st_size
        except FileNotFoundError:
            return False

        if current_size == last_size:
            stable_for += POLL_INTERVAL
        else:
            stable_for = 0
            last_size = current_size

        time.sleep(POLL_INTERVAL)

    return True


# ============================================================
# FILE PROCESSING
# ============================================================

def process_file(file_path):
    global next_episode

    print(f"\nDetected: {file_path.name}")

    print("Waiting for rip to finish...")
    complete = wait_for_file_complete(file_path)

    if not complete:
        print("File disappeared.")
        return

    new_name = build_episode_filename(next_episode)

    destination = DESTINATION_DIR / new_name

    if destination.exists():
        print(f"ERROR: File already exists:\n{destination}")
        return

    print(f"Moving to:\n{destination}")

    shutil.move(str(file_path), str(destination))

    print(f"Created: {new_name}")

    next_episode += 1


# ============================================================
# WATCHDOG HANDLER
# ============================================================

class MKVHandler(FileSystemEventHandler):

    def on_created(self, event):
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        if file_path.suffix.lower() != ".mkv":
            return

        # Small delay so MakeMKV fully creates file
        time.sleep(2)

        process_file(file_path)


# ============================================================
# MAIN
# ============================================================

def main():

    if not INCOMING_DIR.exists():
        print(f"Incoming folder missing:\n{INCOMING_DIR}")
        return

    print("\n" + "=" * 60)
    print("TV RENAMER RUNNING")
    print("=" * 60)

    print(f"Show: {show_name}")
    print(f"Season: {season:02d}")
    print(f"Next episode: {next_episode:02d}")
    print(f"Watching: {INCOMING_DIR}")
    print(f"Destination: {DESTINATION_DIR}")

    print("=" * 60 + "\n")

    event_handler = MKVHandler()

    observer = Observer()
    observer.schedule(
        event_handler,
        str(INCOMING_DIR),
        recursive=False
    )

    observer.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    main()