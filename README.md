# Puzzle Decoder Race - High-Performance Solution

A Python solution for the Puzzle Decoder Race challenge that fetches puzzle fragments concurrently and assembles them as fast as possible.

## 🚀 Features

- **Concurrent Fragment Fetching**: Uses asyncio and aiohttp for high-performance parallel requests
- **Smart Search Strategy**: Multi-phase approach to discover puzzle structure efficiently
- **Optimized Connection Management**: Persistent connections and connection pooling
- **Completion Detection**: Intelligent algorithm to detect when puzzle is complete
- **Sub-second Performance**: Optimized to complete puzzles in under 1 second

## 📋 Requirements

- Python 3.7+
- aiohttp library
- mypy (optional, for type checking)
- Docker (for running the puzzle server)

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/dherreraa1/puzzle-decoder-race.git
   cd puzzle-decoder-race
   ```

2. **Install dependencies**:
   ```bash
   pip install aiohttp
   # Optional: for type checking
   pip install mypy
   ```

3. **Type checking** (optional):
   ```bash
   mypy decoder.py
   ```

4. **Start the puzzle server**:
   ```bash
   docker run -p 8080:8080 ifajardov/puzzle-server
   ```

## 🎯 How to Run

1. **Ensure the server is running** on `localhost:8080` or `localhost:8888` 
2. **Run the puzzle decoder**:
   ```bash
   python decoder.py
   ```

## 🧠 Strategy for Speed and Correctness

### Multi-Phase Search Strategy

**Phase 1: Initial Discovery**
- Performs random sampling across a wide ID range (1-1000)
- Uses concurrent requests to quickly discover puzzle structure
- Identifies the approximate size and indices of the puzzle

**Phase 2: Gap Filling**
- Analyzes discovered fragments to identify missing indices
- Performs targeted searches for missing pieces
- Uses the fact that puzzle indices are consecutive starting from 0

**Phase 3: Extended Search**
- Fallback strategy for edge cases
- Systematic search with early termination
- Handles puzzles with unusual ID distributions

### Performance Optimizations

1. **Concurrent Requests**: Up to 20 parallel requests using asyncio
2. **Connection Pooling**: Reuses HTTP connections to minimize overhead
3. **Smart Caching**: Tracks seen IDs to avoid duplicate requests
4. **Early Termination**: Stops as soon as puzzle is complete
5. **Efficient Data Structures**: Uses dictionaries for O(1) lookups

### Completion Detection

The algorithm detects completion by checking for a consecutive sequence of fragments starting from index 0:
- Maintains fragments in a dictionary keyed by index
- Checks for gaps in the sequence (0, 1, 2, ..., max_index)
- Declares complete when no gaps exist

## ⚡ Performance Results

**Target**: Complete puzzle in under 1 second
**Typical Performance**: 500-600ms 

### Optimization Techniques Used:

- **Batch Processing**: Groups multiple requests together
- **Connection Reuse**: Maintains persistent HTTP connections
- **Parallel Execution**: Maximizes network utilization
- **Smart Sampling**: Reduces total number of requests needed

## 🏆 Bonus Achievement

✅ **YES** - This solution completes the puzzle in under 1 second

The combination of concurrent requests, smart search strategy, and optimized connection handling typically results in completion times between 500-600ms, under the 1-second bonus threshold.

## 🔧 Configuration

You can adjust performance parameters in the `PuzzleDecoder` class:

```python
self.max_concurrent = 30  # Number of concurrent requests
self.timeout = 5.0        # Request timeout in seconds
```

## 📊 Example Output

```
🧩 Starting Puzzle Decoder Race...
Phase 1: Initial discovery...
Found fragment 0: 'This'
Found fragment 1: 'is'
Found fragment 2: 'a'
Found fragment 3: 'test'

Puzzle Complete!
Message: 'This is a test'
Time: 0.423 seconds
Total fragments: 4
Requests made: 27
BONUS ACHIEVED: Completed in under 1 second!

Final Answer: This is a test
```

## 🧪 Testing

The solution has been tested with:
- `self.max_concurrent` set to 30 (under this value, bonus was not achieved) and `self.timeout` to 5.0 
- **Type checking with mypy**: Passes type checking
- **Error handling**: Basic exception handling with informative messages

## 📈 Scalability

The solution scales well because:
- Concurrent requests increase throughput
- Connection pooling minimizes overhead
- Early termination prevents unnecessary work

## 🔍 Error Handling

- Proper resource cleanup
- Informative error messages

## 🏗️ Architecture

```
PuzzleDecoder
├── fetch_fragment()      # Single fragment fetching
├── fetch_batch()         # Concurrent batch fetching
├── smart_search_strategy() # Multi-phase search logic
├── is_puzzle_complete()  # Completion detection
└── get_assembled_message() # Final assembly
```