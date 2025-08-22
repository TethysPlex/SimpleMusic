# SimpleMusic API Reference

This document provides detailed API documentation for the SimpleMusic Python library.

## Table of Contents

1. [Core Functions](#core-functions)
2. [Parser Classes](#parser-classes)
3. [Data Structures](#data-structures)
4. [Constants](#constants)
5. [Examples and Utilities](#examples-and-utilities)

## Core Functions

### `dsl_to_midi(dsl_text, output_file, verbose=False)`

Main function to convert SimpleMusic DSL text to a MIDI file.

**Parameters:**
- `dsl_text` (str): The SimpleMusic DSL content as a string
- `output_file` (str, optional): Output MIDI filename. Defaults to `'output.mid'`
- `verbose` (bool, optional): Enable verbose output showing parsing details. Defaults to `False`

**Returns:**
- `dict` or `None`: Parsed data structure on success, `None` on failure

**Example:**
```python
from simplemusic import dsl_to_midi

dsl_content = """
Tempo=120
Track Piano: Instrument=piano
C4q D4q E4q F4q
"""

result = dsl_to_midi(dsl_content, 'my_song.mid', verbose=True)
if result:
    print("Conversion successful!")
```

### `create_midi_file(parsed_data, output_file='output.mid')`

Create a MIDI file from parsed DSL data.

**Parameters:**
- `parsed_data` (dict): Data structure returned by `DSLParser.parse()`
- `output_file` (str, optional): Output MIDI filename. Defaults to `'output.mid'`

**Example:**
```python
from simplemusic import DSLParser, create_midi_file

parser = DSLParser("C4q D4q E4q F4q")
parsed_data = parser.parse()
create_midi_file(parsed_data, 'output.mid')
```

## Parser Classes

### `DSLParser`

Main parser class for SimpleMusic DSL content.

#### `__init__(self, dsl_text)`

Initialize the parser with DSL text.

**Parameters:**
- `dsl_text` (str): The SimpleMusic DSL content to parse

#### `parse(self) -> dict`

Parse the DSL text and return structured data.

**Returns:**
- `dict`: Structured representation with the following format:
  ```python
  {
      'metadata': {
          'tempo': int,
          'key': str,  
          'time_sig': tuple,
          'ticks_per_beat': int
      },
      'tracks': {
          'track_name': {
              'config': {
                  'channel': int,
                  'instrument': int
              },
              'notes': [Note, ...],
              'events': [Event, ...]
          }
      }
  }
  ```

**Example:**
```python
from simplemusic import DSLParser

dsl_text = """
Tempo=120
Track Lead: Instrument=piano Channel=1
C4q D4q E4q F4q
"""

parser = DSLParser(dsl_text)
result = parser.parse()

print(f"Tempo: {result['metadata']['tempo']}")
print(f"Number of tracks: {len(result['tracks'])}")
```

#### Private Methods

The `DSLParser` class contains several private methods for internal parsing:

- `_preprocess_lines(self, dsl_text)`: Process input text and handle multi-line tracks
- `_parse_track_line(self, line)`: Parse individual track definition lines
- `_parse_sequence(self, sequence, track)`: Parse note sequences within tracks
- `_parse_chord(self, chord_str, track)`: Parse chord notation
- `_parse_note(self, note_str, track, is_chord=False)`: Parse individual notes
- `_parse_note_params(self, param_parts)`: Parse note parameters (velocity, channel, etc.)
- `_note_to_midi(self, note_name, octave)`: Convert note names to MIDI pitch numbers
- `_parse_duration(self, duration_str)`: Parse duration strings to beat values

## Data Structures

### `Note`

Represents a musical note with all its properties.

**Attributes:**
- `pitch` (int): MIDI pitch value (0-127)
- `duration` (float): Duration in beats
- `start_time` (float): Start time in beats from beginning of track
- `velocity` (int, default=80): MIDI velocity (0-127)
- `channel` (int, default=0): MIDI channel (0-15)
- `instrument` (Optional[int], default=None): Specific instrument override
- `actual_length` (Optional[float], default=None): Actual note length for legato/staccato

**Example:**
```python
from simplemusic import Note

# Create a C4 quarter note
note = Note(
    pitch=60,           # C4
    duration=1.0,       # Quarter note
    start_time=0.0,     # Beginning of track
    velocity=100,       # Forte
    channel=0           # Channel 1 (0-indexed)
)
```

### `Event`

Represents a MIDI control event.

**Attributes:**
- `type` (str): Event type ('PC', 'CC', 'PB', 'Tempo')
- `time` (float): Event time in beats
- `channel` (int): MIDI channel (0-15)  
- `data` (dict): Event-specific data

**Event Types:**
- `'PC'` (Program Change): `{'program': int}`
- `'CC'` (Control Change): `{'controller': int, 'value': int}`
- `'PB'` (Pitch Bend): `{'value': int}`
- `'Tempo'`: `{'tempo': int}`

**Example:**
```python
from simplemusic import Event

# Sustain pedal on
sustain_on = Event(
    type='CC',
    time=0.0,
    channel=0,
    data={'controller': 64, 'value': 127}
)

# Program change to piano
piano_change = Event(
    type='PC', 
    time=0.0,
    channel=0,
    data={'program': 0}
)
```

### `Track`

Represents a musical track containing notes and events.

**Attributes:**
- `name` (str): Track name
- `channel` (int, default=0): Default MIDI channel
- `instrument` (int, default=0): Default instrument
- `notes` (List[Note]): List of notes in the track
- `events` (List[Event]): List of control events
- `current_time` (float, default=0.0): Current parsing position in beats

**Example:**
```python
from simplemusic import Track, Note, Event

track = Track(
    name="Lead Guitar",
    channel=0,
    instrument=27  # Clean electric guitar
)

# Add a note
track.notes.append(Note(60, 1.0, 0.0))  # C4 quarter note

# Add a control event  
track.events.append(Event('CC', 0.0, 0, {'controller': 7, 'value': 100}))
```

## Constants

### `NOTE_MAP`

Dictionary mapping note names to semitone offsets within an octave.

```python
NOTE_MAP = {
    'C': 0, 'D': 2, 'E': 4, 'F': 5, 
    'G': 7, 'A': 9, 'B': 11
}
```

### `DURATION_MAP`

Dictionary mapping duration characters to beat values.

```python
DURATION_MAP = {
    'w': 4.0,      # Whole note
    'h': 2.0,      # Half note  
    'q': 1.0,      # Quarter note
    'e': 0.5,      # Eighth note
    's': 0.25,     # Sixteenth note
    't': 0.125,    # Thirty-second note
}
```

### `INSTRUMENT_NAMES`

Dictionary mapping instrument names to MIDI program numbers.

**Examples:**
```python
INSTRUMENT_NAMES = {
    'piano': 0,
    'guitar': 24,
    'violin': 40,
    'trumpet': 56,
    'drums': 0,  # Special case for channel 10
    # ... many more instruments
}
```

**Usage:**
```python
from simplemusic import INSTRUMENT_NAMES

# Get MIDI program number for violin
violin_program = INSTRUMENT_NAMES['violin']  # Returns 40

# Check available instruments
available_instruments = list(INSTRUMENT_NAMES.keys())
```

## Examples and Utilities

### Built-in Examples

The library includes three pre-defined example compositions:

#### `EXAMPLE_BASIC`
Simple two-track composition demonstrating basic functionality.

#### `EXAMPLE_COMPLEX` 
Multi-track composition with chords, multiple instruments, and control events.

#### `EXAMPLE_ADVANCED`
Advanced composition featuring dotted rhythms, tuplets, and sophisticated techniques.

**Usage:**
```python
from simplemusic import EXAMPLE_BASIC, EXAMPLE_COMPLEX, dsl_to_midi

# Convert basic example
result = dsl_to_midi(EXAMPLE_BASIC, 'basic_demo.mid')

# Convert complex example with verbose output
result = dsl_to_midi(EXAMPLE_COMPLEX, 'complex_demo.mid', verbose=True)
```

## Error Handling

### Parser Errors

The parser is designed to be fault-tolerant and will continue parsing even when errors are encountered. Common issues include:

1. **Invalid note formats**: Malformed note strings are skipped
2. **Out-of-range values**: MIDI values are clamped to valid ranges (0-127)
3. **Unknown instruments**: Default to piano (program 0)
4. **Malformed control events**: Invalid events are skipped with warnings

### Exception Types

The library may raise standard Python exceptions:

- `ValueError`: Invalid parameter values
- `FileNotFoundError`: Output directory doesn't exist
- `PermissionError`: Cannot write to output file

**Example Error Handling:**
```python
from simplemusic import dsl_to_midi

try:
    result = dsl_to_midi(dsl_content, 'output.mid', verbose=True)
    if result is None:
        print("Conversion failed - check DSL syntax")
    else:
        print("Conversion successful!")
except Exception as e:
    print(f"Error during conversion: {e}")
```

## Advanced Usage

### Custom Track Processing

```python
from simplemusic import DSLParser

# Parse DSL
parser = DSLParser(dsl_text)
result = parser.parse()

# Process each track
for track_name, track_data in result['tracks'].items():
    print(f"Track: {track_name}")
    print(f"  Instrument: {track_data['config']['instrument']}")
    print(f"  Channel: {track_data['config']['channel']}")
    print(f"  Notes: {len(track_data['notes'])}")
    
    # Analyze note ranges
    if track_data['notes']:
        pitches = [note.pitch for note in track_data['notes']]
        print(f"  Pitch range: {min(pitches)} - {max(pitches)}")
```

### Programmatic DSL Generation

```python
from simplemusic import dsl_to_midi

def generate_scale(root_note='C', octave=4, scale_type='major'):
    """Generate a DSL string for a musical scale."""
    
    major_intervals = [0, 2, 4, 5, 7, 9, 11]
    note_names = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    
    dsl = f"""
Tempo=120
Key={root_note} Major
Track Scale: Instrument=piano

"""
    
    for i, interval in enumerate(major_intervals):
        note_name = note_names[(note_names.index(root_note) + i) % 7]
        dsl += f"{note_name}{octave}q "
    
    return dsl

# Generate and convert C major scale
scale_dsl = generate_scale('C', 4, 'major')
dsl_to_midi(scale_dsl, 'c_major_scale.mid')
```

This API reference provides comprehensive documentation for integrating SimpleMusic into Python applications and extending its functionality.