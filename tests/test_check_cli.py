from relmote.check_cli import run_check


def test_human_check_output(capsys):
    assert run_check() == 0
    output = capsys.readouterr().out

    assert "CHECK THIS COMPUTER" in output
    assert "Not-tested" in output


def test_json_check_output(capsys):
    assert run_check(as_json=True) == 0
    output = capsys.readouterr().out

    assert '"findings"' in output
    assert '"observations"' in output
