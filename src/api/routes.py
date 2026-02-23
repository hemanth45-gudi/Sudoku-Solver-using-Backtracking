from fastapi import APIRouter, HTTPException
from src.api.schemas import SudokuBoard, SolveResponse, HealthCheck
from src.solver.backtracking_solver import BacktrackingSolver
from src.solver.dlx_solver import DLXSolver
from src.config import settings
from src.logging_config import logger

router = APIRouter()

@router.get("/health", response_model=HealthCheck)
async def health_check():
    return HealthCheck(status="healthy", version=settings.VERSION)

@router.post("/solve/backtracking", response_model=SolveResponse)
async def solve_backtracking(request: SudokuBoard):
    solver = BacktrackingSolver()
    result = solver.solve(request.board)
    
    if result is None:
        raise HTTPException(status_code=400, detail="Puzzle is unsolvable or invalid")
        
    bench = solver.benchmarker.end_benchmark("Backtracking", solver.steps, solver.backtracks)
    
    return SolveResponse(
        solved_board=result,
        success=True,
        algorithm="Backtracking",
        execution_time=bench.execution_time,
        memory_usage_mb=bench.memory_usage_mb,
        steps=bench.steps,
        backtracks=bench.backtracks,
        message="Solved successfully"
    )

@router.post("/solve/dlx", response_model=SolveResponse)
async def solve_dlx(request: SudokuBoard):
    solver = DLXSolver()
    result = solver.solve(request.board)
    
    if result is None:
        raise HTTPException(status_code=400, detail="Puzzle is unsolvable or invalid")
        
    bench = solver.benchmarker.end_benchmark("DLX", solver.nodes_visited, solver.backtracks)
    
    return SolveResponse(
        solved_board=result,
        success=True,
        algorithm="DLX",
        execution_time=bench.execution_time,
        memory_usage_mb=bench.memory_usage_mb,
        steps=bench.nodes_visited,
        backtracks=bench.backtracks,
        message="Solved successfully"
    )
