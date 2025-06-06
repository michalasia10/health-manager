FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app
WORKDIR /app
COPY ./requirements.txt /app

ENV UV_COMPILE_BYTECODE=1


RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

ENV PATH="/app/.venv/bin:$PATH"
COPY ./src /app/src
COPY pyproject.toml /app/pyproject.toml
COPY uv.lock /app/uv.lock

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

EXPOSE 8080

RUN chmod +x /app/src
CMD [ "python3","-m", "src.main.run"]
