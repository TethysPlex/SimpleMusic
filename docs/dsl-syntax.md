# SimpleMusic DSL Syntax Reference

The SimpleMusic Domain Specific Language (DSL) is a text-based notation system for describing musical compositions that can be converted to MIDI files.

## Overview

A SimpleMusic file consists of:
1. **Metadata** - Global settings like tempo, key signature, time signature
2. **Track Definitions** - Individual instrument tracks with their configurations
3. **Musical Content** - Notes, chords, rests, and control events

## File Structure

```
# Global Metadata
Tempo=120
Key=C Major
TimeSig=4/4
TicksPerBeat=480

# Track Definition with Configuration
Track TrackName: Instrument=piano Channel=1
# Musical content goes here...
C4q D4q E4q F4q

# Multiple tracks can be defined
Track Bass: Instrument=bass Channel=2  
C2h G2h C2w
```

## Metadata Section

### Tempo
Sets the beats per minute for the composition.

```
Tempo=120        # 120 BPM (default)
Tempo=140        # Faster tempo
```

### Key Signature
Specifies the key signature (informational, affects MIDI meta-events).

```
Key=C Major      # C Major (default)
Key=G Major      # G Major
Key=F# Minor     # F# Minor
```

### Time Signature
Sets the time signature of the composition.

```
TimeSig=4/4      # 4/4 time (default)
TimeSig=3/4      # 3/4 waltz time
TimeSig=6/8      # 6/8 compound time
```

### Ticks Per Beat
Sets MIDI timing resolution.

```
TicksPerBeat=480    # High resolution (default)
TicksPerBeat=240    # Standard resolution
```

## Track Definitions

### Basic Track Syntax
```
Track TrackName: [Configuration]
```

### Track Configuration

#### Instrument
Sets the MIDI instrument for the track.

```
# By MIDI program number
Instrument=0         # Acoustic Grand Piano
Instrument=25        # Steel String Guitar

# By name (case-insensitive)
Instrument=piano     # Acoustic Grand Piano
Instrument=guitar    # Acoustic Guitar
Instrument=violin    # Violin
Instrument=drums     # Drum kit (uses channel 10)
```

**Common Instrument Names:**
- **Keyboards**: piano, electric piano, harpsichord, organ, accordion
- **Strings**: violin, viola, cello, guitar, bass, harp
- **Brass**: trumpet, trombone, tuba, french horn, saxophone
- **Woodwinds**: flute, clarinet, oboe, bassoon, piccolo
- **Percussion**: drums (automatically uses channel 10)

#### Channel
Sets the MIDI channel (1-16, converted to 0-15 internally).

```
Channel=1        # Channel 1 (default)
Channel=10       # Channel 10 (typically drums)
```

**Note**: Channel 10 is reserved for percussion in General MIDI.

## Musical Notation

### Note Format
Basic note format: `[NoteName][Accidental][Octave][Duration][Modifiers]`

#### Note Names
- `C`, `D`, `E`, `F`, `G`, `A`, `B`

#### Accidentals  
- `#` - Sharp
- `b` - Flat

#### Octaves
- Numbers 0-9 (default is 4 if omitted)
- `C4` = Middle C (MIDI note 60)

#### Duration Characters
- `w` - Whole note (4 beats)
- `h` - Half note (2 beats)  
- `q` - Quarter note (1 beat) - **default**
- `e` - Eighth note (0.5 beats)
- `s` - Sixteenth note (0.25 beats)
- `t` - Thirty-second note (0.125 beats)

### Basic Notes Examples
```
C4q          # C4 quarter note
D#5h         # D# fifth octave half note  
Bb3w         # Bb third octave whole note
A4           # A4 quarter note (default duration)
```

### Advanced Note Modifiers

#### Dotted Notes
Add `.` for dotted rhythm (1.5× duration):
```
C4h.         # Dotted half note (3 beats)
E4q.         # Dotted quarter note (1.5 beats)
```

#### Tuplets
Add `/n` for tuplets (divide duration by n):
```
C4e/3        # Eighth note triplet
D4q/5        # Quarter note quintuplet
```

#### Note Parameters
Add parameters with `:parameter` syntax:

**Velocity (Volume)**
```
C4q:v100     # Forte (loud)
D4q:v60      # Mezzo-piano (medium-quiet)
E4q:v127     # Fortissimo (very loud)
```

**Channel Override**
```
C4q:ch2      # Play on channel 2
```

**Instrument Override**
```
C4q:i42      # Play with instrument 42
```

**Timing Adjustments**
```
C4q:p0.1     # Start 0.1 beats later
D4q:p-0.05   # Start 0.05 beats earlier
```

**Note Length Override**
```
C4q:lene     # Quarter note duration, eighth note length
D4h:lens     # Half note duration, sixteenth note length
```

**Multiple Parameters**
```
C4q:v100:ch2:p0.1    # Loud, channel 2, delayed start
```

### Rests
Use `R` followed by duration:

```
Rq           # Quarter rest
Rh           # Half rest
Rw           # Whole rest
R.           # Dotted quarter rest
```

### Chords
Enclose multiple notes in square brackets, separated by commas:

```
[C4q, E4q, G4q]           # C major chord
[C3h, E3h, G3h, C4h]      # C major chord with octave
[A3q:v80, C#4q:v90, E4q:v100]  # Chord with different velocities
```

### Bar Lines
Use `|` for bar separations (optional, for readability):

```
C4q D4q E4q F4q | G4h A4h | B4w
```

Use `||` for double bar lines:

```
C4q D4q E4q F4q || G4w
```

## Control Events

### Program Change (PC)
Change instrument mid-track:

```
PC:0         # Change to acoustic piano
PC:25        # Change to steel guitar
```

### Control Change (CC)
Send MIDI control change messages:

```
CC:64:127    # Sustain pedal on
CC:64:0      # Sustain pedal off
CC:7:100     # Main volume to 100
CC:1:64      # Modulation wheel to middle
```

**Common Controllers:**
- `1` - Modulation wheel
- `7` - Main volume
- `11` - Expression
- `64` - Sustain pedal
- `91` - Reverb depth
- `93` - Chorus depth

### Pitch Bend (PB)
Send pitch bend messages:

```
PB:0         # Center (no bend)
PB:4096      # Bend up
PB:-4096     # Bend down
```

Range: -8192 to 8191 (center = 0)

### Tempo Changes
Change tempo within a track:

```
Tempo=140    # Speed up to 140 BPM
```

## Complex Examples

### Multi-Track Composition
```
Tempo=100
Key=G Major
TimeSig=4/4

Track Melody: Instrument=violin Channel=1
C4q:v90 D4q:v95 E4q:v100 F#4q | G4h A4h || B4w

Track Harmony: Instrument=piano Channel=2  
[G3h, B3h, D4h] [C3h, E3h, G3h] | [D3h, F#3h, A3h] [G3w, B3w, D4w]

Track Bass: Instrument=bass Channel=3
G2h G2h | C2h C2h | D2h D2h | G2w

Track Drums: Channel=10
C4e:v100 C4e:v80 D4e:v100 Rq C4q:v110
```

### Advanced Techniques
```
# Dotted rhythms and tuplets
C4e. D4s E4e/3 F4e/3 G4e/3 | A4q:v110 B4q:v120

# Control events with music
CC:64:127                    # Sustain on
[C3q:v60, E3q:v60, G3q:v60] Rq [D3q, F#3q, A3q]  
CC:64:0                      # Sustain off

# Instrument and tempo changes
PC:42 C4q D4q | Tempo=120 PC:0 E4q F4q
```

## Comments
Use `#` for comments (line comments only):

```
# This is a comment
Tempo=120        # End-of-line comment
Track Lead:      # Track with comment
# Another comment line
C4q D4q E4q F4q
```

## Best Practices

1. **Organization**: Use consistent track naming and group related tracks together
2. **Comments**: Document complex sections and unusual techniques
3. **Bar Lines**: Use `|` to improve readability, especially in longer compositions
4. **Consistent Formatting**: Maintain consistent spacing and parameter formatting
5. **Velocity Mapping**: Use consistent velocity ranges (e.g., 40-127) for dynamic expression
6. **Channel Planning**: Plan channel usage to avoid conflicts, reserve channel 10 for drums

## Error Handling

The parser will attempt to continue parsing even with errors, but will report warnings for:
- Invalid note names or formats
- Out-of-range MIDI values  
- Unknown instrument names
- Malformed control events

Always check the verbose output (`-v` flag) when testing new compositions.