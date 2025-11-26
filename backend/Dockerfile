FROM astral/uv:python3.12-bookworm-slim

WORKDIR /app

# Copy project
COPY . .


# Install dependencies
RUN uv sync --frozen

#CMD ["uv", "run", "uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["uv", "run", "uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--app-dir", "src"]

