# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules, copy_metadata

block_cipher = None

hidden_imports = [
    # MCP SDK internals (v2: FastMCP -> mcp.server.mcpserver, wire types -> mcp_types)
    "mcp",
    "mcp.server",
    "mcp.server.mcpserver",
    "mcp.server.stdio",
    "mcp.server.sse",
    "mcp.server.streamable_http",
    "mcp.types",
    "mcp.shared",
    "mcp.shared.exceptions",
    *collect_submodules("mcp", filter=lambda name: not name.startswith("mcp.cli")),
    *collect_submodules("mcp_types"),
    # OpenTelemetry API (required by mcp 2.x, tracing is on by default)
    "opentelemetry",
    "opentelemetry.context",
    "opentelemetry.context.contextvars_context",
    "opentelemetry.propagate",
    "opentelemetry.propagators",
    "opentelemetry.trace",
    "opentelemetry.baggage",
    # ASGI / HTTP stack (used by MCP even in stdio mode)
    "starlette",
    "starlette.applications",
    "starlette.routing",
    "starlette.requests",
    "starlette.responses",
    "starlette.middleware",
    "sse_starlette",
    "anyio",
    "anyio._backends",
    "anyio._backends._asyncio",
    "httpx",
    "httpcore",
    "httpx2",
    "httpcore2",
    "truststore",
    "sniffio",
    "h11",
    "certifi",
    "idna",
    # Pydantic
    "pydantic",
    "pydantic.fields",
    "pydantic._internal",
    "pydantic_core",
    "annotated_types",
    "typing_extensions",
    # Standard library
    "json",
    "hashlib",
    "logging",
    "re",
    # Source package
    "src",
    "src.server",
    "src.models",
    "src.utils",
    # Async
    "asyncio",
    "concurrent.futures",
]

# Packages that read their own dist metadata at import time (httpx2/httpcore2 call
# importlib.metadata.version()) or discover plugins via entry points (opentelemetry).
datas = []
for dist in ("mcp", "mcp-types", "httpx2", "httpcore2", "opentelemetry-api", "pydantic"):
    datas += copy_metadata(dist)

a = Analysis(
    ["src/server.py"],
    pathex=["."],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter", "matplotlib", "numpy", "pandas", "PIL"],
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="br-community-mcp",
    debug=False,
    strip=False,
    upx=True,
    console=True,
    runtime_tmpdir=None,
)
