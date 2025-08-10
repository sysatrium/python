import json
import xml.etree.ElementTree as ET
from typing import Dict, Any, Union
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass(frozen=True)
class Song:
    title: str
    artist: str
    duration: int  # in seconds
    genre: str
    release_year: int
    id: int


class SongFactory(ABC):
    @abstractmethod
    def serialize(self, *args, **kwargs) -> Song:
        pass


class JSONSongFactory(SongFactory):
    def serialize(self, song: Song) -> str:
        return json.dumps(song.__dict__)


class XMLSongFactory(SongFactory):
    def serialize(self, song: Song) -> str:
        song_element = ET.Element("song")
        for key, value in song.__dict__.items():
            child = ET.SubElement(song_element, key)
            child.text = str(value)
        return ET.tostring(song_element, encoding="unicode")


class SongManager:
    def __init__(self):
        self.factories: Dict[str, SongFactory] = {
            "json": JSONSongFactory(),
            "xml": XMLSongFactory(),
        }

    def serialize(self, song: Song, format_type: str) -> Union[str, None]:
        factory = self.factories.get(format_type.lower())
        if not factory:
            raise ValueError(f"Factory for format {format_type} not found.")
        return factory.serialize(song)

    def get_factory(self, format_type: str) -> SongFactory:
        factory = self.factories.get(format_type.lower())
        if not factory:
            raise ValueError(f"Factory for format {format_type} not found.")
        return factory


if __name__ == "__main__":
    song = Song(
        title="Imagine",
        artist="John Lennon",
        duration=183,
        genre="Rock",
        release_year=1971,
        id=1,
    )

    manager = SongManager()

    json_song = manager.serialize(song, "json")
    print("JSON Format:")
    print(json_song)

    xml_song = manager.serialize(song, "xml")
    print("\nXML Format:")
    print(xml_song)
