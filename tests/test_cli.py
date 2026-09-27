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
    assert args.save is None


def test_parser_accepts_logs_path_only():
    args = build_parser().parse_args(["logs", "--path"])
    assert args.command == "logs"
    assert args.path is True


def test_parser_accepts_logs_save_default_filename():
    args = build_parser().parse_args(["logs", "--save"])
    assert args.save == "relmote-debug.log"
    assert args.tail is None


def test_parser_accepts_logs_save_custom_filename():
    args = build_parser().parse_args(
        ["logs", "--tail", "250", "--save", "/tmp/relmote-debug.txt"]
    )
    assert args.save == "/tmp/relmote-debug.txt"
    assert args.tail == 250


def test_main_formats_permission_denial_without_traceback(monkeypatch, capsys):
    import relmote.cli as cli

    class Args:
        command = "agent"

        @staticmethod
        def func(args):
            raise PermissionError("agent capability not granted: terminal.exec")

    class Parser:
        @staticmethod
        def parse_args():
            return Args()

    monkeypatch.setattr(cli, "build_parser", lambda: Parser())

    assert cli.main() == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.strip() == (
        "Denied: agent capability not granted: terminal.exec"
    )
    assert "Traceback" not in captured.err
