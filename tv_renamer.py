# ============================================================
# TV_Renamer
#
# Copyright (c) 2026 Joshua Holmes
#
# Licensed under the Apache License, Version 2.0
# ============================================================

import re
import shutil
import time
import json
import threading
import subprocess
import tempfile
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


# ============================================================
# CONFIG
# ============================================================

CONFIG_FILE = Path("config.json")

STABLE_TIME = 30
POLL_INTERVAL = 2

MKVMERGE_PATH = "mkvmerge.exe"

ANIME_TARGET_EPISODE_MINUTES = 24
ANIME_MIN_EPISODE_MINUTES = 18
ANIME_MAX_EPISODE_MINUTES = 35
CHAPTER_MATCH_TOLERANCE_MINUTES = 3


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
print("2. Anime / Split Mode")

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

DESTINATION_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# DETERMINE NEXT EPISODE
# ============================================================

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

    stable_for = 0
    last_size = -1

    while stable_for < STABLE_TIME:

        try:
            current_size = (
                file_path.stat().st_size
            )

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
# MKV SPLITTING
# ============================================================

def duration_to_seconds(value):

    if value is None:
        return None

    if isinstance(value, (int, float)):

        if value > 1000000:
            return value / 1000000000

        return float(value)

    if not isinstance(value, str):
        return None

    value = value.strip()

    if not value:
        return None

    if value.isdigit():
        return duration_to_seconds(
            int(value)
        )

    parts = value.split(":")

    if len(parts) != 3:
        return None

    try:

        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = float(parts[2])

    except ValueError:
        return None

    return (
        hours * 3600
        + minutes * 60
        + seconds
    )


def seconds_to_timestamp(seconds):

    whole_seconds = int(seconds)
    milliseconds = int(
        round(
            (seconds - whole_seconds) * 1000
        )
    )

    if milliseconds == 1000:
        whole_seconds += 1
        milliseconds = 0

    hours = whole_seconds // 3600
    minutes = (
        whole_seconds % 3600
    ) // 60
    secs = whole_seconds % 60

    return (
        f"{hours:02d}:"
        f"{minutes:02d}:"
        f"{secs:02d}."
        f"{milliseconds:03d}"
    )


def load_mkv_metadata(input_file):

    command = [
        MKVMERGE_PATH,
        "-J",
        str(input_file)
    ]

    try:

        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True
        )

    except FileNotFoundError:

        print(
            "\nAutomatic split unavailable:"
            "\nmkvmerge.exe not found."
        )

        print(
            "\nInstall MKVToolNix "
            "and add it to PATH."
        )

        return None

    except subprocess.CalledProcessError:

        print(
            "\nAutomatic split unavailable:"
            "\nCould not read MKV metadata."
        )

        return None

    try:

        return json.loads(
            result.stdout
        )

    except json.JSONDecodeError:

        print(
            "\nAutomatic split unavailable:"
            "\nMKV metadata was not valid JSON."
        )

        return None


def get_mkv_duration_seconds(metadata):

    container = metadata.get(
        "container",
        {}
    )

    properties = container.get(
        "properties",
        {}
    )

    duration = duration_to_seconds(
        properties.get("duration")
    )

    if duration:
        return duration

    longest_track = 0

    for track in metadata.get("tracks", []):

        track_properties = track.get(
            "properties",
            {}
        )

        track_duration = duration_to_seconds(
            track_properties.get("duration")
        )

        if track_duration:
            longest_track = max(
                longest_track,
                track_duration
            )

    if longest_track:
        return longest_track

    return None


def collect_chapter_starts(node):

    chapter_starts = []

    if isinstance(node, dict):

        for key in (
            "start",
            "start_time",
            "start_timestamp"
        ):

            if key in node:

                seconds = duration_to_seconds(
                    node[key]
                )

                if seconds is not None:
                    chapter_starts.append(
                        seconds
                    )

        for value in node.values():

            chapter_starts.extend(
                collect_chapter_starts(
                    value
                )
            )

    elif isinstance(node, list):

        for item in node:

            chapter_starts.extend(
                collect_chapter_starts(
                    item
                )
            )

    return chapter_starts


def get_chapter_start_seconds(metadata):

    chapter_starts = collect_chapter_starts(
        metadata.get(
            "chapters",
            []
        )
    )

    cleaned_starts = {
        round(start, 3)
        for start in chapter_starts
        if start > 1
    }

    return sorted(
        cleaned_starts
    )


def choose_episode_count(duration_seconds):

    target_seconds = (
        ANIME_TARGET_EPISODE_MINUTES
        * 60
    )

    episode_count = round(
        duration_seconds / target_seconds
    )

    if episode_count < 2:
        return None

    average_minutes = (
        duration_seconds
        / episode_count
        / 60
    )

    if (
        average_minutes
        < ANIME_MIN_EPISODE_MINUTES
        or average_minutes
        > ANIME_MAX_EPISODE_MINUTES
    ):
        return None

    return episode_count


def detect_anime_split_timestamps(input_file):

    metadata = load_mkv_metadata(
        input_file
    )

    if not metadata:
        return []

    duration_seconds = get_mkv_duration_seconds(
        metadata
    )

    if not duration_seconds:

        print(
            "\nAutomatic split unavailable:"
            "\nCould not determine MKV duration."
        )

        return []

    episode_count = choose_episode_count(
        duration_seconds
    )

    if not episode_count:
        return []

    chapter_starts = get_chapter_start_seconds(
        metadata
    )

    if not chapter_starts:

        print(
            "\nAutomatic split unavailable:"
            "\nNo chapter markers found."
        )

        return []

    tolerance_seconds = (
        CHAPTER_MATCH_TOLERANCE_MINUTES
        * 60
    )

    split_points = []

    for split_number in range(
        1,
        episode_count
    ):

        target_seconds = (
            duration_seconds
            / episode_count
            * split_number
        )

        nearest_chapter = min(
            chapter_starts,
            key=lambda chapter: abs(
                chapter - target_seconds
            )
        )

        if (
            abs(
                nearest_chapter - target_seconds
            )
            > tolerance_seconds
        ):
            return []

        if (
            split_points
            and nearest_chapter <= split_points[-1]
        ):
            return []

        split_points.append(
            nearest_chapter
        )

    return [
        seconds_to_timestamp(
            split_point
        )
        for split_point in split_points
    ]


def split_mkv_by_timestamps(
    input_file,
    timestamps
):

    global next_episode

    print("\nStarting MKV split process...")

    temp_dir = Path(
        tempfile.mkdtemp(
            prefix="tvrenamer_"
        )
    )

    output_pattern = (
        temp_dir
        / "split_%03d.mkv"
    )

    split_string = ",".join(
        timestamps
    )

    command = [
        MKVMERGE_PATH,
        "-o",
        str(output_pattern),
        "--split",
        f"timestamps:{split_string}",
        str(input_file)
    ]

    try:

        subprocess.run(
            command,
            check=True
        )

    except FileNotFoundError:

        print(
            "\nERROR:"
            "\nmkvmerge.exe not found."
        )

        print(
            "\nInstall MKVToolNix "
            "and add it to PATH."
        )

        return False

    except subprocess.CalledProcessError:

        print(
            "\nERROR:"
            "\nMKV splitting failed."
        )

        return False

    split_files = sorted(
        temp_dir.glob("*.mkv")
    )

    if not split_files:

        print(
            "\nERROR:"
            "\nNo split files created."
        )

        return False

    print(
        f"\nCreated "
        f"{len(split_files)} episode files."
    )

    for split_file in split_files:

        new_name = build_episode_filename(
            next_episode
        )

        destination = (
            DESTINATION_DIR
            / new_name
        )

        print(
            f"\nMoving:\n"
            f"{split_file.name}"
        )

        print(
            f"To:\n{destination}"
        )

        shutil.move(
            str(split_file),
            str(destination)
        )

        print(
            f"Created: {new_name}"
        )

        next_episode += 1

    try:
        input_file.unlink()
    except Exception:
        pass

    try:
        temp_dir.rmdir()
    except Exception:
        pass

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

    detected_title = extract_title_number(
        file_path.name
    )

    if detected_title is not None:

        print(
            f"Detected MakeMKV title: "
            f"t{detected_title:02d}"
        )

    # ====================================================
    # ANIME / SPLIT MODE
    # ====================================================

    if rip_mode == "anime":

        print("\nAnime/Split mode enabled.")

        if is_probable_multi_episode(
            detected_title
        ):

            print(
                "\nPossible multi-episode "
                "MKV detected."
            )

        auto_timestamps = detect_anime_split_timestamps(
            file_path
        )

        if auto_timestamps:

            print(
                "\nAutomatic split points found:"
            )

            print(
                ", ".join(
                    auto_timestamps
                )
            )

            auto_choice = input(
                "\nSplit automatically "
                "using these timestamps? "
                "(y/n): "
            ).strip().lower()

            if auto_choice == "y":

                split_mkv_by_timestamps(
                    file_path,
                    auto_timestamps
                )

                return

        split_choice = input(
            "\nEnter manual split timestamps? "
            "(y/n): "
        ).strip().lower()

        # ====================================================
        # SPLIT MKV
        # ====================================================

        if split_choice == "y":

            print(
                "\nEnter split timestamps."
            )

            print(
                "\nExample:"
            )

            print(
                "00:24:10,00:48:22"
            )

            print(
                "\nThis creates:"
            )

            print(
                "Episode 1 = 0 -> 24:10"
            )

            print(
                "Episode 2 = 24:10 -> 48:22"
            )

            print(
                "Episode 3 = 48:22 -> end"
            )

            timestamp_input = input(
                "\nSplit timestamps: "
            ).strip()

            timestamps = [
                t.strip()
                for t in timestamp_input.split(",")
                if t.strip()
            ]

            if not timestamps:

                print(
                    "\nNo timestamps entered."
                )

                return

            split_mkv_by_timestamps(
                file_path,
                timestamps
            )

            return

    # ====================================================
    # NORMAL SINGLE FILE
    # ====================================================

    new_name = build_episode_filename(
        next_episode
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

    next_episode += 1


# ============================================================
# WATCHDOG HANDLER
# ============================================================

class MKVHandler(
    FileSystemEventHandler
):

    def on_created(self, event):

        if event.is_directory:
            return

        file_path = Path(
            event.src_path
        )

        if file_path.suffix.lower() != ".mkv":
            return

        time.sleep(2)

        process_file(file_path)


# ============================================================
# RUNTIME COMMANDS
# ============================================================

def rebuild_destination():

    global DESTINATION_DIR
    global next_episode
    global EPISODE_PATTERN

    show_folder = (
        f"{show_name} ({year})"
    )

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

    print(
        f"Watching:\n{INCOMING_DIR}"
    )

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
            print("2. Anime / Split Mode")

            mode_choice = input(
                "\nSelect mode: "
            ).strip()

            if mode_choice == "2":
                rip_mode = "anime"
            else:
                rip_mode = "standard"

            print(
                f"\nMode changed to: "
                f"{rip_mode}\n"
            )

        # ====================================================
        # STATUS
        # ====================================================

        elif command == "status":

            show_status()

        # ====================================================
        # CONFIG
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

            print(
                "\nExiting TV Renamer..."
            )

            quit()


# ============================================================
# MAIN
# ============================================================

def main():

    if not INCOMING_DIR.exists():

        print(
            f"Incoming folder missing:\n"
            f"{INCOMING_DIR}"
        )

        return

    print("\n" + "=" * 60)

    print("TV RENAMER RUNNING")

    print("=" * 60)

    print(f"Show: {show_name}")

    print(f"Season: {season:02d}")

    print(
        f"Next episode: "
        f"{next_episode:02d}"
    )

    print(
        f"Watching: {INCOMING_DIR}"
    )

    print(
        f"Destination: "
        f"{DESTINATION_DIR}"
    )

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
