# Getting Started with SimpleMusic

Welcome to SimpleMusic! This guide will help you get up and running quickly with the SimpleMusic DSL to MIDI converter.

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Your First Composition](#your-first-composition)
4. [Understanding the Basics](#understanding-the-basics)
5. [Common Patterns](#common-patterns)
6. [Troubleshooting](#troubleshooting)
7. [Next Steps](#next-steps)

## Installation

### Prerequisites
- Python 3.9 or higher
- `uv` package manager (recommended) or `pip`

### Install SimpleMusic

**Using uv (recommended):**
```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install SimpleMusic
uv pip install -e .
```

**Using pip:**
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install SimpleMusic
pip install -e .
```

### Verify Installation

Test that everything is working:

```bash
# Test the CLI with a built-in example
simplemusic --example basic -o test.mid

# You should see: "✨ Conversion completed! Output: test.mid"
```

## Quick Start

### Command Line Usage

The fastest way to get started is with the built-in examples:

```bash
# Convert a basic example
simplemusic --example basic -o basic.mid

# Convert with verbose output to see details
simplemusic --example complex -o complex.mid -v

# Convert an advanced example
simplemusic --example advanced -o advanced.mid
```

### Python Library Usage

```python
from simplemusic import dsl_to_midi, EXAMPLE_BASIC

# Convert built-in example
result = dsl_to_midi(EXAMPLE_BASIC, 'my_first_song.mid', verbose=True)

if result:
    print("✅ MIDI file created successfully!")
else:
    print("❌ Conversion failed")
```

## Your First Composition

Let's create a simple song step by step.

### Step 1: Basic Setup

Create a new file called `my_song.dsl`:

```
# My First SimpleMusic Composition
Tempo=120
Key=C Major
TimeSig=4/4
```

This sets up the basic metadata:
- **Tempo**: 120 beats per minute (moderate tempo)
- **Key**: C Major (no sharps or flats)
- **TimeSig**: 4/4 time signature (4 quarter-note beats per measure)

### Step 2: Add a Simple Melody

Add a melody track:

```
# My First SimpleMusic Composition
Tempo=120
Key=C Major
TimeSig=4/4

Track Melody: Instrument=piano Channel=1
C4q D4q E4q F4q | G4q A4q B4q C5q
```

This creates:
- A track named "Melody" 
- Using piano (instrument 0)
- On MIDI channel 1
- Playing C-D-E-F-G-A-B-C as quarter notes
- The `|` separates measures for readability

### Step 3: Add Bass Line

Add a bass accompaniment:

```
# My First SimpleMusic Composition  
Tempo=120
Key=C Major
TimeSig=4/4

Track Melody: Instrument=piano Channel=1
C4q D4q E4q F4q | G4q A4q B4q C5q

Track Bass: Instrument=bass Channel=2
C3h G3h | C4h G3h
```

The bass plays:
- Half notes (`h`) for a slower rhythm
- In the lower register (octave 3-4)
- A simple C-G pattern

### Step 4: Convert to MIDI

Save your DSL file and convert it:

```bash
# Convert your composition
simplemusic my_song.dsl -o my_song.mid -v
```

The `-v` flag shows verbose output so you can see what was parsed.

## Understanding the Basics

### Note Format

Notes follow this pattern: `[NoteName][Accidental][Octave][Duration]`

**Examples:**
- `C4q` - C in 4th octave, quarter note duration
- `F#5h` - F sharp in 5th octave, half note duration  
- `Bb3w` - B flat in 3rd octave, whole note duration

### Common Durations
- `w` - Whole note (4 beats)
- `h` - Half note (2 beats)
- `q` - Quarter note (1 beat) 
- `e` - Eighth note (0.5 beats)
- `s` - Sixteenth note (0.25 beats)

### Basic Track Structure

```
Track [Name]: Instrument=[instrument] Channel=[channel]
[musical content here...]
```

**Example:**
```
Track Lead Guitar: Instrument=electric guitar Channel=1
E4q G4q B4q E5q
```

### Rests and Bar Lines

- **Rests**: Use `R` + duration (e.g., `Rq` for quarter rest)
- **Bar lines**: Use `|` to separate measures (optional but helpful)

```
Track Example: Instrument=piano
C4q D4q Rq F4q | G4h Rh
```

## Common Patterns

### Adding Chords

Use square brackets to group notes that play simultaneously:

```
Track Piano: Instrument=piano
# C major chord
[C4q, E4q, G4q] | [F4q, A4q, C5q] | [G4q, B4q, D5q] | [C4q, E4q, G4q]
```

### Dynamic Expression

Add velocity parameters for volume control:

```
Track Expressive: Instrument=violin
# Crescendo from soft to loud
C4q:v40 D4q:v60 E4q:v80 F4q:v100
```

Velocity values range from 1 (very soft) to 127 (very loud).

### Multiple Tracks

Build arrangements by adding more tracks:

```
Tempo=100
Key=G Major

Track Melody: Instrument=flute Channel=1
G4q A4q B4q C5q | D5h E5h

Track Harmony: Instrument=violin Channel=2  
B3q C4q D4q E4q | F#4h G4h

Track Bass: Instrument=bass Channel=3
G2h G2h | C3h C3h

Track Drums: Channel=10
C4q Rq D4q Rq | C4q D4q D4q C4q
```

**Note**: Channel 10 is reserved for drums in General MIDI.

### Adding Expression

Use control change (CC) events for realism:

```
Track Piano: Instrument=piano
# Add sustain pedal
CC:64:127
C4q E4q G4q C5q
# Release sustain
CC:64:0
```

Common controllers:
- `CC:64:127` - Sustain pedal on
- `CC:64:0` - Sustain pedal off  
- `CC:7:100` - Set main volume to 100

## Troubleshooting

### Common Issues

**1. "No such group" errors**
- Check note format: must be `NoteName[Octave][Duration]`
- Example: `C4q` not `C4` or `Cq`

**2. No sound when playing MIDI**
- Ensure your MIDI player supports General MIDI
- Try different instruments (piano = 0 always works)
- Check that channels don't conflict

**3. Timing sounds wrong**
- Verify tempo setting (`Tempo=120`)
- Check time signature (`TimeSig=4/4`)
- Use bar lines `|` to visually check measures

**4. Instruments sound wrong**
- Use instrument numbers (0-127) instead of names if names don't work
- Channel 10 is drums only - use other channels for melodic instruments
- Try `Instrument=0` (piano) as a fallback

### Debugging Tips

**Use verbose output:**
```bash
simplemusic my_song.dsl -o output.mid -v
```

This shows:
- Parsed metadata
- Number of tracks found
- Notes and events per track
- Any parsing warnings

**Test incrementally:**
1. Start with one track
2. Add tracks one by one
3. Test after each addition

**Check your DSL syntax:**
```
# Good:
Track Piano: Instrument=piano
C4q D4q E4q F4q

# Bad (missing colon after track name):
Track Piano Instrument=piano
C4q D4q E4q F4q
```

## Next Steps

### Learn More Features

Now that you have the basics, explore more advanced features:

1. **[DSL Syntax Reference](dsl-syntax.md)** - Complete language documentation
2. **[Examples](examples.md)** - More complex compositions and techniques
3. **[API Reference](api-reference.md)** - Using SimpleMusic in Python programs

### Advanced Techniques to Try

**Dotted rhythms:**
```
Track Swing: Instrument=saxophone
C4q. D4e E4q. F4e
```

**Chord progressions:**
```
Track Progression: Instrument=piano
[C4q, E4q, G4q] [A3q, C4q, E4q] [F3q, A3q, C4q] [G3q, B3q, D4q]
```

**Tuplets:**
```
Track Triplets: Instrument=piano
C4e/3 D4e/3 E4e/3 F4q
```

### Building Longer Compositions

**Structure your compositions:**
```
# Verse
Track Lead: Instrument=guitar
C4q D4q E4q F4q | G4q F4q E4q D4q |

# Chorus  
G4q G4q A4q A4q | B4h C5h |

# Bridge
E4e F4e G4e A4e B4e C5e D5e E5e
```

**Use comments for organization:**
```
# === INTRO ===
Track Piano: Instrument=piano
C4w

# === VERSE 1 ===
C4q D4q E4q F4q | G4h A4h

# === CHORUS ===
[C4q, E4q, G4q] [F4q, A4q, C5q] | [G4q, B4q, D5q] [C4w, E4w, G4w]
```

### Performance Tips

- **Start simple** and add complexity gradually
- **Use built-in examples** as templates
- **Test frequently** while composing
- **Organize with comments** and consistent formatting
- **Plan your channels** to avoid conflicts

Happy composing! 🎵