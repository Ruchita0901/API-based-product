import argparse
from uvicorn import run


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a selected API service.")
    parser.add_argument(
        "--service",
        choices=["record_label_api", "book_service"],
        default="record_label_api",
        help="Service to run.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind the selected service.",
    )
    args = parser.parse_args()

    if args.service == "record_label_api":
        from record_label_api.main import app
    else:
        from book_service.app import app

    run(app, host="0.0.0.0", port=args.port)


if __name__ == "__main__":
    main()
