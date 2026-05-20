import sys
import threading
import time
import sentencepiece as spm


class HeartbeatCounter:

  def __init__(self):
    self.count = 0
    self._lock = threading.Lock()

  def increment(self):
    with self._lock:
      self.count += 1

  def get_count(self):
    with self._lock:
      return self.count


def background_heartbeat(stop_event, counter):
  """This thread increments the counter as long as the GIL is properly released."""
  while not stop_event.is_set():
    counter.increment()
    sys.stdout.write(".")
    sys.stdout.flush()
    time.sleep(0.01)  # Force context switch


def test_gil_release():
  # 1. Generate heavy dummy text data to create enough load
  print("[Main] Generating heavy dummy text...")
  heavy_text = (
      "Hello, world! Testing SentencePiece GIL release behavior. " * 1000000
  )

  # 2. Load the pre-trained model
  model_path = "test_model.model"
  sp = spm.SentencePieceProcessor(model_file=model_path)

  # 3. Setup the counter and start the background heartbeat thread
  counter = HeartbeatCounter()
  stop_event = threading.Event()
  bg_thread = threading.Thread(
      target=background_heartbeat, args=(stop_event, counter)
  )
  bg_thread.daemon = True
  bg_thread.start()

  # Wait a brief moment to ensure the background thread spins up
  time.sleep(0.1)

  # 4. Execute the target C++ action where the GIL should be released
  print(
      "\n[Main] Starting SentencePiece encode... (Text length:"
      f" {len(heavy_text)})",
      flush=True,
  )
  start_time = time.time()

  tokens = sp.encode(heavy_text)

  end_time = time.time()
  elapsed_time = end_time - start_time
  print(
      f"\n[Main] Encode finished. Elapsed time: {elapsed_time:.4f} seconds",
      flush=True,
  )

  # 5. Stop and clean up the background thread
  stop_event.set()
  bg_thread.join()

  # 6. Validate GIL release by checking the background thread's activity
  heartbeat_count = counter.get_count()
  print(
      f"[Main] Background thread executed {heartbeat_count} times during C++"
      " execution."
  )

  # ASSERTION: If the GIL was locked, the background thread wouldn't have executed.
  # We expect at least a reasonable number of heartbeats based on elapsed time (e.g., > 5 times)
  min_expected_heartbeats = 100

  assert heartbeat_count >= min_expected_heartbeats, (
      "GIL Release Failure Detected! The background thread was blocked."
      f" Expected at least {min_expected_heartbeats} heartbeats, but only got"
      f" {heartbeat_count}."
  )

  assert len(tokens) > 0, "Tokenization result is empty"
  print(
      "[Main] Test passed successfully! GIL release confirmed programmatically."
  )


if __name__ == "__main__":
  test_gil_release()
