#!/usr/bin/env python3
"""
Puzzle Decoder Race - High-Performance Solution
Fetches puzzle fragments concurrently and assembles them as fast as possible.
"""

import asyncio
import aiohttp
import time
import random
from typing import Dict, Optional, Set
from dataclasses import dataclass

@dataclass
class Fragment:
    """Represents a puzzle fragment"""
    id: int
    index: int
    text: str


class PuzzleDecoder:
    """High-performance puzzle decoder with concurrent fragment fetching"""
    
    def __init__(self, base_url: str = "http://localhost:8888"): # try 8080/8888
        self.base_url = base_url
        self.fragments: Dict[int, Fragment] = {}  # index -> fragment
        self.seen_ids: Set[int] = set()
        self.max_concurrent = 30  # Concurrent requests
        self.timeout = 5.0  # Request timeout
        
    async def fetch_fragment(self, session: aiohttp.ClientSession, fragment_id: int) -> Optional[Fragment]:
        """Fetch a single fragment from the server"""
        if fragment_id in self.seen_ids:
            return None
            
        try:
            url = f"{self.base_url}/fragment?id={fragment_id}"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    fragment = Fragment(
                        id=data['id'],
                        index=data['index'],
                        text=data['text']
                    )
                    self.seen_ids.add(fragment_id)
                    return fragment
        except Exception as e:
            print(f"Error fetching fragment {fragment_id}: {e}")
        return None
    
    async def fetch_batch(self, session: aiohttp.ClientSession, start_id: int, batch_size: int) -> list:
        """Fetch a batch of fragments concurrently"""
        tasks = []
        for i in range(batch_size):
            fragment_id = start_id + i
            task = asyncio.create_task(self.fetch_fragment(session, fragment_id))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [r for r in results if isinstance(r, Fragment)]
    
    def is_puzzle_complete(self) -> bool:
        """Check if we have a complete sequence starting from index 0"""
        if not self.fragments:
            return False
            
        # Check for consecutive sequence starting from 0
        max_index = max(self.fragments.keys())
        for i in range(max_index + 1):
            if i not in self.fragments:
                return False
        return True
    
    def get_assembled_message(self) -> str:
        """Assemble the complete message from fragments"""
        if not self.is_puzzle_complete():
            return ""
        
        sorted_fragments = sorted(self.fragments.items())
        return ' '.join(fragment.text for _, fragment in sorted_fragments)
    
    async def smart_search_strategy(self, session: aiohttp.ClientSession):
        """Smart search strategy combining multiple approaches"""
        
        # Phase 1: Random sampling to discover the puzzle structure
        print("Phase 1: Initial discovery...")
        random_ids = random.sample(range(1, 1000), min(50, 1000))
        
        batch_size = min(self.max_concurrent, len(random_ids))
        for i in range(0, len(random_ids), batch_size):
            batch = random_ids[i:i + batch_size]
            fragments = await self.fetch_batch(session, batch[0], len(batch))
            
            for fragment in fragments:
                if fragment:
                    self.fragments[fragment.index] = fragment
                    print(f"Found fragment {fragment.index}: '{fragment.text}'")
            
            if self.is_puzzle_complete():
                return
        
        # Phase 2: Fill gaps in discovered sequence
        print("Phase 2: Filling gaps...")
        if self.fragments:
            max_discovered = max(self.fragments.keys())
            missing_indices = []
            
            for i in range(max_discovered + 1):
                if i not in self.fragments:
                    missing_indices.append(i)
            
            if missing_indices:
                # Use a wider search range for missing pieces
                search_range = range(1, 10000)
                remaining_ids = [id for id in search_range if id not in self.seen_ids]
                
                # Search in batches until we find all missing pieces
                for i in range(0, len(remaining_ids), self.max_concurrent):
                    if self.is_puzzle_complete():
                        break
                        
                    batch = remaining_ids[i:i + self.max_concurrent]
                    fragments = await self.fetch_batch(session, batch[0], len(batch))
                    
                    for fragment in fragments:
                        if fragment:
                            self.fragments[fragment.index] = fragment
                            print(f"Found missing fragment {fragment.index}: '{fragment.text}'")
        
        # Phase 3: Extended search if still incomplete
        print("Phase 3: Extended search...")
        search_id = 1
        consecutive_failures = 0
        
        while not self.is_puzzle_complete() and consecutive_failures < 100:
            batch_ids = [id for id in range(search_id, search_id + self.max_concurrent) 
                        if id not in self.seen_ids]
            
            if not batch_ids:
                search_id += self.max_concurrent
                continue
                
            fragments = await self.fetch_batch(session, batch_ids[0], len(batch_ids))
            
            if fragments:
                consecutive_failures = 0
                for fragment in fragments:
                    self.fragments[fragment.index] = fragment
                    print(f"Found fragment {fragment.index}: '{fragment.text}'")
            else:
                consecutive_failures += 1
                
            search_id += self.max_concurrent
    
    async def solve_puzzle(self) -> str:
        """Main method to solve the puzzle"""
        print("Starting Puzzle Decoder Race...")
        start_time = time.time()
        
        # Configure aiohttp session with optimizations
        connector = aiohttp.TCPConnector(
            limit=50,  # Total connection limit
            limit_per_host=30,  # Per-host connection limit
            ttl_dns_cache=300,  # DNS cache TTL
            use_dns_cache=True,
        )
        
        session_timeout = aiohttp.ClientTimeout(total=self.timeout)
        
        async with aiohttp.ClientSession(
            connector=connector,
            timeout=session_timeout,
            headers={'Connection': 'keep-alive'}
        ) as session:
            
            await self.smart_search_strategy(session)
            
            if self.is_puzzle_complete():
                message = self.get_assembled_message()
                elapsed = time.time() - start_time
                
                print(f"\n Puzzle Complete!")
                print(f"Message: '{message}'")
                print(f"Time: {elapsed:.3f} seconds")
                print(f"Total fragments: {len(self.fragments)}")
                print(f"Requests made: {len(self.seen_ids)}")
                
                if elapsed < 1.0:
                    print("BONUS ACHIEVED: Completed in under 1 second!")
                
                return message
            else:
                print("Failed to complete puzzle")
                return ""


async def main():
    """Main entry point"""
    decoder = PuzzleDecoder()
    message = await decoder.solve_puzzle()
    return message


if __name__ == "__main__":
    # Run the puzzle decoder
    try:
        message = asyncio.run(main())
        if message:
            print(f"\n Final Answer: {message}")
    except KeyboardInterrupt:
        print("\n Stopped by user")
    except Exception as e:
        print(f" Error: {e}")