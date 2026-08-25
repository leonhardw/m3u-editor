[![License: AGPL v3+](https://img.shields.io/badge/License-AGPL_v3+-green.svg)](https://www.gnu.org/licenses/agpl-3.0)

# M3U Playlist Editor

A lightweight graphical tool for managing, sorting, and batch-renaming `.m3u` playlists.

| Main Editor View | Batch Rename Dialog |
| :---: | :---: |
| <img src="images/editor1.png" width="100%" alt="Main Editor View"> | <img src="images/rename.png" width="100%" alt="Rename Dialog"> |

## Features
- **Folder View:** Display all audio tracks in a selected directory.
- **Batch Renaming:** Rename files based on embedded metadata tags (see [Batch Renaming](#batch-renaming)).
- **Playlist Management:** Rearrange tracks via drag-and-drop and add songs manually.
- **Sorting:** Sort folder contents by title or artist (ascending and descending).
- **Compact Mode:** Hide the folder panel if you don't need it.
- **Path Flexibility:** Support for absolute and relative paths (see [Absolute and Relative Paths](#absolute-and-relative-paths)).

## Limitations
- Currently, only .flac files are supported (.mp3 support might come in the future)
- Only plain-text .m3u playlists are supported

## Batch Renaming
1. Check "Show folder list" and open a folder containing .flac files.
2. Click on "Rename"
3. Enter the new filename pattern with the following placeholders:  
  - `%T` = Title  
  - `%A` = Artist  

*Example:* `%T (%A)` → `Title (Artist).flac`

**Note:**
- Metadata is extracted directly from embedded FLAC tags (the original filename is not analyzed).
- Do **not** include `.flac` in your custom pattern.
- You do not need to use every placeholder.
- Duplicate filenames automatically receive incremental suffixes like `(1)`, `(2)`, etc.
- Tracks without metadata will be skipped.

## Absolute and Relative Paths
When saving a playlist, choose between two path formats:

- **Relative Paths:** File paths are relative to the directory where the `.m3u` file is saved. Moving the playlist file independently will break track paths. To relocate a relative playlist, open it in the editor and save it to the new location.
- **Absolute Paths:** Stores explicit full system paths, keeping the playlist functional regardless of where the `.m3u` file itself is moved.

## Installation
Requirements: Python 3.10 or newer
1. Clone or download this repository:
```bash
git clone https://github.com/leonhardw/m3u-editor.git
cd m3u-editor
```
2. Install dependencies
```bash
# Windows
pip install -r requirements.txt

# Linux and macOS
pip3 install -r requirements.txt
```
3. Run
```bash
# Windows
python playlisteditor.py

# Linux and macOS
python3 playlisteditor.py
```


