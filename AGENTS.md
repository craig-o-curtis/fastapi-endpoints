# Agents

This project uses FastAPI. Follow these conventions when working with the codebase.

## AI interactions

- NEVER perform CREATE, UPDATE, or DELETE git actions that add, commit, revert, stash, revert, reset or any altercations AT ALL. You may ONLY perform READ actions.

## FastAPI Conventions

- Use `Annotated[..., Depends(...)]` for parameters and dependencies; create reusable type aliases for shared dependencies.
- Do not use `...` (Ellipsis) as a default value for required parameters or model fields; use `Query()`, `Body()`, etc. instead.
- Prefer return type annotations; use `response_model` when the public response schema differs from the internal return value.
- Do not use Pydantic `RootModel`; use regular type annotations with `Annotated` and Pydantic validation utilities like `Field()`.
- Declare router-level `prefix`, `tags`, and `dependencies` on the `APIRouter` itself rather than in `include_router()`.
- Use `async` path operations only when the called logic is async-compatible and non-blocking; otherwise use regular `def` functions.
- Serve built frontend assets with `app.frontend()` or `router.frontend()` instead of mounting `StaticFiles` manually.

## Tooling

- Package management and scripts: use `uv`.
- Linting and formatting: use Ruff.
- Type checking: use `ty`.
- Async utilities: use Asyncer when mixing async and blocking code.
- Database: use SQLModel over SQLAlchemy.
- HTTP client: use HTTPX over Requests.

## Streaming

- Server-Sent Events: use `response_class=EventSourceResponse` and `yield` items.
- JSON Lines and byte streaming: use `StreamingResponse` with generators.

## References

Detailed guidance is available in the skill files under `.agents/skills/fastapi/`:
- `references/pydantic.md`
- `references/responses.md`
- `references/streaming.md`
- `references/dependencies.md`
- `references/path-operations.md`
- `references/other-tools.md`
