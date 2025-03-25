# pyright: reportPrivateUsage=none

from typing import cast

import pytest

from object_ci.cdktf.cloudflare import CloudflareStack, RecordName


@pytest.mark.parametrize(
    ["input_name", "want_name", "want_display_name"],
    [
        ["@", "@", "ROOT"],
        [RecordName.ROOT, "@", "ROOT"],
        ["*", "*", "WILDCARD"],
        [RecordName.WILDCARD, "*", "WILDCARD"],
        ["", "", ""],
        ["name", "name", "name"],
        [None, "@", None],
    ],
)
def test_record_display_name(
    input_name: str | RecordName | None,
    want_name: str,
    want_display_name: str | None,
):
    mock_stack = cast(CloudflareStack, None)

    name, display_name = CloudflareStack._record_display_name(mock_stack, input_name)

    assert name == want_name
    assert display_name == want_display_name
