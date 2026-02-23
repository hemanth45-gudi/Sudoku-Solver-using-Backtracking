# Sudoku Solver: Production Edition

An industry-level, production-quality Sudoku Solver featuring high-performance algorithms, a REST API, Docker deployment, and a modern GUI.

## 🚀 Features

- **Dual Solving Engines**: 
  - **Backtracking**: Classic recursive approach with visualization.
  - **DLX (Dancing Links)**: Blazing fast Knuth's Algorithm X implementation.
- **REST API**: Built with **FastAPI**, featuring automatic OpenAPI docs and benchmarking.
- **Modern GUI**:
  - Dark/Light Theme support.
  - Row, Column, and Box highlighting.
  - Real-time solving animation and stats.
  - Import/Export puzzle (JSON).
- **Production Infrastructure**:
  - **Docker & Docker Compose** for easy deployment.
  - **Structured Logging** with Loguru.
  - **Pydantic Settings** for configuration.
  - **CI/CD** via GitHub Actions.
  - **Unit Testing** with Pytest.

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/hemanth45-gudi/Sudoku-Solver-using-Backtracking.git
cd Sudoku-Solver-using-Backtracking

# Install dependencies
pip install -r requirements.txt
```

## 🏃 Usage

### GUI Application
```bash
python main.py
```

### REST API
```bash
# Start the API
uvicorn src.api.main:app --reload

# View Docs at http://localhost:8000/docs
```

### Docker
```bash
docker-compose up --build
```

## 🧪 Testing
```bash
pytest tests/
```

## 📁 Project Structure
- `src/api`: FastAPI models and routes.
- `src/gui`: Pygame interface and theme logic.
- `src/solver`: Core algorithms and validation.
- `src/utils`: Helpers, constants, and generator.
- `tests`: Unit and integration tests.
- `docs`: Detailed architecture and API documentation.
