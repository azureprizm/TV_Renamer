# ============================================================
# TV_Renamer
#
# Copyright (c) 2026 Joshua Holmes
#
# Licensed under the Apache License, Version 2.0
# you may not use this file except in compliance
# with the License.
#
# You may obtain a copy of the License at:
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to
# in writing, software distributed under the
# License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND.
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
import json
import threading
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


# ============================================================
# CONFIG
# ============================================================

CONFIG_FILE = Path("config.json")

# How long file size must remain unchanged
STABLE_TIME = 30

# Poll interval while checking rip completion
POLL_INTERVAL = 2


def create_config():

    from tkinter import Tk
    from tkinter.filedialog import askdirectory

    print("\nFIRST TIME SETUP")
    print("-" * 40)

    root = Tk()
    root.withdraw()

    print("\nSelect Incoming MKV folder...")

    incoming = askdirectory(
        title="Select Incoming MKV Folder"
    )

    if not incoming:

        print("No folder selected.")
        quit()

    print("\nSelect TV library root folder...")

    tv_root = askdirectory(
        title="Select TV Library Root Folder"
    )

    if not tv_root:

        print("No folder selected.")
        quit()

    incoming_path = Path(incoming)
    tv_root_path = Path(tv_root)

    incoming_path.mkdir(
        parents=True,
        exist_ok=True
    )

    tv_root_path.mkdir(
        parents=True,
        exist_ok=True
    )

    config_data = {
        "incoming_dir": str(incoming_path),
        "tv_root": str(tv_root_path)
    }

    with open(CONFIG_FILE, "w") as f:

        json.dump(config_data, f, indent=4)

    print("\nConfiguration saved.\n")


def load_config():

    global INCOMING_DIR
    global TV_ROOT

    if not CONFIG_FILE.exists():

        create_config()

    with open(CONFIG_FILE, "r") as f:

        config = json.load(f)

    INCOMING_DIR = Path(
        config["incoming_dir"]
    )

    TV_ROOT = Path(
        config["tv_root"]
    )


load_config()


# ============================================================
# USER INPUT
# ============================================================

show_name = input("Show name: ").strip()
year = input("Year: ").strip()
season = int(input("Season number: ").strip())

print("\nRip Modes")
print("-" * 30)
print("1. Standard TV")
print("2. Anime / Multi-Episode")

mode_choice = input(
    "\nSelect mode: "
).strip()

if mode_choice == "2":

    rip_mode = "anime"

else:

    rip_mode = "standard"


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


def build_multi_episode_filename(
    start_ep,
    end_ep
):

    return (
        f"{show_name} - "
        f"S{season:02d}"
        f"E{start_ep:02d}"
        f"-E{end_ep:02d}.mkv"
    )


# ============================================================
# NEW ADDITION
# MKV TITLE DETECTION
# ============================================================

TITLE_PATTERN = re.compile(
    r"_t(\d+)",
    re.IGNORECASE
)


def extract_title_number(file_name):

    match = TITLE_PATTERN.search(
        file_name
    )

    if not match:

        return None

    return int(match.group(1))


def is_probable_multi_episode(
    title_number
):

    if title_number is None:

        return False

    return title_number >= 10


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

    complete = wait_for_file_complete(
        file_path
    )

    if not complete:

        print("File disappeared.")
        return

    # ====================================================
    # NEW ADDITION
    # TITLE NUMBER ANALYSIS
    # ====================================================

    detected_title = extract_title_number(
        file_path.name
    )

    if detected_title is not None:

        print(
            f"Detected MakeMKV title: "
            f"t{detected_title:02d}"
        )

    # ====================================================
    # ANIME MODE
    # ====================================================

    if rip_mode == "anime":

        print("\nAnime mode enabled.")

        # ================================================
        # NEW ADDITION
        # SMART SUGGESTION
        # ================================================

        suggested_count = 1

        if is_probable_multi_episode(
            detected_title
        ):

            suggested_count = 2

            print(
                "\nPossible multi-episode file "
                "detected."
            )

            print(
                "Suggested episode count: 2"
            )

        while True:

            try:

                user_input = input(
                    "Episodes contained in this MKV "
                    f"[{suggested_count}]: "
                ).strip()

                if user_input == "":

                    episode_count = (
                        suggested_count
                    )

                else:

                    episode_count = int(
                        user_input
                    )

                if episode_count < 1:

                    raise ValueError

                break

            except ValueError:

                print(
                    "Please enter a valid number."
                )

        start_episode = next_episode

        end_episode = (
            next_episode
            + episode_count
            - 1
        )

        # ================================================
        # SINGLE EPISODE
        # ================================================

        if episode_count == 1:

            new_name = build_episode_filename(
                start_episode
            )

        # ================================================
        # MULTI EPISODE
        # ================================================

        else:

            new_name = (
                build_multi_episode_filename(
                    start_episode,
                    end_episode
                )
            )

        destination = (
            DESTINATION_DIR
            / new_name
        )

        if destination.exists():

            print(
                f"ERROR: File already exists:\n"
                f"{destination}"
            )

            return

        print(f"Moving to:\n{destination}")

        shutil.move(
            str(file_path),
            str(destination)
        )

        print(f"Created: {new_name}")

        next_episode = end_episode + 1

        return

    # ====================================================
    # STANDARD MODE
    # ====================================================

    new_name = build_episode_filename(
        next_episode
    )

    destination = DESTINATION_DIR / new_name

    if destination.exists():

        print(
            f"ERROR: File already exists:\n"
            f"{destination}"
        )

        return

    print(f"Moving to:\n{destination}")

    shutil.move(
        str(file_path),
        str(destination)
    )

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
# RUNTIME COMMANDS
# ============================================================

def rebuild_destination():

    global DESTINATION_DIR
    global next_episode
    global EPISODE_PATTERN

    show_folder = f"{show_name} ({year})"

    season_folder = (
        f"Season {season:02d}"
    )

    DESTINATION_DIR = (
        TV_ROOT
        / show_folder
        / season_folder
    )

    DESTINATION_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    EPISODE_PATTERN = re.compile(
        rf"S{season:02d}E(\d+)",
        re.IGNORECASE
    )

    existing_episodes = []

    for file in DESTINATION_DIR.glob("*.mkv"):

        match = EPISODE_PATTERN.search(
            file.name
        )

        if match:

            existing_episodes.append(
                int(match.group(1))
            )

    if existing_episodes:

        next_episode = (
            max(existing_episodes) + 1
        )

    else:

        next_episode = 1


def show_status():

    print("\n" + "=" * 60)

    print("CURRENT STATUS")

    print("=" * 60)

    print(f"Show: {show_name}")

    print(f"Year: {year}")

    print(f"Season: {season:02d}")

    print(f"Mode: {rip_mode}")

    print(
        f"Next Episode: "
        f"{next_episode:02d}"
    )

    print(f"Watching:\n{INCOMING_DIR}")

    print(
        f"\nDestination:\n"
        f"{DESTINATION_DIR}"
    )

    print("=" * 60 + "\n")


def command_listener():

    global show_name
    global year
    global season
    global rip_mode

    while True:

        command = input().strip().lower()

        # ====================================================
        # CHANGE SEASON
        # ====================================================

        if command == "s":

            print("\nCHANGE SEASON")
            print("-" * 30)

            season = int(
                input(
                    "New season number: "
                ).strip()
            )

            rebuild_destination()

            print(
                f"\nSeason changed "
                f"to {season:02d}"
            )

            print(
                f"Next episode: "
                f"{next_episode:02d}\n"
            )

        # ====================================================
        # NEW SHOW
        # ====================================================

        elif command == "n":

            print("\nCHANGE SHOW")
            print("-" * 30)

            show_name = input(
                "Show name: "
            ).strip()

            year = input(
                "Year: "
            ).strip()

            season = int(
                input(
                    "Season number: "
                ).strip()
            )

            rebuild_destination()

            print("\nShow updated.\n")

        # ====================================================
        # CHANGE MODE
        # ====================================================

        elif command == "mode":

            print("\nRIP MODES")
            print("-" * 30)

            print("1. Standard TV")
            print("2. Anime / Multi-Episode")

            mode_choice = input(
                "\nSelect mode: "
            ).strip()

            if mode_choice == "2":

                rip_mode = "anime"

            else:

                rip_mode = "standard"

            print(
                f"\nMode changed to: {rip_mode}\n"
            )

        # ====================================================
        # STATUS
        # ====================================================

        elif command == "status":

            show_status()

        # ====================================================
        # RECONFIGURE
        # ====================================================

        elif command == "config":

            if CONFIG_FILE.exists():

                CONFIG_FILE.unlink()

            create_config()

            load_config()

            rebuild_destination()

            print(
                "\nConfiguration updated.\n"
            )

        # ====================================================
        # HELP
        # ====================================================

        elif command == "help":

            print("\nCOMMANDS")
            print("-" * 30)

            print(
                "s       = Change season"
            )

            print(
                "n       = Change show"
            )

            print(
                "mode    = Change rip mode"
            )

            print(
                "status  = Show status"
            )

            print(
                "config  = Reconfigure folders"
            )

            print(
                "help    = Show commands"
            )

            print(
                "q       = Quit"
            )

            print()

        # ====================================================
        # QUIT
        # ====================================================

        elif command == "q":

            print("\nExiting TV Renamer...")

            quit()


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
    
    command_thread = threading.Thread(
        target=command_listener,
        daemon=True
    )

    command_thread.start()

    print("Type 'help' for commands.\n")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    main()
