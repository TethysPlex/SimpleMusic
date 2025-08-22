"""
DSL Parser for SimpleMusic notation.
"""

import re
from typing import List, Dict, Optional, Tuple

from .constants import NOTE_MAP, DURATION_MAP, INSTRUMENT_NAMES
from .data_structures import Note, Event, Track

class DSLParser:
    def __init__(self, dsl_text: str):
        self.lines = []
        self.tempo = 120
        self.key = 'C Major'
        self.time_sig = (4, 4)
        self.ticks_per_beat = 480
        self.tracks = {}
        self.current_track_name = None
        
        # 预处理：合并多行轨道内容
        self._preprocess_lines(dsl_text)
        
    def _preprocess_lines(self, dsl_text: str):
        """预处理输入文本，合并轨道内容"""
        raw_lines = dsl_text.strip().split('\n')
        processed_lines = []
        current_track = None
        track_content = []
        
        for line in raw_lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            # 检查是否是元数据
            if any(line.startswith(x) for x in ['Tempo=', 'Key=', 'TimeSig=', 'TicksPerBeat=']):
                if current_track and track_content:
                    # 保存之前的轨道内容
                    processed_lines.append(f"{current_track}: {' '.join(track_content)}")
                    track_content = []
                    current_track = None
                processed_lines.append(line)
            # 检查是否是新轨道定义
            elif line.startswith('Track '):
                if current_track and track_content:
                    # 保存之前的轨道内容
                    processed_lines.append(f"{current_track}: {' '.join(track_content)}")
                    track_content = []
                
                # 解析轨道定义
                if ':' in line:
                    track_def, content = line.split(':', 1)
                    current_track = track_def
                    processed_lines.append(track_def + ':')
                    if content.strip():
                        # 检查是否是配置还是音符
                        if any(x in content for x in ['Instrument=', 'Channel=']):
                            processed_lines[-1] = track_def + ':' + content
                        else:
                            track_content.append(content.strip())
                else:
                    current_track = line
                    processed_lines.append(line + ':')
            # 其他内容属于当前轨道
            elif current_track:
                track_content.append(line)
            else:
                # 如果没有轨道定义，创建默认轨道
                if 'Default' not in [l.split(':')[0].replace('Track ', '').strip() 
                                    for l in processed_lines if l.startswith('Track ')]:
                    processed_lines.append('Track Default: Instrument=0 Channel=1')
                    current_track = 'Track Default'
                track_content.append(line)
        
        # 保存最后的轨道内容
        if current_track and track_content:
            processed_lines.append(f"{current_track}: {' '.join(track_content)}")
        
        self.lines = processed_lines
        
    def parse(self) -> Dict:
        """解析 DSL 文本"""
        # 第一遍：解析元数据和轨道定义
        for line in self.lines:
            if line.startswith('Tempo='):
                self.tempo = int(line.split('=')[1])
            elif line.startswith('Key='):
                self.key = line.split('=', 1)[1]
            elif line.startswith('TimeSig='):
                parts = line.split('=')[1].split('/')
                self.time_sig = (int(parts[0]), int(parts[1]))
            elif line.startswith('TicksPerBeat='):
                self.ticks_per_beat = int(line.split('=')[1])
            elif line.startswith('Track '):
                self._parse_track_line(line)
        
        # 返回结果
        result = {
            'metadata': {
                'tempo': self.tempo,
                'key': self.key,
                'time_sig': self.time_sig,
                'ticks_per_beat': self.ticks_per_beat
            },
            'tracks': {}
        }
        
        for track_name, track in self.tracks.items():
            result['tracks'][track_name] = {
                'config': {
                    'channel': track.channel,
                    'instrument': track.instrument
                },
                'notes': track.notes,
                'events': track.events
            }
        
        return result
    
    def _parse_track_line(self, line: str):
        """解析轨道行（包括定义和内容）"""
        # 分离轨道名称和内容
        if ':' in line:
            header, content = line.split(':', 1)
            track_name = header.replace('Track ', '').strip()
            
            # 如果轨道不存在，创建它
            if track_name not in self.tracks:
                self.tracks[track_name] = Track(name=track_name)
            
            track = self.tracks[track_name]
            content = content.strip()
            
            # 检查是否包含配置
            if 'Instrument=' in content or 'Channel=' in content:
                # 解析配置
                config_parts = content.split()
                for part in config_parts:
                    if '=' in part:
                        key, value = part.split('=', 1)
                        if key == 'Instrument':
                            if value.isdigit():
                                track.instrument = int(value)
                            else:
                                track.instrument = INSTRUMENT_NAMES.get(value.lower(), 0)
                        elif key == 'Channel':
                            track.channel = int(value) - 1
                
                # 移除配置部分，保留音符序列
                for cfg in ['Instrument=', 'Channel=']:
                    content = re.sub(rf'{cfg}\S+\s*', '', content)
            
            # 解析音符序列
            if content:
                self._parse_sequence(content, track)
    
    def _parse_sequence(self, sequence: str, track: Track):
        """解析音符序列"""
        # 使用更复杂的正则表达式来分割token
        # 匹配和弦、音符、休止符、事件等
        pattern = r'\[[^\]]+\]|[A-GR][#b]?\d*[whqest]?\.?(?:/\d+)?(?::[^:\s]+)*|PC:[^:\s]+|CC:[^:\s]+:[^:\s]+|PB:[^:\s]+|Tempo=\d+|\|+'
        
        tokens = re.findall(pattern, sequence)
        
        for token in tokens:
            token = token.strip()
            if not token or token in ['|', '||']:
                continue
            elif token.startswith('R'):
                # 休止符
                rest_match = re.match(r'R([whqest]\.?(?:/\d+)?)', token)
                if rest_match:
                    duration = self._parse_duration(rest_match.group(1))
                    track.current_time += duration
            elif token.startswith('['):
                # 和弦
                self._parse_chord(token, track)
            elif token.startswith('PC:'):
                # Program Change
                program = int(token.split(':')[1])
                track.events.append(Event('PC', track.current_time, track.channel, 
                                        {'program': program}))
            elif token.startswith('CC:'):
                # Control Change
                parts = token.split(':')
                if len(parts) >= 3:
                    controller = int(parts[1])
                    value = int(parts[2])
                    track.events.append(Event('CC', track.current_time, track.channel,
                                            {'controller': controller, 'value': value}))
            elif token.startswith('PB:'):
                # Pitch Bend
                value = int(token.split(':')[1])
                track.events.append(Event('PB', track.current_time, track.channel,
                                        {'value': value}))
            elif token.startswith('Tempo='):
                # Tempo Change
                new_tempo = int(token.split('=')[1])
                track.events.append(Event('Tempo', track.current_time, track.channel,
                                        {'tempo': new_tempo}))
            else:
                # 单个音符
                note = self._parse_note(token, track)
                if note:
                    track.notes.append(note)
                    track.current_time += note.duration
    
    def _parse_chord(self, chord_str: str, track: Track):
        """解析和弦"""
        # 移除方括号
        chord_content = chord_str.strip('[]')
        # 分割音符
        note_strs = [n.strip() for n in chord_content.split(',')]
        
        chord_duration = 0
        chord_notes = []
        
        for note_str in note_strs:
            note = self._parse_note(note_str, track, is_chord=True)
            if note:
                chord_notes.append(note)
                chord_duration = max(chord_duration, note.duration)
        
        # 将和弦音符添加到轨道
        track.notes.extend(chord_notes)
        
        # 更新时间（和弦的所有音符同时开始，所以只增加一次时间）
        if chord_duration > 0:
            track.current_time += chord_duration
    
    def _parse_note(self, note_str: str, track: Track, is_chord: bool = False) -> Optional[Note]:
        """解析单个音符"""
        # 分离基础音符和参数
        parts = note_str.split(':')
        note_base = parts[0]
        
        # 解析参数
        params = self._parse_note_params(parts[1:])
        
        # 解析音高和时值
        # 改进的正则表达式，支持更多格式
        match = re.match(r'([A-G])([#b]?)(\d+)?([whqest])?(\.)?(/\d+)?', note_base)
        if not match:
            return None
        
        note_name = match.group(1) + (match.group(2) or '')
        octave = int(match.group(3)) if match.group(3) else 4
        duration_char = match.group(4) or 'q'
        dotted = match.group(5) == '.'
        tuplet = match.group(6)
        
        # 计算 MIDI 音高
        pitch = self._note_to_midi(note_name, octave)
        
        # 计算时值
        duration = self._parse_duration(duration_char)
        
        # 应用修饰符
        if dotted or params.get('dotted'):
            duration *= 1.5
        
        if tuplet:
            tuplet_num = int(tuplet[1:])
            duration /= tuplet_num
        elif params.get('tuplet'):
            duration /= params['tuplet']
        
        # 应用参数中的时值修饰
        if 'd' in params.get('duration_mod', ''):
            duration *= 1.5
        
        # 创建音符
        note = Note(
            pitch=pitch,
            duration=duration,
            start_time=track.current_time + params.get('position', 0),
            velocity=params.get('velocity', 80),
            channel=params.get('channel', track.channel),
            instrument=params.get('instrument'),
            actual_length=params.get('actual_length')
        )
        
        return note
    
    def _parse_note_params(self, param_parts: List[str]) -> Dict:
        """解析音符参数"""
        params = {}
        
        for param in param_parts:
            if not param:
                continue
                
            if param.startswith('v') and param[1:].isdigit():
                params['velocity'] = int(param[1:])
            elif param.startswith('ch') and param[2:].isdigit():
                params['channel'] = int(param[2:]) - 1
            elif param.startswith('i') and param[1:].isdigit():
                params['instrument'] = int(param[1:])
            elif param.startswith('t'):
                params['duration_mod'] = param[1:]
            elif param.startswith('p') and param[1:].replace('.', '').replace('-', '').isdigit():
                params['position'] = float(param[1:])
            elif param.startswith('len'):
                duration_str = param[3:]
                params['actual_length'] = self._parse_duration(duration_str)
            elif param == 'd':
                params['dotted'] = True
            elif '/' in param and param.replace('/', '').isdigit():
                params['tuplet'] = int(param.split('/')[1])
        
        return params
    
    def _note_to_midi(self, note_name: str, octave: int) -> int:
        """转换音符名称到 MIDI 音高"""
        base_note = note_name[0]
        midi_note = NOTE_MAP[base_note] + (octave + 1) * 12
        
        # 处理升降号
        if len(note_name) > 1:
            if note_name[1] == '#':
                midi_note += 1
            elif note_name[1] == 'b':
                midi_note -= 1
        
        return max(0, min(127, midi_note))  # 确保在 MIDI 范围内
    
    def _parse_duration(self, duration_str: str) -> float:
        """解析时值字符串"""
        if not duration_str:
            return 1.0
        
        # 提取基础时值字符
        base_char = duration_str[0] if duration_str else 'q'
        
        if base_char in DURATION_MAP:
            duration = DURATION_MAP[base_char]
            
            # 检查附点
            if '.' in duration_str:
                duration *= 1.5
            
            # 检查连音符
            if '/' in duration_str:
                tuplet_match = re.search(r'/(\d+)', duration_str)
                if tuplet_match:
                    duration /= int(tuplet_match.group(1))
            
            return duration
        
        return 1.0  # 默认四分音符