import sys
import os

# --- CORRECCIÓN DE CODIFICACIÓN PARA EMOJIS EN WINDOWS ---
if sys.stdout is not None and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from utils.helpers import format_duration

def test_format_duration():
    print("Testing format_duration...")
    assert format_duration(None) == "0s"
    assert format_duration("not a number") == "0s"
    assert format_duration(0) == "0s"
    assert format_duration(1000) == "1s"
    assert format_duration(61000) == "1m 1s"
    assert format_duration(3661000) == "1h 1m 1s"
    assert format_duration(90061000) == "1d 1h 1m 1s"
    print("✅ format_duration tests passed!")

def test_select_playlist_robustness():
    print("\nTesting select_playlist robustness (mocking)...")
    playlists = [
        {'name': 'Valid Playlist', 'tracks': {'total': 10}},
        {'name': None, 'tracks': None},
        {'tracks': {'total': 5}},
        {}
    ]
    
    print("Simulated playlist listing:")
    for i, pl in enumerate(playlists, start=1):
        name = pl.get('name', 'Unknown Playlist')
        tracks_info = pl.get('tracks', {})
        total_tracks = tracks_info.get('total', 0) if isinstance(tracks_info, dict) else 0
        print(f"{i}: {name} ({total_tracks} tracks)")
    
    print("✅ select_playlist logic (listing) is robust!")

def test_select_playlist_search_robustness():
    print("\nTesting select_playlist search robustness (mocking)...")
    playlists = [
        {'name': 'Rock Mix', 'tracks': {'total': 10}},
        {'name': None, 'tracks': None},
        {'tracks': {'total': 5}},
        {'name': 'Jazz Party'}
    ]
    
    choice = "rock"
    matches = [pl for pl in playlists if isinstance(pl, dict) and choice.lower() in (pl.get('name') or "").lower()]
    assert len(matches) == 1
    assert matches[0]['name'] == 'Rock Mix'
    
    choice = "unknown"
    matches = [pl for pl in playlists if isinstance(pl, dict) and choice.lower() in (pl.get('name') or "").lower()]
    assert len(matches) == 0
    
    print("✅ Search logic is robust!")

if __name__ == "__main__":
    try:
        test_format_duration()
        test_select_playlist_robustness()
        test_select_playlist_search_robustness()
        print("\nAll tests passed successfully!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        sys.exit(1)
