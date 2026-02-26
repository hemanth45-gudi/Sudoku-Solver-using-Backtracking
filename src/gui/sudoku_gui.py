import pygame
import sys
import os
import json
import time as _time
from src.utils.constants import *
from src.utils.helpers import *
from src.utils.generator import generate_new_puzzle
from src.solver.backtracking_solver import BacktrackingSolver, VisualSolver
from src.solver.validator import SudokuValidator
from src.logging_config import logger
from src.config import settings

class SudokuGUI:
    def __init__(self):
        pygame.font.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("SUDOKU SOLVER - PRODUCTION EDITION")
        
        try:
            img = pygame.image.load('assets/icon.png')
            pygame.display.set_icon(img)
        except Exception:
            logger.warning("Icon not found, using default")

        # Fonts
        self._setup_fonts()

        # State
        self.theme_name = settings.DEFAULT_THEME
        self.theme = THEMES[self.theme_name]
        self.mode = 'play'
        self.solve_speed = settings.ANIMATION_SPEED
        self.visualizing = False
        self.current_pos = None
        self.cell_state = {}
        
        self.row = 0
        self.col = 0
        self.flag_box = False
        self.message = "Welcome! Use R to Reset, V to Solve."
        self.message_color = Colors.FOCUS
        self.solution_grid = None

        self.solver = VisualSolver(self)
        self.new_game('medium')

        # Custom input state
        self.custom_grid = [[0]*9 for _ in range(9)]
        self.custom_row = 0
        self.custom_col = 0
        
        # Interactive Layout State
        self.buttons = {} # Stores Rect objects for collision detection
        self.ui_padding = 10
        self.btn_row_y = 530

    def _setup_fonts(self):
        """Initializes fonts with fallbacks."""
        # Main grid numbers
        self.font_main = pygame.font.SysFont("Arial", 36, bold=True)
        # Buttons and smaller UI elements
        self.font_btn = pygame.font.SysFont("Arial", 18, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 14, bold=True)
        self.font_title = pygame.font.SysFont("Arial", 22, bold=True)

    def toggle_theme(self):
        self.theme_name = "light" if self.theme_name == "dark" else "dark"
        self.theme = THEMES[self.theme_name]
        logger.info(f"Theme toggled to {self.theme_name}")

    def new_game(self, diff):
        self.grid = generate_new_puzzle(diff)
        self.start_grid = [row[:] for row in self.grid]
        self.row = self.col = 0
        self.flag_box = False
        self.cell_state.clear()
        self.reset_stats()
        logger.info(f"New game started: {diff}")
        
        # Pre-solve for "Correct Number" feedback
        solver_temp = BacktrackingSolver()
        self.solution_grid = solver_temp.solve(self.grid)

    def reset_stats(self):
        self.solver.steps = 0
        self.solver.backtracks = 0

    # ── Drawing Helpers ──────────────────────────────────────────────────

    def draw_button(self, text, rect_dim, color, text_color=None, font=None, btn_id=None):
        """Draws a themed button and returns its Rect."""
        rect = pygame.Rect(rect_dim)
        if btn_id: self.buttons[btn_id] = rect
        
        # Draw background
        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        # Subtle border
        pygame.draw.rect(self.screen, self.theme["grid"], rect, 1, border_radius=8)
        
        t_color = text_color if text_color else self.theme["text"]
        f = font if font else self.font_btn
        surf = f.render(text, True, t_color)
        self.screen.blit(surf, surf.get_rect(center=rect.center))
        return rect

    def draw_grid_lines(self, origin_x=0, origin_y=0):
        for i in range(10):
            thick = 5 if i % 3 == 0 else 2
            color = self.theme["text"] if i % 3 == 0 else self.theme["grid"]
            pygame.draw.line(self.screen, color,
                             (origin_x, origin_y + i*DIF),
                             (origin_x + 500, origin_y + i*DIF), thick)
            pygame.draw.line(self.screen, color,
                             (origin_x + i*DIF, origin_y),
                             (origin_x + i*DIF, origin_y + 500), thick)

    def draw_highlights(self):
        """Highlights the row and column of the selected cell."""
        if not self.flag_box: return
        
        # Row highlight
        s = pygame.Surface((500, DIF), pygame.SRCALPHA)
        s.fill(Colors.HIGHLIGHT)
        self.screen.blit(s, (0, self.row * DIF))
        
        # Col highlight
        s = pygame.Surface((DIF, 500), pygame.SRCALPHA)
        s.fill(Colors.HIGHLIGHT)
        self.screen.blit(s, (self.col * DIF, 0))

    def draw_cells(self):
        for r in range(9):
            for c in range(9):
                val = self.grid[r][c]
                if val != 0 or (r, c) in self.cell_state:
                    bg = self.theme["surface"]
                    st = self.cell_state.get((r, c))
                    
                    if st == "TRYING": bg = Colors.TRYING
                    elif st == "BACKTRACK": bg = Colors.BACKTRACK
                    elif st == "STABLE": bg = Colors.STABLE
                    
                    if bg != self.theme["surface"]:
                        pygame.draw.rect(self.screen, bg, (c*DIF+1, r*DIF+1, DIF-1, DIF-1))

                    if val != 0:
                        # Original numbers use theme text color, others use success color
                        is_original = self.start_grid[r][c] != 0
                        
                        if is_original:
                            color = self.theme["text"]
                        else:
                            # For solver-placed numbers, ensure contrast against the cell background
                            # Use contrast helper if background is a solving state (Trying/Backtrack/Stable)
                            if bg != self.theme["surface"]:
                                color = get_contrast_text_color(bg)
                            else:
                                color = self.theme["success"]
                        
                        surf = self.font_main.render(str(val), True, color)
                        self.screen.blit(surf, surf.get_rect(center=(c*DIF+DIF/2, r*DIF+DIF/2)))

                # Solver focus
                if self.current_pos == (r, c):
                    pygame.draw.rect(self.screen, self.theme["focus"], (c*DIF, r*DIF, DIF+1, DIF+1), 4)

    # ── UI Layouts ───────────────────────────────────────────────────────

    def draw_legend(self, y_pos):
        legend_y = y_pos
        items = [("Trying", Colors.TRYING), ("Backtrack", Colors.BACKTRACK), ("Solved", Colors.STABLE)]
        for i, (text, color) in enumerate(items):
            pygame.draw.rect(self.screen, color, (10 + i*160, legend_y, 20, 20), border_radius=4)
            surf = self.font_small.render(text, True, self.theme["text"])
            self.screen.blit(surf, (40 + i*160, legend_y + 2))

    def draw_play_ui(self):
        self.screen.fill(self.theme["bg"])
        self.buttons.clear()
        
        self.draw_highlights()
        self.draw_cells()
        self.draw_grid_lines()
        
        if self.flag_box:
            pygame.draw.rect(self.screen, self.theme["accent"], (self.col*DIF, self.row*DIF, DIF+1, DIF+1), 4)

        # ── Bottom controls ──────────────────────────────────────────────────
        btn_y = self.btn_row_y
        padding = 6
        # Narrower width for 500px screen
        available_w = 500 - 20 - (4 * padding)
        btn_w = available_w // 5
        
        btns = [
             ("Solve (V)", Colors.SUCCESS, WHITE, "solve"),
             ("Reset (R)", Colors.ERROR, WHITE, "reset"),
             ("New (G)", self.theme["accent"], WHITE, "new"),
             ("Custom (C)", self.theme["grid"], self.theme["text"], "custom"),
             ("Theme (T)", self.theme["grid"], self.theme["text"], "theme"),
        ]
        
        for i, (text, color, t_color, b_id) in enumerate(btns):
            x = 10 + i * (btn_w + padding)
            self.draw_button(text, (x, btn_y, btn_w, 38), color, t_color, btn_id=b_id)

        # ── Row 2: Difficulty & IO ───────────────────────────────────────────
        btn_y2 = btn_y + 45
        available_w_row2 = 500 - 20 - (4 * padding)
        btn_w2 = available_w_row2 // 5
        
        btns2 = [
             ("Easy (E)", self.theme["accent"], WHITE, "easy"),
             ("Medium (M)", self.theme["accent"], WHITE, "med"),
             ("Hard (H)", self.theme["accent"], WHITE, "hard"),
             ("Import (I)", self.theme["success"], WHITE, "import"),
             ("Export (O)", self.theme["success"], WHITE, "export"),
        ]
        
        for i, (text, color, t_color, b_id) in enumerate(btns2):
            x = 10 + i * (btn_w2 + padding)
            self.draw_button(text, (x, btn_y2, btn_w2, 38), color, t_color, btn_id=b_id)

        # Stats Row
        text_y = btn_y2 + 55
        time_ms = int(self.solver.solve_time * 1000)
        stats = f"Steps: {self.solver.steps} | Backtracks: {self.solver.backtracks} | Time: {time_ms}ms"
        surf_stats = self.font_small.render(stats, True, self.theme["text"])
        self.screen.blit(surf_stats, (10, text_y))

        # Message Area
        msg_y = text_y + 25
        msg_surf = self.font_btn.render(self.message, True, self.message_color)
        self.screen.blit(msg_surf, (10, msg_y))

        # Legend & Instructions
        self.draw_legend(msg_y + 35)
        
        inst_y = 550 + 175 # Near bottom
        inst = "E:Easy M:Med H:Hard | I:Import O:Export"
        surf_inst = self.font_small.render(inst, True, self.theme["text"])
        self.screen.blit(surf_inst, (10, inst_y))

    def draw_custom_input_ui(self):
        self.screen.fill(self.theme["bg"])
        self.buttons.clear()
        
        # Draw cells
        for r in range(9):
            for c in range(9):
                val = self.custom_grid[r][c]
                if r == self.custom_row and c == self.custom_col:
                    pygame.draw.rect(self.screen, self.theme["focus"], (c*DIF, r*DIF, DIF, DIF))
                elif val != 0:
                    pygame.draw.rect(self.screen, self.theme["surface"], (c*DIF, r*DIF, DIF, DIF))
                
                if val != 0:
                    bg_color = self.theme["focus"] if (r == self.custom_row and c == self.custom_col) else self.theme["surface"]
                    color = get_contrast_text_color(bg_color)
                    surf = self.font_main.render(str(val), True, color)
                    self.screen.blit(surf, surf.get_rect(center=(c*DIF+DIF/2, r*DIF+DIF/2)))

        self.draw_grid_lines()
        self._highlight_custom_conflicts()

        # Custom Mode Buttons
        btn_y = self.btn_row_y
        padding = 8
        available_w = 500 - 20 - (3 * padding)
        btn_w = available_w // 4
        
        btns = [
             ("Solve (S)", Colors.SUCCESS, WHITE, "c_solve"),
             ("Clear (C)", self.theme["grid"], self.theme["text"], "c_clear"),
             ("Import (I)", self.theme["accent"], WHITE, "c_import"),
             ("Export (O)", self.theme["accent"], WHITE, "c_export")
        ]
        
        for i, (text, color, t_color, b_id) in enumerate(btns):
            x = 10 + i * (btn_w + padding)
            self.draw_button(text, (x, btn_y, btn_w, 38), color, t_color, btn_id=b_id)
        
        # Back Button Row
        self.draw_button("Return (Esc)", (10, btn_y + 48, 140, 38), Colors.ERROR, WHITE, btn_id="c_back")
        
        title = self.font_title.render("CUSTOM INPUT", True, self.theme["accent"])
        self.screen.blit(title, (160, btn_y + 55))
        
        pygame.display.update()

    def _highlight_custom_conflicts(self):
        g = self.custom_grid
        for r in range(9):
            for c in range(9):
                v = g[r][c]
                if v == 0: continue
                # Basic conflict check
                conflict = False
                for i in range(9):
                    if (g[r][i] == v and i != c) or (g[i][c] == v and i != r):
                        conflict = True; break
                if not conflict:
                    br, bc = (r//3)*3, (c//3)*3
                    for dr in range(3):
                        for dc in range(3):
                            if g[br+dr][bc+dc] == v and (br+dr != r or bc+dc != c):
                                conflict = True; break
                
                if conflict:
                    pygame.draw.rect(self.screen, Colors.ERROR, (c*DIF, r*DIF, DIF, DIF), 4)

    # ── Puzzle I/O ───────────────────────────────────────────────────────

    def export_puzzle(self):
        try:
            # Choose the correct grid to export based on the current mode
            target_grid = self.custom_grid if self.mode == 'custom_input' else self.grid
            data = {"board": target_grid}
            with open("puzzle_export.json", "w") as f:
                json.dump(data, f)
            self.message = f"Saved to puzzle_export.json"
            self.message_color = Colors.SUCCESS
            logger.info("Puzzle exported")
        except Exception as e:
            self.message = f"Export failed: {str(e)}"
            self.message_color = Colors.ERROR

    def import_puzzle(self):
        # Fallback to export file if import file doesn't exist
        filename = "puzzle_import.json"
        if not os.path.exists(filename):
            filename = "puzzle_export.json"
            
        if not os.path.exists(filename):
            self.message = "No import or export file found!"
            self.message_color = Colors.WARNING
            return
            
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                new_board = data["board"]
                
                if self.mode == 'custom_input':
                    self.custom_grid = [row[:] for row in new_board]
                    self.message = f"Custom grid loaded from {filename}"
                else:
                    self.grid = [row[:] for row in new_board]
                    self.start_grid = [row[:] for row in self.grid]
                    self.cell_state.clear()
                    self.reset_stats()
                    
                    # Pre-solve for feedback
                    solver_temp = BacktrackingSolver()
                    self.solution_grid = solver_temp.solve(self.grid)
                    self.message = "Puzzle imported successfully!"
                
                self.message_color = Colors.SUCCESS
                logger.info(f"Puzzle imported from {filename}")
        except Exception as e:
            self.message = f"Import failed: {str(e)}"
            self.message_color = Colors.ERROR

    # ── Main Loop and Logic ──────────────────────────────────────────────

    def start_solve(self):
        self.visualizing = True
        self.message = "Solving..."
        self.message_color = self.theme["accent"]
        self.cell_state.clear()
        
        # Run visual solve
        success = self.solver.run_solve(self.grid)
        
        if success:
            self.message = "Puzzle Solved!"
            self.message_color = Colors.SUCCESS
        else:
            self.message = "No Solution Found"
            self.message_color = Colors.ERROR
            
        self.visualizing = False
        self.current_pos = None

    def update_display(self):
        if self.visualizing:
            self.solver.solve_time = _time.perf_counter() - self.solver.start_time
        self.draw_play_ui()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            if self.mode == 'play':
                self.draw_play_ui()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit(); sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = event.pos
                        if pos[1] < 500:
                            self.row, self.col = int(pos[1]//DIF), int(pos[0]//DIF)
                            self.flag_box = True
                        else:
                            # Button Click Handling
                            if self.buttons.get("solve") and self.buttons["solve"].collidepoint(pos):
                                self.start_solve()
                            elif self.buttons.get("reset") and self.buttons["reset"].collidepoint(pos):
                                self.grid = [r[:] for r in self.start_grid]
                            elif self.buttons.get("new") and self.buttons["new"].collidepoint(pos):
                                self.new_game('medium')
                            elif self.buttons.get("custom") and self.buttons["custom"].collidepoint(pos):
                                self.mode = 'custom_input'
                            elif self.buttons.get("theme") and self.buttons["theme"].collidepoint(pos):
                                self.toggle_theme()
                            elif self.buttons.get("easy") and self.buttons["easy"].collidepoint(pos):
                                self.new_game('easy')
                            elif self.buttons.get("med") and self.buttons["med"].collidepoint(pos):
                                self.new_game('medium')
                            elif self.buttons.get("hard") and self.buttons["hard"].collidepoint(pos):
                                self.new_game('hard')
                            elif self.buttons.get("import") and self.buttons["import"].collidepoint(pos):
                                self.import_puzzle()
                            elif self.buttons.get("export") and self.buttons["export"].collidepoint(pos):
                                self.export_puzzle()

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_v: self.start_solve()
                        elif event.key == pygame.K_t: self.toggle_theme()
                        elif event.key == pygame.K_g: self.new_game('medium')
                        elif event.key == pygame.K_r: self.grid = [r[:] for r in self.start_grid]
                        elif event.key == pygame.K_o: self.export_puzzle()
                        elif event.key == pygame.K_i: self.import_puzzle()
                        elif event.key == pygame.K_c: self.mode = 'custom_input'
                        elif event.key == pygame.K_e: self.new_game('easy')
                        elif event.key == pygame.K_m: self.new_game('medium')
                        elif event.key == pygame.K_h: self.new_game('hard')
                        elif pygame.K_1 <= event.key <= pygame.K_9:
                            if self.flag_box and self.start_grid[self.row][self.col] == 0:
                                val = event.key - pygame.K_0
                                if SudokuValidator.is_safe_move(self.grid, self.row, self.col, val):
                                    self.grid[self.row][self.col] = val
                                    # Provide specific feedback against the solution
                                    if self.solution_grid and self.solution_grid[self.row][self.col] == val:
                                        self.message = "Correct Number!"; self.message_color = Colors.SUCCESS
                                    else:
                                        self.message = "Valid Move!"; self.message_color = Colors.TRYING
                                else:
                                    self.message = "Invalid Move!"; self.message_color = Colors.ERROR
                        elif event.key in (pygame.K_BACKSPACE, pygame.K_0, pygame.K_DELETE):
                            if self.flag_box and self.start_grid[self.row][self.col] == 0:
                                self.grid[self.row][self.col] = 0

            elif self.mode == 'custom_input':
                self.draw_custom_input_ui()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit(); sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = event.pos
                        if pos[1] < 500:
                            self.custom_row, self.custom_col = int(pos[1]//DIF), int(pos[0]//DIF)
                        else:
                            # Custom Button Click Handling
                            if self.buttons.get("c_solve") and self.buttons["c_solve"].collidepoint(pos):
                                self.grid = [r[:] for r in self.custom_grid]
                                self.start_grid = [r[:] for r in self.custom_grid]
                                self.mode = 'play'; self.start_solve()
                            elif self.buttons.get("c_clear") and self.buttons["c_clear"].collidepoint(pos):
                                self.custom_grid = [[0]*9 for _ in range(9)]
                            elif self.buttons.get("c_import") and self.buttons["c_import"].collidepoint(pos):
                                self.import_puzzle()
                            elif self.buttons.get("c_export") and self.buttons["c_export"].collidepoint(pos):
                                self.start_grid = [r[:] for r in self.custom_grid]
                                self.export_puzzle()
                            elif self.buttons.get("c_back") and self.buttons["c_back"].collidepoint(pos):
                                self.mode = 'play'

                    elif event.type == pygame.KEYDOWN:
                        if pygame.K_1 <= event.key <= pygame.K_9:
                            self.custom_grid[self.custom_row][self.custom_col] = event.key - pygame.K_0
                        elif event.key in (pygame.K_0, pygame.K_BACKSPACE, pygame.K_DELETE):
                            self.custom_grid[self.custom_row][self.custom_col] = 0
                        elif event.key == pygame.K_UP: self.custom_row = (self.custom_row - 1) % 9
                        elif event.key == pygame.K_DOWN: self.custom_row = (self.custom_row + 1) % 9
                        elif event.key == pygame.K_LEFT: self.custom_col = (self.custom_col - 1) % 9
                        elif event.key == pygame.K_RIGHT: self.custom_col = (self.custom_col + 1) % 9
                        elif event.key == pygame.K_s:
                            self.grid = [r[:] for r in self.custom_grid]
                            self.start_grid = [r[:] for r in self.custom_grid]
                            self.mode = 'play'; self.start_solve()
                        elif event.key == pygame.K_c: self.custom_grid = [[0]*9 for _ in range(9)]
                        elif event.key == pygame.K_i: self.import_puzzle()
                        elif event.key == pygame.K_o:
                            self.start_grid = [r[:] for r in self.custom_grid]
                            self.export_puzzle()
                        elif event.key == pygame.K_ESCAPE: self.mode = 'play'

            pygame.display.update()
            clock.tick(60)
