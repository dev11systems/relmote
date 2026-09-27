from relmote.cli import build_parser


def test_parser_accepts_hub_inventory():
    args = build_parser().parse_args(["hub", "inventory", "--live", "--json"])

    assert args.command == "hub"
    assert args.hub_command == "inventory"
    assert args.live is True
    assert args.json is True
