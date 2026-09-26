#  Copyright (C) 2026  leonhardw
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import re
from typing import Sequence

import unicodedata
from PIL import Image
from pathvalidate import sanitize_filename

from metadata_helper import Metadata

song_pattern = re.compile(r'^(?:\d\d )?(.+) - (.+).(flac|mp3)$')

placeholder_replacements = {'%T': '{title}', '%A': '{artist}'}


def to_ascii(text: str) -> str:
    replacements = {
        'ä': 'ae',
        'Ä': 'Ae',
        'ö': 'oe',
        'Ö': 'Oe',
        'ü': 'ue',
        'Ü': 'Ue',
        'ß': 'ss',
        'ẞ': 'Ss',
    }
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)
    
    normalized = unicodedata.normalize('NFD', text)
    ascii_text = ''.join(
        char for char in normalized if unicodedata.category(char) != 'Mn'
    )
    
    return ascii_text.encode('ascii', 'ignore').decode('ascii')


def load_m3u(filename) -> list:
    with open(filename, 'r') as f:
        content = f.read()
    songs = content.split('\n')
    return songs


def get_song_metadata(songs: Sequence[str], basedir=None, cover_as_bytes=False, cover_size=None) -> list[dict]:
    metadata_list = []
    if basedir is None:
        basedir = os.getcwd()
    
    for song in songs:
        path = os.path.abspath(os.path.join(basedir, song))
        metadata = Metadata(path)
        title = metadata.title
        artists = metadata.artists
        cover = metadata.cover
        
        if cover:
            if cover_as_bytes:
                img = cover
            else:
                img = metadata.cover_pil
                if cover_size is not None:
                    img.thumbnail((cover_size, cover_size), Image.Resampling.LANCZOS)
        else:
            img = None
        
        song_data = {'text': f'{title}\n{', '.join(artists)}', 'title': title, 'artists': ', '.join(artists), 'cover': img, 'path': path}
        metadata_list.append(song_data)
    
    return metadata_list


def save_as_m3u(filename, data, rel_paths=True):
    folder = os.path.dirname(filename)
    m3u_data = '\n'.join(convert_data_to_m3u(data, folder, rel_paths))
    with open(filename, 'w') as f:
        f.write(m3u_data)


def convert_data_to_m3u(data: list[dict], folder=None, rel_paths=True):
    m3u_list = []
    for song in data:
        if rel_paths:
            new_path = os.path.relpath(song['path'], start=folder)
        else:
            new_path = os.path.abspath(song['path'])
        m3u_list.append(new_path)
    return m3u_list


def batch_rename(folder, pattern, preview_only=False):
    for old, new in (('%%', '\x00'), ('{', '{{'), ('}', '}}')):
        pattern = pattern.replace(old, new)
    for old, new in placeholder_replacements.items():
        pattern = pattern.replace(old, new)
    pattern = pattern.replace('\x00', '%')
    
    old_names = set(os.path.splitext(i)[0] for i in os.listdir(folder))
    new_names = set()
    rename_operations: list[tuple[str, str]] = []
    # print(folder, pattern)
    
    for filename in os.listdir(folder):
        ext = os.path.splitext(filename)[1]
        if ext not in ('.flac', '.mp3'):
            continue
        
        incomplete_data = False
        
        metadata = Metadata(os.path.join(folder, filename), include_cover=False)
        title = metadata.title
        artists = ', '.join(metadata.artists)
        if not title or not artists:
            incomplete_data = True
        
        if not incomplete_data:
            new_filename = pattern.format(title=title, artist=artists)
            new_filename = sanitize_filename(to_ascii(new_filename))
            # print(filename)
            if new_filename in new_names or (new_filename != os.path.splitext(filename)[0] and new_filename in old_names):
                already_exists = True
                duplicate_number = 1
                
                while already_exists:
                    possible_name = f'{new_filename} ({duplicate_number})'
                    if possible_name in new_names:
                        duplicate_number += 1
                    else:
                        already_exists = False
                        new_filename = possible_name
            
            new_names.add(new_filename)
            rename_operations.append((filename, f'{new_filename}{ext}'))
    
    if preview_only:
        return rename_operations
    
    else:
        for old, new in rename_operations:
            old_path = os.path.join(folder, old)
            new_path = os.path.join(folder, new)
            os.rename(old_path, new_path)
        return None
