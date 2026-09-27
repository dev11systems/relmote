from relmote.cli import build_parser


def test_parser_accepts_hub_serve_tailscale():
    args = build_parser().parse_args(
        ["hub", "serve", "--tailscale", "--port", "9000", "--lifetime-minutes", "15"]
    )

    assert args.command == "hub"
    assert args.hub_command == "serve"
    assert args.tailscale is True
    assert args.port == 9000
    assert args.lifetime_minutes == 15
