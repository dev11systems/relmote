import sys

from relmote.cli import build_parser


def test_parser_accepts_version():
    args = build_parser().parse_args(["version"])
    assert args.command == "version"


def test_parser_leaves_bare_command_for_app_launch():
    args = build_parser().parse_args([])
    assert args.command is None


def test_help_does_not_inherit_workspace_handler():
    parser = build_parser()
    # Building/parsing the top-level parser must not require workspace fields.
    args = parser.parse_args([])
    assert not hasattr(args, "target")


def test_parser_accepts_logs_command():
    args = build_parser().parse_args(["logs", "--tail", "25"])
    assert args.command == "logs"
    assert args.tail == 25
    assert args.path is False


def test_parser_accepts_logs_path_only():
    args = build_parser().parse_args(["logs", "--path"])
    assert args.command == "logs"
    assert args.path is True
