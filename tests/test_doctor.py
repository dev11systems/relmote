from relmote.doctor import DoctorCheck, doctor_exit_code, run_doctor_checks


def test_doctor_runs_on_ci_host():
    checks = run_doctor_checks()

    names = {check.name for check in checks}
    assert "Relmote" in names
    assert "Local diagnostics" in names
    assert "Local web interface" in names


def test_optional_missing_does_not_fail_doctor():
    checks = (
        DoctorCheck("core", "ok", "ok", True),
        DoctorCheck("tailscale", "optional-missing", "not found", False),
    )
    assert doctor_exit_code(checks) == 0


def test_required_failure_fails_doctor():
    checks = (DoctorCheck("core", "failed", "boom", True),)
    assert doctor_exit_code(checks) == 1
