"""
MIDI file creation and conversion functions.
"""

from typing import Dict
from midiutil import MIDIFile

from .parser import DSLParser

def create_midi_file(parsed_data: Dict, output_file: str = 'output.mid'):
    """从解析的数据创建 MIDI 文件"""
    metadata = parsed_data.get('metadata', {})
    tracks_data = parsed_data.get('tracks', {})
    
    if not tracks_data:
        print("警告：没有找到任何轨道数据")
        return
    
    # 创建 MIDI 文件，至少需要一个轨道
    num_tracks = max(1, len(tracks_data))
    midi = MIDIFile(num_tracks, deinterleave=False)
    
    # 设置全局元数据
    tempo = metadata.get('tempo', 120)
    time_sig = metadata.get('time_sig', (4, 4))
    
    # 为每个轨道设置元数据和音符
    for track_idx, (track_name, track_data) in enumerate(tracks_data.items()):
        # 设置轨道名称
        midi.addTrackName(track_idx, 0, track_name)
        
        # 设置拍号
        midi.addTimeSignature(track_idx, 0, time_sig[0], 
                            int(2 ** (2 - time_sig[1] / 4)), 24)
        
        # 设置初始速度
        midi.addTempo(track_idx, 0, tempo)
        
        # 获取轨道配置
        config = track_data.get('config', {})
        default_channel = config.get('channel', 0)
        default_instrument = config.get('instrument', 0)
        
        # 设置默认乐器（除非是鼓轨道）
        if default_channel != 9:  # Channel 10 (index 9) 是鼓
            midi.addProgramChange(track_idx, default_channel, 0, default_instrument)
        
        # 添加音符
        notes = track_data.get('notes', [])
        for note in notes:
            # 如果音符指定了特殊乐器，先切换乐器
            if note.instrument is not None and note.channel != 9:
                midi.addProgramChange(track_idx, note.channel, note.start_time, note.instrument)
            
            # 计算实际持续时间
            actual_duration = note.actual_length if note.actual_length else note.duration
            
            # 添加音符
            try:
                midi.addNote(track_idx, note.channel, note.pitch, 
                           note.start_time, actual_duration, note.velocity)
            except Exception as e:
                print(f"警告：无法添加音符 (pitch={note.pitch}, time={note.start_time}): {e}")
        
        # 添加事件
        events = track_data.get('events', [])
        for event in events:
            try:
                if event.type == 'PC':
                    midi.addProgramChange(track_idx, event.channel, event.time, 
                                        event.data['program'])
                elif event.type == 'CC':
                    midi.addControllerEvent(track_idx, event.channel, event.time,
                                          event.data['controller'], event.data['value'])
                elif event.type == 'PB':
                    # MIDIFile 的 pitchWheelEvent 需要将值转换到 0-16383 范围
                    pb_value = event.data['value'] + 8192  # 转换从 -8192~8191 到 0~16383
                    midi.addPitchWheelEvent(track_idx, event.channel, event.time, pb_value)
                elif event.type == 'Tempo':
                    midi.addTempo(track_idx, event.time, event.data['tempo'])
            except Exception as e:
                print(f"警告：无法添加事件 {event.type}: {e}")
    
    # 写入文件
    with open(output_file, 'wb') as f:
        midi.writeFile(f)
    
    print(f"✅ MIDI 文件已生成: {output_file}")

def dsl_to_midi(dsl_text: str, output_file: str = 'output.mid', verbose: bool = False):
    """主函数：将 DSL 文本转换为 MIDI 文件"""
    try:
        parser = DSLParser(dsl_text)
        parsed_data = parser.parse()
        
        if verbose:
            print("\n📊 解析结果:")
            print(f"  元数据: {parsed_data['metadata']}")
            print(f"  轨道数: {len(parsed_data['tracks'])}")
            
            for track_name, track_data in parsed_data['tracks'].items():
                print(f"\n  轨道 '{track_name}':")
                print(f"    配置: {track_data['config']}")
                print(f"    音符数: {len(track_data.get('notes', []))}")
                print(f"    事件数: {len(track_data.get('events', []))}")
        
        create_midi_file(parsed_data, output_file)
        return parsed_data
        
    except Exception as e:
        print(f"❌ 转换失败: {e}")
        import traceback
        traceback.print_exc()
        return None