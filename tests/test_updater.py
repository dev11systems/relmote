from unittest.mock import patch

from relmote.updater import update_repo_preview


@patch("relmote.updater.shutil.which", return_value="/usr/bin/pipx")
def test_update_check_does_not_run_pipx(which, capsys):
    result = update_repo_preview(dry_run=True)

    assert result == 0
    assert "Would update" in capsys.readouterr().out


@patch("relmote.updater.subprocess.run")
@patch("relmote.updater.shutil.which", return_value="/usr/bin/pipx")
def test_repo_update_uses_pipx_force_install(which, run):
    run.return_value.returncode = 0

    result = update_repo_preview()

    assert result == 0
    argv = run.call_args.args[0]
    assert argv[:3] == ["pipx", "install", "--force"]
    assert argv[-1].startswith("git+https://github.com/dev11systems/relmote")
