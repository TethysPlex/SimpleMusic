"""
SimpleMusic - A DSL to MIDI converter library

A Python library that converts custom music DSL notation to MIDI files.
Supports multi-track compositions, chords, control events, and advanced features.
"""

from .parser import DSLParser
from .midi_converter import create_midi_file, dsl_to_midi
from .data_structures import Note, Event, Track
from .constants import NOTE_MAP, DURATION_MAP, INSTRUMENT_NAMES
from .examples import EXAMPLE_BASIC, EXAMPLE_COMPLEX, EXAMPLE_ADVANCED

__version__ = "0.1.0"
__all__ = [
    "DSLParser",
    "create_midi_file", 
    "dsl_to_midi",
    "Note",
    "Event", 
    "Track",
    "NOTE_MAP",
    "DURATION_MAP",
    "INSTRUMENT_NAMES",
    "EXAMPLE_BASIC",
    "EXAMPLE_COMPLEX", 
    "EXAMPLE_ADVANCED"
]