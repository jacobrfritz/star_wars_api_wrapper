import argparse
import sys

import uvicorn

from base_fast_api.config import settings


def parse_args(args: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Base FastAPI Project Server Runner")
    parser.add_argument(
        "--host",
        type=str,
        default=settings.HOST,
        help=f"Host interface to bind the server to (default: {settings.HOST})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=settings.PORT,
        help=f"Port number to listen on (default: {settings.PORT})",
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        default=settings.DEBUG,
        help=f"Enable development hot-reloading (default: {settings.DEBUG})",
    )
    return parser.parse_args(args)


def main() -> None:
    parsed_args = parse_args(sys.argv[1:])
    uvicorn.run(
        "base_fast_api.main:app",
        host=parsed_args.host,
        port=parsed_args.port,
        reload=parsed_args.reload,
    )


if __name__ == "__main__":
    main()
