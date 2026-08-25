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

import io
import os
import re
from typing import Sequence

import unicodedata
from PIL import Image
from mutagen.flac import FLAC
from pathvalidate import sanitize_filename

song_pattern = re.compile(r'^(?:\d\d )?(.+) - (.+).flac$')

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
    metadata = []
    if basedir is None:
        basedir = os.getcwd()
    
    for song in songs:
        path = os.path.abspath(os.path.join(basedir, song))
        audio = FLAC(path)
        title = audio.get('title')[0]
        artists = audio.get('artist')
        
        if not title or not artists:
            artists, title = song_pattern.search(os.path.split(path)[1]).groups()
            artists = [artists]
        
        if audio.pictures:
            cover_data = audio.pictures[0].data
            
            if cover_as_bytes:
                img = cover_data
            else:
                img = Image.open(io.BytesIO(cover_data))
                if cover_size is not None:
                    img.thumbnail((cover_size, cover_size), Image.Resampling.LANCZOS)
        else:
            img = None
        
        song_data = {'text': f'{title}\n{', '.join(artists)}', 'title': title, 'artists': ', '.join(artists), 'cover': img, 'path': path}
        metadata.append(song_data)
    
    return metadata


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
        if os.path.splitext(filename)[1] != '.flac':
            continue
        
        incomplete_data = False
        
        audio = FLAC(os.path.join(folder, filename))
        title = audio.get('title')[0]
        artists = ', '.join(audio.get('artist'))
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
            rename_operations.append((filename, f'{new_filename}.flac'))
    
    if preview_only:
        return rename_operations
    
    else:
        for old, new in rename_operations:
            old_path = os.path.join(folder, old)
            new_path = os.path.join(folder, new)
            os.rename(old_path, new_path)
        return None


if __name__ == '__main__':
    print(to_ascii('ÄÖÜäöüßẞ, –é— âêîôû²³'))
    get_song_metadata([r"C:\Leonhard\Musik\FLAC\Racing\14 The Blah Blah Blahs - Do It Better.flac"], basedir=r"C:\Leonhard\Musik\FLAC\Racing")
    print(batch_rename(r"C:\Leonhard\Musik\FLAC\LW 2", '{a}{{b}}%T%%%A', True))
