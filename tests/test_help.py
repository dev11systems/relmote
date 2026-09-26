import pytest

from relmote.help import render_help, topic_names


def test_general_help_is_plain_language():
    text = render_help()

    assert "GETTING STARTED" in text
    assert "relmote doctor" in text
    assert "relmote update" in text


def test_help_topics_include_core_user_tasks():
    names = topic_names()

    assert "support" in names
    assert "remote" in names
    assert "workspace" in names
    assert "privacy" in names


def test_unknown_topic_explains_available_topics():
    with pytest.raises(ValueError, match="Available topics"):
        render_help("nope")
