FROM astral/uv:python3.12-bookworm-slim

WORKDIR /app

#  Copy only dependency files first for caching
COPY pyproject.toml pyproject.lock* uv.lock ./

#  Install runtime dependencies via UV
RUN uv sync --frozen

#  Copy the rest of the project
COPY . .

#  Start FastAPI app
CMD ["uv", "run", "uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--app-dir", "src"]
