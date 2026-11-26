"""Protocol-level tests that drive the server through the MCP SDK's in-memory client."""

import pytest
import respx
from httpx import Response
from mcp.client import Client

from src.server import mcp
from src.utils import BASE_URL

EXPECTED_TOOLS = {
    "search_community",
    "get_topic",
    "list_categories",
    "get_latest_topics",
    "get_top_topics",
}


@pytest.mark.asyncio
async def test_initialize_list_and_call_tool() -> None:
    """initialize, tools/list and tools/call work over the in-memory JSON-RPC transport."""
    with respx.mock:
        respx.get(f"{BASE_URL}/search.json").mock(
            return_value=Response(
                200,
                json={
                    "posts": [
                        {
                            "id": 1,
                            "topic_id": 100,
                            "username": "testuser",
                            "blurb": "mappView widgets",
                            "post_number": 1,
                        }
                    ],
                    "topics": [{"id": 100, "title": "mappView Widget Question"}],
                },
            )
        )

        # mode="legacy" forces the classic initialize handshake over JSON-RPC
        async with Client(mcp, mode="legacy", raise_exceptions=True) as client:
            assert client.server_info is not None
            assert client.server_info.name == "B&R Community"
            assert client.instructions and "B&R Automation" in client.instructions

            tools = await client.list_tools()
            assert {t.name for t in tools.tools} == EXPECTED_TOOLS

            result = await client.call_tool("search_community", {"query": "mappView"})
            assert not result.is_error
            assert result.structured_content is not None
            assert result.structured_content["total_posts"] == 1
            assert (
                result.structured_content["posts"][0]["topic_title"]
                == "mappView Widget Question"
            )
