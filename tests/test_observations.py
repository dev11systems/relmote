from relmote.observations import (
    Completeness,
    Finding,
    Observation,
    ObservationKind,
    TaskResult,
)


def test_finding_references_evidence():
    observation = Observation(
        target_id="target:router",
        source_transport="ssh",
        kind=ObservationKind.TEXT,
        content="eth0: link up",
    )

    finding = Finding(
        statement="Ethernet link is up.",
        evidence_ids=(observation.observation_id,),
    )

    result = TaskResult(
        task_id="task-1",
        findings=(finding,),
        evidence_ids=(observation.observation_id,),
    )

    assert result.findings[0].evidence_ids == result.evidence_ids


def test_summary_is_marked_as_transformed():
    raw = Observation(
        target_id="target:router",
        source_transport="serial",
        kind=ObservationKind.TEXT,
        content="large raw log",
    )
    summary = Observation(
        target_id="target:router",
        source_transport="local-summary",
        kind=ObservationKind.STRUCTURED,
        content={"dhcp": "failed"},
        completeness=Completeness.SUMMARIZED,
        transformed_from=(raw.observation_id,),
    )

    assert summary.completeness is Completeness.SUMMARIZED
    assert summary.transformed_from == (raw.observation_id,)
