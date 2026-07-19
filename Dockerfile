FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy

RUN pip install --no-cache-dir uv==0.8.3
WORKDIR /app
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
RUN uv sync --frozen --no-dev
COPY alembic.ini ./
COPY migrations ./migrations
COPY configs ./configs

RUN groupadd --system causal && useradd --system --gid causal --home /app causal \
    && mkdir -p /state/objects /state/workspaces \
    && chown -R causal:causal /app /state
USER causal

ENV PATH="/app/.venv/bin:${PATH}" \
    CAUSAL_ATELIER_STATE_DIR=/state
EXPOSE 8000
CMD ["uvicorn", "causal_atelier.interfaces.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
