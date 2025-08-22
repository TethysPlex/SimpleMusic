#!/usr/bin/env python3
"""
Unit tests for DSL parser functionality.
"""

from simplemusic import DSLParser

def test_basic_note_parsing():
    """Test basic note parsing"""
    dsl = "Track Test: C4q D4h E4w"
    parser = DSLParser(dsl)
    result = parser.parse()
    
    track_data = result['tracks']['Test']
    notes = track_data['notes']
    
    assert len(notes) == 3, f"Expected 3 notes, got {len(notes)}"
    
    # Test first note (C4 quarter note)
    assert notes[0].pitch == 60, f"Expected pitch 60, got {notes[0].pitch}"  # C4 = 60
    assert notes[0].duration == 1.0, f"Expected duration 1.0, got {notes[0].duration}"
    
    # Test second note (D4 half note)  
    assert notes[1].pitch == 62, f"Expected pitch 62, got {notes[1].pitch}"  # D4 = 62
    assert notes[1].duration == 2.0, f"Expected duration 2.0, got {notes[1].duration}"
    
    # Test third note (E4 whole note)
    assert notes[2].pitch == 64, f"Expected pitch 64, got {notes[2].pitch}"  # E4 = 64
    assert notes[2].duration == 4.0, f"Expected duration 4.0, got {notes[2].duration}"
    
    print("✅ Basic note parsing test passed")

def test_sharps_and_flats():
    """Test sharp and flat note parsing"""
    dsl = "Track Test: C#4q Db4q"
    parser = DSLParser(dsl)
    result = parser.parse()
    
    notes = result['tracks']['Test']['notes']
    
    assert len(notes) == 2, f"Expected 2 notes, got {len(notes)}"
    assert notes[0].pitch == 61, f"Expected C# pitch 61, got {notes[0].pitch}"
    assert notes[1].pitch == 61, f"Expected Db pitch 61, got {notes[1].pitch}"
    
    print("✅ Sharps and flats test passed")

def test_chord_parsing():
    """Test chord parsing"""
    dsl = "Track Test: [C4q, E4q, G4q]"
    parser = DSLParser(dsl)
    result = parser.parse()
    
    notes = result['tracks']['Test']['notes']
    
    assert len(notes) == 3, f"Expected 3 chord notes, got {len(notes)}"
    
    # All notes should start at the same time
    assert all(note.start_time == 0.0 for note in notes), "Chord notes should start at same time"
    
    # Check pitches (C major chord)
    pitches = sorted([note.pitch for note in notes])
    expected_pitches = [60, 64, 67]  # C4, E4, G4
    assert pitches == expected_pitches, f"Expected pitches {expected_pitches}, got {pitches}"
    
    print("✅ Chord parsing test passed")

def test_rest_parsing():
    """Test rest parsing"""
    dsl = "Track Test: C4q Rh D4q"
    parser = DSLParser(dsl)
    result = parser.parse()
    
    notes = result['tracks']['Test']['notes']
    
    assert len(notes) == 2, f"Expected 2 notes (rest should not create note), got {len(notes)}"
    
    # Second note should start after the quarter note + half rest
    expected_start_time = 1.0 + 2.0  # quarter + half rest
    assert notes[1].start_time == expected_start_time, f"Expected start time {expected_start_time}, got {notes[1].start_time}"
    
    print("✅ Rest parsing test passed")

def test_instrument_and_channel():
    """Test instrument and channel parsing"""
    dsl = "Track Test: Instrument=piano Channel=2"
    parser = DSLParser(dsl)
    result = parser.parse()
    
    config = result['tracks']['Test']['config']
    
    assert config['instrument'] == 0, f"Expected piano (0), got {config['instrument']}"
    assert config['channel'] == 1, f"Expected channel 1 (0-indexed), got {config['channel']}"
    
    print("✅ Instrument and channel test passed")

def run_parser_tests():
    """Run all parser tests"""
    print("Running DSL parser tests...")
    
    try:
        test_basic_note_parsing()
        test_sharps_and_flats()
        test_chord_parsing()
        test_rest_parsing()
        test_instrument_and_channel()
        
        print("\n🎉 All parser tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Parser test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = run_parser_tests()
    exit(0 if success else 1)