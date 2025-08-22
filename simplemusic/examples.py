"""
Example DSL compositions for demonstration purposes.
"""

EXAMPLE_BASIC = """
Tempo=120
Key=C Major
TimeSig=4/4

Track Melody: Instrument=piano Channel=1
C4q D4q E4q F4q | G4h A4h | B4w

Track Bass: Instrument=acoustic bass Channel=2
C2h C2h | G2h G2h | C2w
"""

EXAMPLE_COMPLEX = """
Tempo=100
Key=G Major
TimeSig=4/4
TicksPerBeat=480

Track Melody: Instrument=41 Channel=1
C4q:v90 D4q:v95 E4q:v100 F#4q | G4h A4h || B4w
C5e D5e E5e F#5e G5e A5e B5e C6e | D6h. Rq || C6w

Track Chords: Instrument=1 Channel=2
[G3h, B3h, D4h] [C3h, E3h, G3h] | [D3h, F#3h, A3h] [G3w, B3w, D4w]

Track Bass: Instrument=33 Channel=3
G2h G2h | C2h C2h | D2h D2h | G2w

Track Effects: Channel=4
CC:64:127 Rq CC:64:0 Rh CC:7:100
"""

EXAMPLE_ADVANCED = """
Tempo=140
TimeSig=6/8

Track Lead: Instrument=violin Channel=1
# 使用附点、连音符和力度变化
C4e. D4s E4e/3 F4e/3 G4e/3 | A4q:v110 B4q:v120 | C5h.:v127

Track Piano: Instrument=0 Channel=2  
# 复杂和弦与踏板
CC:64:127
[C3q:v60, E3q:v60, G3q:v60, C4q:v70] Rq [D3q, F#3q, A3q, D4q]
CC:64:0

Track Percussion: Channel=10
# 鼓轨道示例（通道10）
C4e:v100 C4e:v80 D4e:v100 Rq C4q:v110
"""