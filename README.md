[![License: AGPL v3+](https://img.shields.io/badge/License-AGPL_v3+-green.svg)](https://www.gnu.org/licenses/agpl-3.0)

# M3U Playlist Editor

A small graphical editor for .m3u playlists

<img width="80%" alt="Filters" src="https://github.com/leonhardw/m3u-editor/blob/main/images/editor1.png" /> 
<img width="40%" alt="Filters" src="https://github.com/leonhardw/m3u-editor/blob/main/images/rename.png" /> 

## Features
- Add songs from a folder
- Batch rename all songs in a folder based on metadata (see [Batch Renaming](#batch-renaming) section below)
- Rearrange songs in a playlist (with drag'n'drop support)
- Add song manually
- Sort folder list by title or artist (ascending and descending)
- Compact mode without folder panel
- Absolute and relative path support (see [Absolute and Relative Paths](#absolute-and-relative-paths) section below)

## Limitations
- Currently, only .flac files are supported (.mp3 support might come in the future)
- Only plain-text .m3u playlists are supported

## Batch Renaming
1. Check the "Show folder list" checkbox and open a folder containing .flac files.
2. Click on "Rename"
3. Enter the new filename pattern with the following placeholders:  
`%T` = Title  
`%A` = Artist  
e.g. `%T (%A)` -> `Title (Artist).flac`

- The title and artist will be extracted from the embedded metadata of the file.
- The filename itself is not analyzed.
- Don't add `.flac` to the pattern. Note you don't have to use all placeholders.  
- If multiple files would have the same name, `(1)`, `(2)` and so on will be added automatically.
- If a song doesn't have metadata, it won't be renamed.

## Absolute and Relative Paths
When saving a playlist, you can decide whether paths should be absolute or relative.  
- If you select relative paths, the paths will be relative to where the playlist is saved. If you move the playlist to another folder, the songs can't be found anymore. To move a playlist, open it again in the editor and save it to the new folder.  
- Absolute paths are resistent to moving the .m3u file.

## Installation
Requirements: Python 3.10 or newer
1. Download or clone the repository
2. Install requirements.txt
3. Run `playlisteditor.py`


