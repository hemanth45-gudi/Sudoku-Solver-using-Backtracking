import pygame
import sys
import time as _time
from ..utils.constants import *
from ..utils.helpers import *
from ..utils.generator import generate_new_puzzle
from ..solver.backtracking_solver import VisualSolver

class SudokuGUI:
    def __init__(self):
        pygame.font.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("SUDOKU SOLVER - BACKTRACKING")
        
        try:
            img = pygame.image.load('assets/icon.png')
            pygame.display.set_icon(img)
        except:
            pass

        self.font1  = pygame.font.SysFont("comicsans", 40)
        self.font2  = pygame.font.SysFont("comicsans", 20)
        self.font3  = pygame.font.SysFont("comicsans", 16)
        self.font_h = pygame.font.SysFont("comicsans", 22, bold=True)

        # ── Play mode state ────────────────────────────────────────────
        self.mode = 'play'          # 'play' | 'custom_input'
        self.new_game('medium')

        self.message       = ""
        self.message_color = BLACK
        self.color_idx     = 0

        # ── Solver state ───────────────────────────────────────────────
        self.solve_speed   = 0.05
        self.visualizing   = False
        self.current_pos   = None
        self.cell_state    = {}

        # ── Live stats ─────────────────────────────────────────────────
        self.live_steps      = 0
        self.live_backtracks = 0
        self.live_time       = 0.0
        self.solve_start     = 0.0

        self.solver = VisualSolver(self)

        # ── Custom input mode state ────────────────────────────────────
        self.custom_grid  = [[0]*9 for _ in range(9)]   # grid being typed
        self.custom_row   = 0
        self.custom_col   = 0

    # ════════════════════════════════════════════════════════════════════
    # GAME MANAGEMENT
    # ════════════════════════════════════════════════════════════════════
    def new_game(self, diff):
        self.grid       = generate_new_puzzle(diff)
        self.start_grid = [row[:] for row in self.grid]
        self.row = self.col = self.val = self.flag_box = 0

    def reset_stats(self):
        self.live_steps = self.live_backtracks = 0
        self.live_time  = 0.0

    # ════════════════════════════════════════════════════════════════════
    # DRAWING – SHARED HELPERS
    # ════════════════════════════════════════════════════════════════════
    def draw_button(self, text, rect, color, text_color=WHITE, font=None):
        f = font or self.font2
        pygame.draw.rect(self.screen, color, rect, border_radius=6)
        surf = f.render(text, 1, text_color)
        self.screen.blit(surf, surf.get_rect(center=(rect[0]+rect[2]//2, rect[1]+rect[3]//2)))

    def draw_grid_lines(self, origin_x=0, origin_y=0):
        for i in range(10):
            thick = 5 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, BLACK,
                             (origin_x,            origin_y + i*DIF),
                             (origin_x + SCREEN_WIDTH, origin_y + i*DIF), thick)
            pygame.draw.line(self.screen, BLACK,
                             (origin_x + i*DIF, origin_y),
                             (origin_x + i*DIF, origin_y + SCREEN_WIDTH), thick)

    # ════════════════════════════════════════════════════════════════════
    # DRAWING – PLAY MODE
    # ════════════════════════════════════════════════════════════════════
    def draw_cells(self):
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] != 0:
                    bg = COLORS[self.color_idx]
                    if (r, c) in self.cell_state:
                        st = self.cell_state[(r, c)]
                        if st == "TRYING":    bg = TRYING_COLOR
                        elif st == "BACKTRACK": bg = BACKTRACK_COLOR

                    pygame.draw.rect(self.screen, bg, (c*DIF, r*DIF, DIF+1, DIF+1))

                    num_color = BLACK if self.start_grid[r][c] != 0 else BLUE
                    surf = self.font1.render(str(self.grid[r][c]), 1, num_color)
                    self.screen.blit(surf, surf.get_rect(center=(c*DIF+DIF/2, r*DIF+DIF/2)))

                if self.current_pos == (r, c):
                    pygame.draw.rect(self.screen, ORANGE, (c*DIF, r*DIF, DIF+1, DIF+1), 5)

    def draw_selection_box(self):
        r, c = self.row, self.col
        if not (0 <= r < 9 and 0 <= c < 9):
            return
        for i in range(2):
            pygame.draw.line(self.screen, ORANGE,
                             (c*DIF-3,        (r+i)*DIF),
                             (c*DIF+DIF+3,    (r+i)*DIF), 7)
            pygame.draw.line(self.screen, ORANGE,
                             ((c+i)*DIF, r*DIF),
                             ((c+i)*DIF, r*DIF+DIF), 7)

    def draw_stats_panel(self):
        """Live stats bar shown at the very bottom of the play screen."""
        panel_y = 660
        # Background strip
        pygame.draw.rect(self.screen, (230, 230, 230), (0, panel_y, SCREEN_WIDTH, 40))
        pygame.draw.line(self.screen, BLACK, (0, panel_y), (SCREEN_WIDTH, panel_y), 2)

        if self.visualizing:
            elapsed = round(_time.time() - self.solve_start, 1)
            stats = f"⏱ {elapsed}s   |   Steps: {self.live_steps}   |   Backtracks: {self.live_backtracks}"
            col = (0, 100, 200)
        elif self.solver.total_time > 0:
            stats = (f"Solved in {self.solver.total_time}s   |   "
                     f"Steps: {self.solver.rec_steps}   |   "
                     f"Backtracks: {self.solver.backtrack_steps}")
            col = (0, 140, 0)
        else:
            stats = "Press V or SOLVE to start  |  Speed: 1=Slow  2=Med  3=Fast"
            col = (100, 100, 100)

        surf = self.font3.render(stats, 1, col)
        self.screen.blit(surf, surf.get_rect(center=(SCREEN_WIDTH//2, panel_y+20)))

    def draw_play_ui(self):
        """Draws the full play-mode UI."""
        self.screen.fill(WHITE)
        self.draw_cells()
        self.draw_grid_lines()
        if self.flag_box:
            self.draw_selection_box()

        # ── instruction text ──
        t1 = self.font3.render("D:Default  R:Reset  C:Color  G:New  I:Custom Input", 1, BLACK)
        t2 = self.font3.render("Levels: E:Easy  M:Medium  H:Hard  |  Speed: 1 2 3", 1, BLACK)
        self.screen.blit(t1, (8, 508))
        self.screen.blit(t2, (8, 528))

        # ── buttons ──
        self.draw_button("SOLVE (V)", ( 8, 548, 148, 38), (0, 150, 0))
        self.draw_button("RESET (R)", (162, 548, 148, 38), (180, 30, 30))
        self.draw_button("NEW (G)",   (316, 548, 160, 38), (0, 0, 170))

        # ── custom input button ──
        self.draw_button("CUSTOM INPUT (I)", (8, 592, 470, 34),
                         (60, 60, 60), font=self.font3)

        # ── status message ──
        if self.message:
            surf = self.font2.render(self.message, 1, self.message_color)
            self.screen.blit(surf, (8, 632))

        # ── live stats panel ──
        self.draw_stats_panel()

    # ════════════════════════════════════════════════════════════════════
    # DRAWING – CUSTOM INPUT MODE
    # ════════════════════════════════════════════════════════════════════
    def draw_custom_input_ui(self):
        self.screen.fill((245, 245, 245))

        # Title
        title = self.font_h.render("CUSTOM PUZZLE INPUT  (0 = empty cell)", 1, (30, 30, 30))
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 18)))

        # Grid background
        pygame.draw.rect(self.screen, WHITE, (0, 30, SCREEN_WIDTH, SCREEN_WIDTH))

        # Draw cells
        for r in range(9):
            for c in range(9):
                val = self.custom_grid[r][c]
                cell_x = c * DIF
                cell_y = 30 + r * DIF

                # Highlight selected cell
                if r == self.custom_row and c == self.custom_col:
                    pygame.draw.rect(self.screen, (200, 230, 255),
                                     (cell_x+1, cell_y+1, DIF-1, DIF-1))
                elif val != 0:
                    pygame.draw.rect(self.screen, (220, 240, 220),
                                     (cell_x+1, cell_y+1, DIF-1, DIF-1))

                if val != 0:
                    surf = self.font1.render(str(val), 1, (20, 80, 20))
                    self.screen.blit(surf, surf.get_rect(
                        center=(cell_x + DIF/2, cell_y + DIF/2)))

        # Grid lines (shifted down by 30 to leave header space)
        for i in range(10):
            thick = 5 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, BLACK,
                             (0,            30 + i*DIF),
                             (SCREEN_WIDTH, 30 + i*DIF), thick)
            pygame.draw.line(self.screen, BLACK,
                             (i*DIF, 30),
                             (i*DIF, 30 + SCREEN_WIDTH), thick)

        # Buttons
        self.draw_button("▶  SOLVE IT",
                         (8,  518, 230, 42), (0, 150, 0))
        self.draw_button("CLEAR GRID",
                         (248, 518, 115, 42), (160, 160, 160), text_color=BLACK)
        self.draw_button("← BACK",
                         (368, 518, 120, 42), (180, 30, 30))

        # Validation message
        if self.message:
            surf = self.font2.render(self.message, 1, self.message_color)
            self.screen.blit(surf, (8, 568))

        # Instructions
        hint = self.font3.render(
            "Click a cell, type 1-9 to enter  |  0 or Del to clear  |  Arrow keys to navigate",
            1, (100, 100, 100))
        self.screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH//2, 598)))

        # Conflict highlights
        self._highlight_custom_conflicts()

        pygame.display.update()

    def _highlight_custom_conflicts(self):
        """Draw a red border around conflicting cells in custom input mode."""
        conflict_cells = set()
        g = self.custom_grid
        for r in range(9):
            for c in range(9):
                v = g[r][c]
                if v == 0:
                    continue
                # Check row
                for c2 in range(9):
                    if c2 != c and g[r][c2] == v:
                        conflict_cells.add((r, c)); conflict_cells.add((r, c2))
                # Check col
                for r2 in range(9):
                    if r2 != r and g[r2][c] == v:
                        conflict_cells.add((r, c)); conflict_cells.add((r2, c))
                # Check box
                br, bc = (r//3)*3, (c//3)*3
                for dr in range(3):
                    for dc in range(3):
                        nr, nc = br+dr, bc+dc
                        if (nr, nc) != (r, c) and g[nr][nc] == v:
                            conflict_cells.add((r, c)); conflict_cells.add((nr, nc))

        for (r, c) in conflict_cells:
            pygame.draw.rect(self.screen, RED,
                             (c*DIF, 30+r*DIF, DIF, DIF), 4)

    def _custom_has_conflicts(self):
        g = self.custom_grid
        for r in range(9):
            for c in range(9):
                v = g[r][c]
                if v == 0: continue
                for c2 in range(9):
                    if c2 != c and g[r][c2] == v: return True
                for r2 in range(9):
                    if r2 != r and g[r2][c] == v: return True
                br, bc = (r//3)*3, (c//3)*3
                for dr in range(3):
                    for dc in range(3):
                        nr, nc = br+dr, bc+dc
                        if (nr, nc) != (r, c) and g[nr][nc] == v: return True
        return False

    # ════════════════════════════════════════════════════════════════════
    # SOLVER
    # ════════════════════════════════════════════════════════════════════
    def start_solve(self):
        self.visualizing  = True
        self.solve_start  = _time.time()
        self.live_steps   = 0
        self.live_backtracks = 0
        self.message      = ""
        self.solver.reset_stats()

        solve_grid = [row[:] for row in self.start_grid]
        success = self.solver.run_solve(solve_grid)

        if success:
            self.grid = solve_grid
            self.message       = "[OK] Puzzle solved!"
            self.message_color = (0, 150, 0)
        else:
            self.message       = "[!!] No solution found for this puzzle"
            self.message_color = RED

        self.visualizing = False
        self.current_pos = None

    # ════════════════════════════════════════════════════════════════════
    # INPUT HANDLING
    # ════════════════════════════════════════════════════════════════════
    def handle_input(self, val):
        if self.start_grid[self.row][self.col] != 0:
            self.message       = "Cannot change original puzzle numbers"
            self.message_color = RED
            self.val = 0
            return
        if val:
            if valid(self.grid, self.row, self.col, val):
                self.grid[self.row][self.col] = val
                self.message       = "[OK] Correct entry"
                self.message_color = (0, 128, 0)
                if check_complete(self.grid):
                    self.message       = "Congrats! Puzzle completed!"
                    self.message_color = (0, 200, 0)
            else:
                self.message       = "[X] Invalid move for this cell"
                self.message_color = RED
            self.val = 0

    # ════════════════════════════════════════════════════════════════════
    # UPDATE DISPLAY (called by solver during visualization too)
    # ════════════════════════════════════════════════════════════════════
    def update_display(self):
        # Update live stats counters from solver
        if self.visualizing:
            self.live_steps      = self.solver.rec_steps
            self.live_backtracks = self.solver.backtrack_steps

        self.draw_play_ui()
        pygame.display.update()

        if self.visualizing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

    # ════════════════════════════════════════════════════════════════════
    # MAIN LOOP
    # ════════════════════════════════════════════════════════════════════
    def run(self):
        clock   = pygame.time.Clock()
        running = True

        while running:
            # ── PLAY MODE ──────────────────────────────────────────────
            if self.mode == 'play':
                self.draw_play_ui()
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = event.pos

                        # ── Buttons (y 548-586) ──
                        btn_y = 548 <= pos[1] <= 586
                        print(f"Click: x={pos[0]}, y={pos[1]}, btn_zone={btn_y}")
                        if btn_y:
                            if pos[0] <= 156:        # SOLVE
                                print("SOLVE clicked")
                                self.start_solve(); continue
                            elif pos[0] <= 310:      # RESET
                                print("RESET clicked")
                                self.grid = [r[:] for r in self.start_grid]
                                self.cell_state.clear(); self.current_pos = None
                                self.reset_stats()
                                self.solver.total_time = 0
                                self.message       = "Board reset to starting state"
                                self.message_color = (0, 100, 180); continue
                            elif pos[0] <= 476:      # NEW
                                print("NEW clicked")
                                self.new_game('medium'); self.reset_stats()
                                self.solver.total_time = 0
                                self.message       = "New puzzle generated!"
                                self.message_color = (0, 100, 180); continue

                        # ── Custom Input button (y 592‒625) ──
                        if 592 <= pos[1] <= 626:
                            self.mode = 'custom_input'
                            self.custom_grid = [[0]*9 for _ in range(9)]
                            self.custom_row = self.custom_col = 0
                            self.message = ""; continue

                        # ── Cell selection ──
                        coord = get_cord(pos)
                        if coord:
                            self.row, self.col = coord
                            self.flag_box = 1
                        else:
                            self.flag_box = 0

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:  self.col -= 1; self.flag_box = 1
                        if event.key == pygame.K_RIGHT: self.col += 1; self.flag_box = 1
                        if event.key == pygame.K_UP:    self.row -= 1; self.flag_box = 1
                        if event.key == pygame.K_DOWN:  self.row += 1; self.flag_box = 1
                        self.row %= 9; self.col %= 9

                        if pygame.K_1 <= event.key <= pygame.K_9:
                            self.val = event.key - pygame.K_0
                        if event.key in (pygame.K_BACKSPACE, pygame.K_0, pygame.K_DELETE):
                            if self.start_grid[self.row][self.col] == 0:
                                self.grid[self.row][self.col] = 0

                        if event.key == pygame.K_r:
                            self.grid = [r[:] for r in self.start_grid]
                            self.reset_stats(); self.solver.total_time = 0
                        if event.key == pygame.K_v: self.start_solve()
                        if event.key == pygame.K_g:
                            self.new_game('medium'); self.reset_stats()
                            self.solver.total_time = 0
                        if event.key == pygame.K_i:
                            self.mode = 'custom_input'
                            self.custom_grid = [[0]*9 for _ in range(9)]
                            self.custom_row = self.custom_col = 0
                            self.message = ""
                        if event.key == pygame.K_d:
                            self.grid = self.start_grid = [r[:] for r in MEDIUM_GRID]
                        if event.key == pygame.K_e: self.new_game('easy')
                        if event.key == pygame.K_m: self.new_game('medium')
                        if event.key == pygame.K_h: self.new_game('hard')
                        if event.key == pygame.K_c:
                            self.color_idx = (self.color_idx + 1) % len(COLORS)
                        if event.key == pygame.K_1: self.solve_speed = 0.15
                        if event.key == pygame.K_2: self.solve_speed = 0.05
                        if event.key == pygame.K_3: self.solve_speed = 0.01

                if self.val:
                    self.handle_input(self.val)

            # ── CUSTOM INPUT MODE ───────────────────────────────────────
            elif self.mode == 'custom_input':
                self.draw_custom_input_ui()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = event.pos
                        # ── SOLVE IT button (y 518‒559) ──
                        if 518 <= pos[1] <= 560:
                            if 8 <= pos[0] <= 238:        # SOLVE IT
                                if self._custom_has_conflicts():
                                    self.message       = "✘  Fix conflicts (red cells) before solving"
                                    self.message_color = RED
                                else:
                                    # Load custom grid as new puzzle
                                    self.grid       = [r[:] for r in self.custom_grid]
                                    self.start_grid = [r[:] for r in self.custom_grid]
                                    self.reset_stats()
                                    self.solver.total_time = 0
                                    self.mode       = 'play'
                                    self.message    = "Custom puzzle loaded — press SOLVE (V) to solve!"
                                    self.message_color = (0, 120, 200)
                                    self.flag_box   = 0
                            elif 248 <= pos[0] <= 363:    # CLEAR GRID
                                self.custom_grid = [[0]*9 for _ in range(9)]
                                self.message = ""
                            elif 368 <= pos[0] <= 488:    # BACK
                                self.mode = 'play'
                                self.message = ""

                        # ── Cell click (y 30‒530) ──
                        elif 30 <= pos[1] <= 30 + SCREEN_WIDTH:
                            c = int(pos[0] // DIF)
                            r = int((pos[1] - 30) // DIF)
                            if 0 <= r < 9 and 0 <= c < 9:
                                self.custom_row, self.custom_col = r, c

                    elif event.type == pygame.KEYDOWN:
                        r, c = self.custom_row, self.custom_col
                        if event.key == pygame.K_LEFT:  self.custom_col = (c-1) % 9
                        if event.key == pygame.K_RIGHT: self.custom_col = (c+1) % 9
                        if event.key == pygame.K_UP:    self.custom_row = (r-1) % 9
                        if event.key == pygame.K_DOWN:  self.custom_row = (r+1) % 9

                        if pygame.K_1 <= event.key <= pygame.K_9:
                            self.custom_grid[r][c] = event.key - pygame.K_0
                            self.message = ""
                        if event.key in (pygame.K_0, pygame.K_BACKSPACE, pygame.K_DELETE):
                            self.custom_grid[r][c] = 0
                            self.message = ""
                        if event.key == pygame.K_ESCAPE:
                            self.mode = 'play'; self.message = ""
                        if event.key == pygame.K_RETURN:
                            # Same as SOLVE IT
                            if not self._custom_has_conflicts():
                                self.grid       = [r2[:] for r2 in self.custom_grid]
                                self.start_grid = [r2[:] for r2 in self.custom_grid]
                                self.reset_stats(); self.solver.total_time = 0
                                self.mode       = 'play'
                                self.message    = "Custom puzzle loaded — press SOLVE (V) to solve!"
                                self.message_color = (0, 120, 200)
                            else:
                                self.message       = "✘  Fix conflicts first!"
                                self.message_color = RED

            clock.tick(60)

        pygame.quit()
