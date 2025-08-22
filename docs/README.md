# SimpleMusic Documentation

Welcome to the SimpleMusic documentation! This directory contains comprehensive documentation for the SimpleMusic DSL to MIDI converter library.

## Documentation Structure

- **[DSL Syntax](dsl-syntax.md)** - Complete reference for the SimpleMusic DSL language
- **[Examples](examples.md)** - Sample compositions and usage patterns
- **[API Reference](api-reference.md)** - Python library API documentation
- **[Getting Started](getting-started.md)** - Quick start guide for new users

## Quick Links

- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [DSL Language Overview](dsl-syntax.md#overview)

## Installation

```bash
# Install from source
pip install -e .

# Or with uv
uv pip install -e .
```

## Basic Usage

### Command Line

```bash
# Use built-in example
simplemusic --example basic -o my_song.mid

# Convert DSL file
simplemusic my_song.dsl -o output.mid
```

### Python Library

```python
from simplemusic import dsl_to_midi, EXAMPLE_BASIC

# Convert DSL text to MIDI
result = dsl_to_midi(EXAMPLE_BASIC, 'output.mid', verbose=True)
```

## DSL Overview

The SimpleMusic DSL allows you to write music using a simple text format:

```
Tempo=120
Key=C Major
TimeSig=4/4

Track Melody: Instrument=piano Channel=1
C4q D4q E4q F4q | G4h A4h | B4w

Track Bass: Instrument=bass Channel=2
C2h C2h | G2h G2h | C2w
```

For complete syntax documentation, see [DSL Syntax](dsl-syntax.md).