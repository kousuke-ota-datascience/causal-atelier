FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_NO_CACHE=1

RUN pip install --no-cache-dir uv==0.8.3
WORKDIR /app
RUN groupadd --system causal && useradd --system --gid causal --home /app causal
COPY --chmod=0644 pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev --no-install-project --no-cache
COPY --chmod=0755 src ./src
RUN uv sync --frozen --no-dev --no-cache
COPY --chmod=0644 alembic_product.ini ./
COPY --chmod=0755 product_migrations ./product_migrations

RUN mkdir -p /state/objects /state/workspaces && chown -R causal:causal /state
USER causal

ENV PATH="/app/.venv/bin:${PATH}" \
    ARIADNE_STATE_DIR=/state
EXPOSE 8000
CMD ["uvicorn", "ariadne.interfaces.web_api.app:app", "--host", "0.0.0.0", "--port", "8000"]
