# SimpleMusic

A Python library for converting custom music DSL notation to MIDI files. Write music using simple text notation and generate professional MIDI output.

## Features

- **Intuitive DSL** - Write music using simple text notation
- **Multi-track Support** - Create complex arrangements with multiple instruments  
- **Rich Expression** - Support for dynamics, articulation, and control events
- **Percussion Support** - Built-in drum kit support on channel 10
- **MIDI Control** - Program changes, control changes, pitch bends
- **Easy Installation** - Simple Python package with minimal dependencies
- **CLI + Library** - Use as command-line tool or Python library

## Quick Start

### Installation

```bash
# Clone and install
git clone <repository-url>
cd SimpleMusic
uv venv && source .venv/bin/activate
uv pip install -e .
```

### Command Line Usage

```bash
# Try a built-in example
simplemusic --example basic -o my_song.mid

# Convert your own DSL file
simplemusic my_composition.dsl -o output.mid -v
```

### Python Library Usage

```python
from simplemusic import dsl_to_midi

# Simple composition
dsl_content = """
Tempo=120
Key=C Major

Track Piano: Instrument=piano Channel=1
C4q D4q E4q F4q | G4h A4h | B4w
"""

result = dsl_to_midi(dsl_content, 'output.mid', verbose=True)
```

## DSL Example

```
# My First Song
Tempo=120
Key=C Major
TimeSig=4/4

Track Melody: Instrument=piano Channel=1
C4q D4q E4q F4q | G4q A4q B4q C5q

Track Bass: Instrument=bass Channel=2  
C3h G3h | C4h G3h

Track Chords: Instrument=guitar Channel=3
[C4q, E4q, G4q] [F4q, A4q, C5q] | [G4q, B4q, D5q] [C4w, E4w, G4w]
```

This creates a simple 3-track arrangement with melody, bass, and chords.

## Documentation

=� **Complete documentation available in the [`docs/`](docs/) directory:**

- **[Getting Started](docs/getting-started.md)** - Installation and first steps
- **[DSL Syntax Reference](docs/dsl-syntax.md)** - Complete language documentation  
- **[Examples](docs/examples.md)** - Sample compositions and techniques
- **[API Reference](docs/api-reference.md)** - Python library documentation

## Key Features

### Simple Note Notation
```
C4q     # C4 quarter note
F#5h.   # F# dotted half note in 5th octave  
Bb3e/3  # Bb eighth note triplet
```

### Chords and Harmony
```
[C4q, E4q, G4q]              # Simple triad
[C3h:v60, E3h:v70, G3h:v80]  # With different velocities
```

### Expression and Dynamics
```
C4q:v40  D4q:v60  E4q:v80  F4q:v100  # Crescendo
CC:64:127  # Sustain pedal on
PB:2048    # Pitch bend up
```

### Multiple Instruments
```
Track Piano: Instrument=piano Channel=1
Track Guitar: Instrument=electric guitar Channel=2  
Track Drums: Channel=10  # Automatic drum kit
```

## Project Structure

```
SimpleMusic/
    simplemusic/           # Main package
        __init__.py        # Package exports
        parser.py          # DSL parser
        midi_converter.py  # MIDI generation
        constants.py       # Note/instrument mappings
        data_structures.py # Note/Track/Event classes
        examples.py        # Built-in examples
        cli.py             # Command-line interface
    tests/                 # Test suite
        test_library.py    # Integration tests
        test_parser.py     # Unit tests
    docs/                  # Documentation
    run_tests.py           # Test runner
```

## Development

### Running Tests

```bash
# Run all tests
python run_tests.py

# Run specific test file
python tests/test_library.py
```

### Adding Features

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Update documentation
5. Submit a pull request

## Examples

### Basic Melody
```bash
simplemusic --example basic -o basic.mid
```

### Complex Arrangement
```bash  
simplemusic --example complex -o complex.mid
```

### Advanced Techniques
```bash
simplemusic --example advanced -o advanced.mid
```

## Requirements

- Python 3.9+
- `midiutil` library (automatically installed)

## License

[Add your license here]

## Contributing

Contributions are welcome! Please read the documentation and run the test suite before submitting changes.

---

**Start composing with SimpleMusic today!** Check out the [Getting Started Guide](docs/getting-started.md) for detailed instructions.