import pygame

# Screen Dimensions
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 750
DIF = 500 / 9  # Grid is 500x500
SIDEBAR_WIDTH = 0

# Colors (Modern Palette)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Colors:
    # High-contrast text colors
    DARK_TEXT = (255, 255, 255) # Pure white
    LIGHT_TEXT = (0, 0, 0)      # Pure black
    
    # Background and Surfaces
    DARK_BG = (10, 10, 10)      # Near black for higher contrast
    DARK_SURFACE = (25, 25, 25)
    DARK_GRID = (70, 70, 70)    # Subdued but visible grid
    DARK_ACCENT = (142, 68, 173) # Deep Amethyst
    
    LIGHT_BG = (255, 255, 255)  # Pure white
    LIGHT_SURFACE = (240, 240, 240)
    LIGHT_GRID = (210, 210, 210)
    LIGHT_ACCENT = (41, 128, 185) # Belize Hole Blue

    # Functional Colors (Accessibility Focused)
    # Reduced intensity green as per user request
    SUCCESS = (39, 174, 96)    # Neptune Green (Softer than emerald)
    ERROR = (192, 57, 43)      # Pomegranate Red
    WARNING = (243, 156, 18)   # Orange
    HIGHLIGHT = (52, 152, 219, 50) # Very light transparent highlight
    FOCUS = (211, 84, 0)       # Pumpkin Orange

    # Solving Visualization (Softer Tones)
    TRYING = (52, 152, 219)    # Peter River Blue
    BACKTRACK = (231, 76, 60)  # Alizarin Red
    STABLE = (39, 174, 96)     # Neptune Green

THEMES = {
    "dark": {
        "bg": (10, 10, 10),
        "surface": (25, 25, 25),
        "text": (255, 255, 255),
        "grid": (70, 70, 70),
        "accent": (142, 68, 173),
        "success": (46, 204, 113),  # Lighter green for dark
        "focus": (243, 156, 18)     # Vibrant orange
    },
    "light": {
        "bg": (255, 255, 255),
        "surface": (240, 240, 240),
        "text": (0, 0, 0),
        "grid": (210, 210, 210),
        "accent": (41, 128, 185),
        "success": (30, 132, 73),   # Darker green for light
        "focus": (211, 84, 0)       # Darker orange
    }
}

# Difficulty Grids
EASY_GRID = [
    [0, 0, 0, 2, 6, 0, 7, 0, 1],
    [6, 8, 0, 0, 7, 0, 0, 9, 0],
    [1, 9, 0, 0, 0, 4, 5, 0, 0],
    [8, 2, 0, 1, 0, 0, 0, 4, 0],
    [0, 0, 4, 6, 0, 2, 9, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 2, 8],
    [0, 0, 9, 3, 0, 0, 0, 7, 4],
    [0, 4, 0, 0, 5, 0, 0, 3, 6],
    [7, 0, 3, 0, 1, 8, 0, 0, 0]
]

MEDIUM_GRID = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]

HARD_GRID = [
    [0, 0, 0, 6, 0, 0, 4, 0, 0],
    [7, 0, 0, 0, 0, 3, 6, 0, 0],
    [0, 0, 0, 0, 9, 1, 0, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 5, 0, 1, 8, 0, 0, 0, 3],
    [0, 0, 0, 3, 0, 6, 0, 4, 5],
    [0, 4, 0, 2, 0, 0, 0, 6, 0],
    [9, 0, 3, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 1, 0, 0]
]
