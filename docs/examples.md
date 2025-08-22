# SimpleMusic Examples

This document provides a collection of example compositions demonstrating various features of the SimpleMusic DSL.

## Table of Contents

1. [Basic Examples](#basic-examples)
2. [Intermediate Examples](#intermediate-examples)  
3. [Advanced Examples](#advanced-examples)
4. [Genre-Specific Examples](#genre-specific-examples)
5. [Technical Examples](#technical-examples)

## Basic Examples

### Simple Melody
A basic single-track melody in C Major.

```
Tempo=120
Key=C Major
TimeSig=4/4

Track Melody: Instrument=piano Channel=1
C4q D4q E4q F4q | G4h A4h | B4w
```

**Features demonstrated:**
- Basic note notation
- Single track composition
- Standard metadata settings

### Two-Part Harmony
Melody with bass accompaniment.

```
Tempo=100
Key=G Major
TimeSig=4/4

Track Melody: Instrument=violin Channel=1
G4q A4q B4q C5q | D5h E5h | F#5w

Track Bass: Instrument=bass Channel=2
G2h G2h | C3h C3h | D3w
```

**Features demonstrated:**
- Multiple tracks
- Different instruments
- Different octaves

## Intermediate Examples

### Chord Progressions
Using chords with different voicings.

```
Tempo=90
Key=C Major
TimeSig=4/4

Track Piano: Instrument=piano Channel=1
# I - vi - IV - V progression
[C4q, E4q, G4q] [A3q, C4q, E4q] [F3q, A3q, C4q] [G3q, B3q, D4q] |
[C4h, E4h, G4h] [G3h, B3h, D4h] | [C4w, E4w, G4w]

Track Melody: Instrument=flute Channel=2  
Rw | G4q A4q B4q C5q | D5w
```

**Features demonstrated:**
- Chord notation with brackets
- Roman numeral harmony (I-vi-IV-V)
- Melody over chords
- Rest notation

### Dotted Rhythms and Tuplets
Complex rhythmic patterns.

```
Tempo=140
Key=F Major
TimeSig=4/4

Track Rhythm: Instrument=guitar Channel=1
# Dotted quarter followed by eighth
F4q. G4e A4q. Bb4e | C5h. Rq |
# Triplets
F4e/3 G4e/3 A4e/3 Bb4e/3 C5e/3 D5e/3 E5q F5q
```

**Features demonstrated:**
- Dotted notes (`.`)
- Tuplets (`/3`)
- Mixed rhythmic patterns

### Dynamic Expression
Using velocity for musical expression.

```
Tempo=80
Key=D Minor
TimeSig=4/4

Track Expressive: Instrument=cello Channel=1
# Crescendo effect
D4q:v40 E4q:v50 F4q:v60 G4q:v70 |
A4q:v80 Bb4q:v90 C5q:v100 D5q:v110 |
# Diminuendo
D5q:v100 C5q:v90 Bb4q:v80 A4q:v70 | G4w:v60
```

**Features demonstrated:**
- Velocity parameters (`:v40`, `:v100`)
- Dynamic changes over time
- Musical phrasing

## Advanced Examples

### Multi-Instrument Ensemble
Complete band arrangement.

```
Tempo=120
Key=A Major
TimeSig=4/4

Track Lead: Instrument=electric guitar Channel=1
A4q:v100 C#5q:v95 E5q:v100 A5q:v110 | 
F#5h:v100 E5h:v90 | D5w:v80

Track Rhythm: Instrument=electric guitar clean Channel=2
# Strummed chords
[A3e, C#4e, E4e] [A3e, C#4e, E4e] [A3e, C#4e, E4e] [A3e, C#4e, E4e] |
[D3e, F#3e, A3e] [D3e, F#3e, A3e] [E3e, G#3e, B3e] [E3e, G#3e, B3e] |
[A3w, C#4w, E4w]

Track Bass: Instrument=electric bass Channel=3
A2q Rq A2e A2e Rq | D2q Rq E2q Rq | A2w

Track Drums: Channel=10
# Basic rock pattern
C4e:v100 C4e:v80 D4e:v100 C4e:v80 C4e:v90 C4e:v80 D4e:v100 C4e:v80
```

**Features demonstrated:**
- Multiple guitar parts
- Drum programming on channel 10
- Complex chord voicings
- Rhythm section coordination

### Control Events and Automation
Using MIDI control events for expression.

```
Tempo=110
Key=Eb Major
TimeSig=4/4

Track Expressive: Instrument=synth strings Channel=1
# Start with sustain pedal
CC:64:127
Eb4w | Ab4w | Bb4w | Eb5w |
# Release sustain
CC:64:0
# Add modulation
CC:1:64
Eb5q Ab5q Bb5q Eb6q
# Remove modulation  
CC:1:0

# Volume swells
CC:7:40 F4w CC:7:127
CC:7:40 G4w CC:7:127
```

**Features demonstrated:**
- Sustain pedal (CC:64)
- Modulation wheel (CC:1)
- Volume automation (CC:7)
- Long sustained notes

### Pitch Bending
Guitar-style bend effects.

```
Tempo=100
Key=E Minor
TimeSig=4/4

Track Guitar: Instrument=electric guitar Channel=1
# Standard bend up
E4h PB:2048 PB:0 |
# Pre-bend and release
PB:2048 G4q PB:0 F#4q E4h |
# Vibrato effect
A4w PB:512 PB:-512 PB:512 PB:-512 PB:0
```

**Features demonstrated:**
- Pitch bend events (PB:value)
- Bend and release techniques
- Vibrato simulation

## Genre-Specific Examples

### Classical Style
Bach-inspired counterpoint.

```
Tempo=100
Key=C Major
TimeSig=4/4

Track Soprano: Instrument=choir Channel=1
C5q D5q E5q F5q | G5h F5q E5q | D5h C5h | C5w

Track Alto: Instrument=choir Channel=2
E4q F4q G4q A4q | Bb4h A4q G4q | F4h E4h | E4w

Track Tenor: Instrument=choir Channel=3
G3q A3q Bb3q C4q | D4h C4q Bb3q | A3h G3h | G3w

Track Bass: Instrument=choir Channel=4
C3q D3q E3q F3q | G3h F3q E3q | D3h C3h | C3w
```

### Jazz Chord Progression
ii-V-I with extensions.

```
Tempo=120
Key=Bb Major
TimeSig=4/4

Track Piano: Instrument=electric piano Channel=1
# Cm7 - F7 - BbMaj7 - EbMaj7
[C4e, Eb4e, G4e, Bb4e] [F3e, A3e, C4e, Eb4e] |
[Bb3e, D4e, F4e, A4e] [Eb3e, G3e, Bb3e, D4e] |

Track Bass: Instrument=bass Channel=2
# Walking bass line
C3q D3q Eb3q E3q | F3q G3q Ab3q A3q |
Bb3q C4q D4q Eb4q | E4q F4q G4q Ab4q
```

### Electronic Dance Music
Four-on-the-floor with synthesized elements.

```
Tempo=128
Key=C Minor
TimeSig=4/4

Track Kick: Channel=10
C4q C4q C4q C4q | C4q C4q C4q C4q

Track Snare: Channel=10  
Rq D4q:v100 Rq D4q:v100 | Rq D4q:v100 Rq D4q:v100

Track Hihat: Channel=10
F#4e:v60 F#4e:v40 F#4e:v60 F#4e:v40 F#4e:v60 F#4e:v40 F#4e:v60 F#4e:v40

Track Synth: Instrument=synth lead Channel=1
# Staccato pattern
C4s:v100 Rs Eb4s:v100 Rs G4s:v100 Rs C5s:v100 Rs |
Bb4s:v100 Rs G4s:v100 Rs Eb4s:v100 Rs C4s:v100 Rs
```

## Technical Examples

### Polyrhythm
3-against-2 rhythmic pattern.

```
Tempo=90
TimeSig=4/4

Track Three: Instrument=marimba Channel=1
# Three notes per measure (dotted half notes)
C4h. E4h. | G4h. C5h.

Track Two: Instrument=vibraphone Channel=2  
# Two notes per measure (half notes)
C3h G3h | C4h G4h
```

### Metric Modulation
Changing time signatures.

```
Tempo=120
TimeSig=4/4

Track Demo: Instrument=piano Channel=1
# 4/4 section
C4q D4q E4q F4q | G4q A4q B4q C5q |

# Change to 3/4
TimeSig=3/4
D5q. E5e F5q | G5h A5q | B5h. |

# Back to 4/4  
TimeSig=4/4
C6w
```

### Microtiming and Humanization
Subtle timing variations.

```
Tempo=100
TimeSig=4/4

Track Human: Instrument=piano Channel=1
# Slightly ahead of beat
C4q:p-0.02 D4q:p0.01 E4q:p-0.01 F4q:p0.02 |
# Behind the beat for laid-back feel
G4q:p0.05 A4q:p0.03 B4q:p0.04 C5q:p0.02
```

**Features demonstrated:**
- Position adjustments (`:p` parameter)
- Positive and negative timing offsets
- Humanization techniques

## Usage Tips

### Running Examples
All examples can be tested using the built-in CLI:

```bash
# Save example to file
echo "example_content_here" > my_song.dsl

# Convert to MIDI
simplemusic my_song.dsl -o my_song.mid -v
```

### Modifying Examples
1. **Tempo**: Experiment with different tempos (60-200 BPM range)
2. **Instruments**: Try different instrument names or numbers
3. **Keys**: Transpose by changing the Key metadata
4. **Dynamics**: Add velocity parameters for expression
5. **Effects**: Include control change events for realism

### Best Practices from Examples
1. **Use bar lines** (`|`) to organize music visually
2. **Comment complex sections** with `#` for clarity  
3. **Plan channel usage** to avoid conflicts
4. **Layer tracks gradually** from simple to complex
5. **Test frequently** while composing to catch errors early