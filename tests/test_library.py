#!/usr/bin/env python3
"""
Basic functionality tests for SimpleMusic library.
"""

import tempfile
import os

from simplemusic import dsl_to_midi, EXAMPLE_BASIC, EXAMPLE_COMPLEX, EXAMPLE_ADVANCED

def test_basic_example():
    """Test basic example conversion"""
    with tempfile.TemporaryDirectory() as temp_dir:
        output_file = os.path.join(temp_dir, 'test_basic.mid')
        result = dsl_to_midi(EXAMPLE_BASIC, output_file, verbose=False)
        
        assert result is not None, "Basic example conversion failed"
        assert os.path.exists(output_file), "Output MIDI file was not created"
        assert len(result['tracks']) == 2, "Expected 2 tracks"
        print("✅ Basic example test passed")

def test_complex_example():
    """Test complex example conversion"""
    with tempfile.TemporaryDirectory() as temp_dir:
        output_file = os.path.join(temp_dir, 'test_complex.mid')
        result = dsl_to_midi(EXAMPLE_COMPLEX, output_file, verbose=False)
        
        assert result is not None, "Complex example conversion failed"
        assert os.path.exists(output_file), "Output MIDI file was not created"
        assert len(result['tracks']) == 4, "Expected 4 tracks"
        print("✅ Complex example test passed")

def test_advanced_example():
    """Test advanced example conversion"""
    with tempfile.TemporaryDirectory() as temp_dir:
        output_file = os.path.join(temp_dir, 'test_advanced.mid')
        result = dsl_to_midi(EXAMPLE_ADVANCED, output_file, verbose=False)
        
        assert result is not None, "Advanced example conversion failed"
        assert os.path.exists(output_file), "Output MIDI file was not created"
        assert len(result['tracks']) == 3, "Expected 3 tracks"
        print("✅ Advanced example test passed")

def test_metadata_parsing():
    """Test metadata parsing"""
    result = dsl_to_midi(EXAMPLE_COMPLEX, tempfile.mktemp(suffix='.mid'), verbose=False)
    
    metadata = result['metadata']
    assert metadata['tempo'] == 100, f"Expected tempo 100, got {metadata['tempo']}"
    assert metadata['key'] == 'G Major', f"Expected key G Major, got {metadata['key']}"
    assert metadata['time_sig'] == (4, 4), f"Expected (4,4) time sig, got {metadata['time_sig']}"
    print("✅ Metadata parsing test passed")

def run_all_tests():
    """Run all tests"""
    print("Running SimpleMusic library tests...")
    
    try:
        test_basic_example()
        test_complex_example() 
        test_advanced_example()
        test_metadata_parsing()
        
        print("\n🎉 All tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)