FROM python:3.12-slim-bookworm

# 1. Install uv by copying it directly from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Enable byte-code compilation and block buffering for optimal Python output
ENV UV_COMPILE_BYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. Copy dependency files first to maximize Docker layer caching
COPY pyproject.toml uv.lock ./

# 5. Install dependencies without the application code itself
RUN uv sync --frozen --no-cache --no-install-project

# 6. Copy the rest of the source code into the container
COPY . .

# 7. Sync the project itself (installs your app into the venv)
RUN uv sync --frozen --no-cache

# 9. Expose the port FastAPI runs on
EXPOSE 8000

# 10. Run the application using fastapi's production command line
CMD ["uv", "run", "uvicorn", "main:xrag", "--host", "0.0.0.0", "--port", "8000"]
