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

from PIL import Image
from mutagen.flac import FLAC
from mutagen.id3 import ID3, Frames

song_pattern = re.compile(r'^(?:\d\d )?(.+) - (.+).flac$')


class Metadata:
    def __init__(self, filename, include_cover=True):
        self.filename = filename
        self.filetype = os.path.splitext(filename)[1]
        
        self.include_cover = include_cover
        
        self.title = ''
        self.artists = ''
        self.cover = None
        
        match self.filetype:
            case '.flac':
                audio = FLAC(filename)
                self.title = audio.get('title', '')[0]
                self.artists = audio.get('artist', [])
                if self.include_cover:
                    if audio.pictures:
                        self.cover = audio.pictures[0].data
            
            case '.mp3':
                requested_ids = {'TIT2', 'TPE1'}
                if self.include_cover:
                    requested_ids.add('APIC')
                
                # Nur die Klassen für die benötigten Frames herausfiltern
                selected_frames = {k: v for k, v in Frames.items() if k in requested_ids}
                
                # ID3 anweisen, ausschließlich diese Frames zu dekodieren
                audio = ID3(filename, known_frames=selected_frames)
                
                tit2 = audio.get('TIT2')
                self.title = tit2.text[0] if tit2 and tit2.text else ''
                
                tpe1 = audio.get('TPE1')
                self.artists = tpe1.text[0].split(';') if tpe1 and tpe1.text else []
                
                if self.include_cover:
                    apic_tags = audio.getall('APIC')
                    if apic_tags:
                        self.cover = apic_tags[0].data
        
        if not self.title or not self.artists:
            self.artists, self.title = song_pattern.search(os.path.split(path)[1]).groups()
            self.artists = [self.artists]
    
    @property
    def cover_pil(self):
        return Image.open(io.BytesIO(self.cover))
