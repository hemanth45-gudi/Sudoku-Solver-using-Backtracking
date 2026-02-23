from typing import List, Optional
from pydantic import BaseModel, Field

class SudokuBoard(BaseModel):
    board: List[List[int]] = Field(..., description="9x9 Sudoku board where 0 represents empty cells")

    model_config = {
        "json_schema_extra": {
            "example": {
                "board": [
                    [5, 3, 0, 0, 7, 0, 0, 0, 0],
                    [6, 0, 0, 1, 9, 5, 0, 0, 0],
                    [0, 9, 8, 0, 0, 0, 0, 6, 0],
                    [8, 0, 0, 0, 6, 0, 0, 0, 3],
                    [4, 0, 0, 8, 0, 3, 0, 0, 1],
                    [7, 0, 0, 0, 2, 0, 0, 0, 6],
                    [0, 6, 0, 0, 0, 0, 2, 8, 0],
                    [0, 0, 0, 4, 1, 9, 0, 0, 5],
                    [0, 0, 0, 0, 8, 0, 0, 7, 9]
                ]
            }
        }
    }

class SolveResponse(BaseModel):
    solved_board: Optional[List[List[int]]] = None
    success: bool
    algorithm: str
    execution_time: float
    memory_usage_mb: float
    steps: int
    backtracks: int
    message: str

class HealthCheck(BaseModel):
    status: str
    version: str
