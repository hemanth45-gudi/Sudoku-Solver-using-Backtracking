from src.logging_config import setup_logging
from src.gui.sudoku_gui import SudokuGUI
from src.config import settings
from src.logging_config import logger

def main():
    logger.info(f"Starting {settings.PROJECT_NAME} version {settings.VERSION}")
    try:
        app = SudokuGUI()
        app.run()
    except Exception as e:
        logger.exception(f"Application crashed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
