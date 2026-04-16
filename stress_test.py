import time
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_stress_test(num_tracks=5000):
    logging.info(f"🚀 Starting Stress Test with {num_tracks} simulated tracks...")
    start_time = time.time()
    
    # 1. Generate Massive Mock Data
    mock_playlist = []
    for i in range(num_tracks):
        mock_playlist.append({
            "id": f"track_{i}",
            "name": f"Generated Song {i}",
            "artist": "Test Artist",
            "duration_ms": random.randint(120000, 300000)
        })
    logging.info(f"✅ Generated {len(mock_playlist)} mock tracks in {time.time() - start_time:.2f}s")
    
    # 2. Simulate heavy processing (e.g., duplicate checking logic)
    process_start = time.time()
    seen = set()
    duplicates = 0
    for track in mock_playlist:
        # Artificial delay to simulate DB/Memory lookup per track
        time.sleep(0.0001) 
        if track["id"] in seen:
            duplicates += 1
        else:
            seen.add(track["id"])
            
    logging.info(f"✅ Processing complete. Simulated {duplicates} duplicates.")
    logging.info(f"⏱️ Total Execution Time: {time.time() - start_time:.2f}s")
    
    # 3. Validate Network Disconnect Handling
    try:
        logging.info("🔌 Testing simulated network failure (Timeout)...")
        # Replace this with your actual API call wrapped in a try/except
        raise ConnectionError("Simulated Internet Disconnect")
    except ConnectionError as e:
        logging.error(f"Caught expected error: {e}. Ensure your UI displays an offline warning here instead of crashing.")

if __name__ == "__main__":
    run_stress_test(5000)
