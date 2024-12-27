FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
ENV PYTHONUNBUFFERED 1
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
CMD [ "uvicorn", "src.main.asgi:application", "--reload","--host", "0.0.0.0" ,"--port","8080", "--lifespan", "off"]