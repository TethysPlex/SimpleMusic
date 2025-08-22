"""
Data structures for the SimpleMusic DSL parser.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any

@dataclass
class Note:
    """音符数据结构"""
    pitch: int  # MIDI pitch (0-127)
    duration: float  # 持续时间（拍数）
    start_time: float  # 开始时间（拍数）
    velocity: int = 80  # 力度
    channel: int = 0  # MIDI 通道 (0-15)
    instrument: Optional[int] = None  # 乐器
    actual_length: Optional[float] = None  # 实际延音长度

@dataclass  
class Event:
    """MIDI 事件"""
    type: str  # 'PC', 'CC', 'PB', 'Tempo'
    time: float  # 事件时间（拍数）
    channel: int  # 通道
    data: Dict[str, Any]  # 事件数据

@dataclass
class Track:
    """轨道数据"""
    name: str
    channel: int = 0
    instrument: int = 0
    notes: List[Note] = field(default_factory=list)
    events: List[Event] = field(default_factory=list)
    current_time: float = 0.0