from mcp_odds_api.server import mcp
from starlette.applications import Starlette
from mcp.server.sse import SseServerTransport
from starlette.requests import Request
from starlette.routing import Mount, Route
from mcp.server import Server
import uvicorn
import argparse
from starlette.middleware.cors import CORSMiddleware  # ✅ Add this import

def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    """Create a Starlette application that can serve the provided mcp server with SSE."""
    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> None:
        async with sse.connect_sse(
                request.scope,
                request.receive,
                request._send,  # noqa: SLF001
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )

    # ✅ Create Starlette app with routes
    app = Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )

    # ✅ Enable CORS for all origins (or restrict to ["http://127.0.0.1:8077"])
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app




def main():
    # Define a single parser for all arguments
    parser = argparse.ArgumentParser(description="mcp-bauplan: MCP server for Bauplan API")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="Transport protocol to use (stdio or sse)"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind to (SSE mode only)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Port to listen on (SSE mode only)"
    )
    args = parser.parse_args()

    # Handle the transport mode
    if args.transport == "stdio":
        mcp.run(transport=args.transport)
    else:  # sse mode
        mcp_server = mcp._mcp_server  # noqa: WPS437
        starlette_app = create_starlette_app(mcp_server, debug=True)
        uvicorn.run(starlette_app, host=args.host, port=args.port)

if __name__ == "__main__":
    main()