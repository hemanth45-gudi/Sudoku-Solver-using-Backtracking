from .constants import DIF

def get_cord(pos):
    """Converts mouse position to grid (row, col) coordinates."""
    if pos[1] >= 500:
        return None
    row = int(pos[1] // DIF)
    col = int(pos[0] // DIF)
    return row, col

def valid(m, r, c, val):
    """
    Checks if 'val' is valid at grid[r][c].
    Returns (bool, reason) if it fails, or True if valid.
    """
    # Check Row
    for i in range(9):
        if m[r][i] == val and i != c:
            return False
            
    # Check Column
    for i in range(9):
        if m[i][c] == val and i != r:
            return False
            
    # Check 3x3 Box
    row_start = (r // 3) * 3
    col_start = (c // 3) * 3
    for i in range(row_start, row_start + 3):
        for j in range(col_start, col_start + 3):
            if m[i][j] == val and (i != r or j != c):
                return False
                
    return True

def check_complete(grid):
    """Checks if the Sudoku board is fully and correctly filled."""
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                return False
    return True

def get_contrast_text_color(bg_color):
    """
    Returns BLACK or WHITE text color based on the perceived luminance of bg_color.
    Uses the WCAG formula: (0.299*R + 0.587*G + 0.114*B)
    """
    # Handle RGBA by stripping Alpha
    r, g, b = bg_color[:3]
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return (0, 0, 0) if luminance > 0.5 else (255, 255, 255)
