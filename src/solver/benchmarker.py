import time
import psutil
import os
from dataclasses import dataclass
from typing import Optional
from src.logging_config import logger

@dataclass
class BenchmarkResult:
    execution_time: float
    memory_usage_mb: float
    steps: int
    backtracks: int
    algorithm: str

class Benchmarker:
    """
    Benchmarks solving performance (time and memory).
    """
    
    def __init__(self):
        self._process = psutil.Process(os.getpid())
        
    def start_benchmark(self):
        self._start_time = time.perf_counter()
        self._start_mem = self._process.memory_info().rss / (1024 * 1024)
        
    def end_benchmark(self, algorithm: str, steps: int = 0, backtracks: int = 0) -> BenchmarkResult:
        end_time = time.perf_counter()
        end_mem = self._process.memory_info().rss / (1024 * 1024)
        
        execution_time = end_time - self._start_time
        memory_used = end_mem - self._start_mem
        
        result = BenchmarkResult(
            execution_time=execution_time,
            memory_usage_mb=max(0, memory_used),
            steps=steps,
            backtracks=backtracks,
            algorithm=algorithm
        )
        
        logger.info(f"Benchmark for {algorithm}: {execution_time:.4f}s, {result.memory_usage_mb:.2f}MB, Steps: {steps}")
        return result
