from relmote.topology import Node, Path, Reachability, reachability


def test_interactive_path_wins():
    paths = (
        Path("mesh", "meshcore", interactive=True, constrained=True),
        Path("wifi", "wifi", interactive=True),
    )
    assert reachability(paths) is Reachability.INTERACTIVE


def test_constrained_path_is_distinct():
    paths = (Path("mesh", "meshcore", interactive=True, constrained=True),)
    assert reachability(paths) is Reachability.CONSTRAINED


def test_noninteractive_path_means_store_forward():
    paths = (Path("mailbox", "lora", interactive=False, constrained=True),)
    assert reachability(paths) is Reachability.STORE_FORWARD


def test_no_paths_is_offline():
    assert reachability(()) is Reachability.OFFLINE
