import pygame
import time
from ..utils.helpers import valid

class VisualSolver:
    def __init__(self, gui_app):
        self.app             = gui_app
        self.rec_steps       = 0
        self.backtrack_steps = 0
        self.start_time      = 0
        self.total_time      = 0

    def reset_stats(self):
        self.rec_steps       = 0
        self.backtrack_steps = 0
        self.total_time      = 0
        self.start_time      = 0

    def visual_solve(self, grid):
        """Backtracking algorithm with real-time visualization."""
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    self.app.current_pos = (i, j)
                    for val in range(1, 10):
                        self.rec_steps += 1
                        if valid(grid, i, j, val):
                            grid[i][j] = val
                            self.app.cell_state[(i, j)] = "TRYING"
                            
                            # Update GUI
                            self.app.update_display()
                            pygame.time.delay(int(self.app.solve_speed * 1000))
                            
                            if self.visual_solve(grid):
                                self.app.cell_state[(i, j)] = "STABLE"
                                return True
                            
                            # Backtrack
                            self.backtrack_steps += 1
                            grid[i][j] = 0
                            self.app.cell_state[(i, j)] = "BACKTRACK"
                            self.app.update_display()
                            pygame.time.delay(int(self.app.solve_speed * 1000))
                            del self.app.cell_state[(i, j)]
                    
                    self.app.current_pos = None
                    return False
        return True

    def run_solve(self, grid):
        """Wrapper to initialize and run the solver with timing."""
        self.rec_steps = 0
        self.backtrack_steps = 0
        self.app.cell_state.clear()
        self.start_time = time.time()
        
        success = self.visual_solve(grid)
        
        self.total_time = round(time.time() - self.start_time, 2)
        return success
