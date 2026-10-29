from unittest.mock import AsyncMock, Mock

import httpx
import pytest
from dojo._exceptions import APIStatusError, APITimeoutError
from pydantic import ValidationError

from dojo import AsyncDojo, Dojo, NotFoundError, PermissionDeniedError
from dojo.resources.analysis import Analysis, AsyncAnalysis
from dojo.types.models import (
    ResearchAggregateResponse,
    ResearchDeleteResponse,
    ResearchListResponse,
    ResearchResultListResponse,
    ResearchResultSnapshotRequest,
    ResearchResultResponse,
    ResearchResultWriteResponse,
)

RESULT_BODY = {
    "task_name": "research-result",
    "title": "Energy supply result",
    "description": "Producer result metadata.",
    "observation_window": {"start_date": "2026-09-14", "end_date": "2026-09-28"},
    "probability_tier": None,
    "probability_pct": None,
    "outcome": "<p>Evidence is currently insufficient for a reliable probability.</p>",
    "outcome_markdown": "Evidence is currently insufficient for a reliable probability.",
    "thumbnail_base64": "dGh1bWJuYWlsLWNvdmVy",
    "timeline": [],
    "used_event_uids": [],
    "generation_time": "2026-09-14T10:00:00Z",
    "job_run_id": "job-20260914-001",
}

ROOT_BODY = {
    "research_uid": "research-energy-2026-001",
    "title": "Will the energy supply constraint ease?",
    "description": "Curated research metadata.",
    "observation_window": {"start_date": "2026-09-14", "end_date": "2026-09-28"},
    "sector_id": 42,
    "status": "tracking",
    "impact": "high",
    "visibility": "public",
    "timeline_source": "producer",
    "initial_result": RESULT_BODY,
}


def test_result_metadata_defaults_and_response_parsing() -> None:
    legacy = {key: value for key, value in RESULT_BODY.items() if key not in {"title", "description"}}
    request = ResearchResultSnapshotRequest.model_validate(legacy)
    assert request.title == "" and request.description == ""
    assert request.outcome_markdown == RESULT_BODY["outcome_markdown"]
    request_without_thumbnail = ResearchResultSnapshotRequest.model_validate(
        {key: value for key, value in RESULT_BODY.items() if key != "thumbnail_base64"}
    )
    assert request_without_thumbnail.thumbnail_base64 is None
    response = ResearchResultResponse.model_validate({**RESULT_BODY, "result_id": 901, "research_uid": "research-1"})
    assert response.title == RESULT_BODY["title"]
    assert response.description == RESULT_BODY["description"]
    assert response.outcome == RESULT_BODY["outcome"]
    assert response.outcome_markdown == RESULT_BODY["outcome_markdown"]
    assert response.thumbnail_base64 == RESULT_BODY["thumbnail_base64"]
    selected_response = ResearchResultResponse.model_validate(
        {
            **RESULT_BODY,
            "result_id": 903,
            "research_uid": "research-1",
            "outcome": None,
            "outcome_markdown": None,
            "thumbnail_base64": None,
            "producer_payload": {"outcome_markdown": RESULT_BODY["outcome_markdown"]},
        }
    )
    assert selected_response.outcome is None
    assert selected_response.outcome_markdown is None
    assert selected_response.thumbnail_base64 is None
    assert selected_response.producer_payload == {"outcome_markdown": RESULT_BODY["outcome_markdown"]}
    legacy_response = ResearchResultResponse.model_validate(
        {**{key: value for key, value in legacy.items() if key != "outcome_markdown"}, "result_id": 902, "research_uid": "research-1"}
    )
    assert legacy_response.outcome_markdown == ""
    with pytest.raises(ValidationError):
        ResearchResultSnapshotRequest.model_validate({**RESULT_BODY, "title": "x" * 513})


def test_market_research_sync_routes_and_preserves_nullable_result_fields() -> None:
    client = Mock()
    client.get.return_value = ResearchListResponse(page=1, size=10, total_num=0, total_page=0, num=0, data=[])
    client.post.return_value = ResearchResultWriteResponse(result_id=901)

    Analysis(client).list_market_research(scope="mine", is_editor_pick=True, sector_id=42, status="tracking", limit=25, offset=5)
    client.get.assert_called_once_with(
        "/api/qdata/v1/analysis/research",
        cast_to=ResearchListResponse,
        options={"params": {"scope": "mine", "is_editor_pick": True, "sector_id": 42, "status": "tracking", "limit": 25, "offset": 5}},
    )

    client.reset_mock()
    result = Analysis(client).create_market_research_result(
        "research-energy-2026-001",
        body=RESULT_BODY,
    )

    assert result.result_id == 901
    client.post.assert_called_once_with(
        "/api/qdata/v1/analysis/research/research-energy-2026-001/results",
        cast_to=ResearchResultWriteResponse,
        options={"json": {**RESULT_BODY, "research_uid": None, "extra": {}}, "max_retries": 0},
    )


def test_market_research_sync_root_result_and_timeline_methods() -> None:
    client = Mock()
    client.post.return_value = ResearchAggregateResponse.model_validate(
        {
            **ROOT_BODY,
            "owner_user_id": "producer-admin",
            "latest_result": None,
            "latest_probability_tier": None,
            "latest_probability_pct": None,
            "related_sector": None,
            "extra": {},
            "timeline": [],
        }
    )
    client.get.return_value = ResearchAggregateResponse.model_validate(
        {
            **ROOT_BODY,
            "owner_user_id": "producer-admin",
            "latest_result": None,
            "latest_probability_tier": None,
            "latest_probability_pct": None,
            "related_sector": None,
            "extra": {},
            "timeline": [],
        }
    )
    client.put.return_value = client.post.return_value

    analysis = Analysis(client)
    analysis.create_market_research(body=ROOT_BODY)
    client.post.assert_called_once()
    assert client.post.call_args.args[0] == "/api/qdata/v1/analysis/research"
    assert client.post.call_args.kwargs["cast_to"] is ResearchAggregateResponse
    assert client.post.call_args.kwargs["options"]["json"]["initial_result"]["probability_pct"] is None
    assert client.post.call_args.kwargs["options"]["json"]["initial_result"]["thumbnail_base64"] == RESULT_BODY["thumbnail_base64"]

    analysis.get_market_research(ROOT_BODY["research_uid"])
    client.get.assert_called_with(
        "/api/qdata/v1/analysis/research/research-energy-2026-001",
        cast_to=ResearchAggregateResponse,
        options={},
    )

    analysis.get_market_research(ROOT_BODY["research_uid"], result_content_fields="thumbnail_base64")
    client.get.assert_called_with(
        "/api/qdata/v1/analysis/research/research-energy-2026-001",
        cast_to=ResearchAggregateResponse,
        options={"params": {"result_content_fields": "thumbnail_base64"}},
    )

    analysis.list_market_research_results(ROOT_BODY["research_uid"], limit=10, offset=20)
    client.get.assert_called_with(
        "/api/qdata/v1/analysis/research/research-energy-2026-001/results",
        cast_to=ResearchResultListResponse,
        options={"params": {"limit": 10, "offset": 20}},
    )

    analysis.replace_market_research_timeline(ROOT_BODY["research_uid"], body={"items": []})
    client.put.assert_called_with(
        "/api/qdata/v1/analysis/research/research-energy-2026-001/timeline",
        cast_to=ResearchAggregateResponse,
        options={"json": {"items": []}},
    )


def test_market_research_result_rejects_legacy_wire_fields() -> None:
    client = Mock()

    with pytest.raises(ValidationError):
        Analysis(client).create_market_research_result(
            "research-energy-2026-001",
            body={**RESULT_BODY, "decision_logic": "legacy"},
        )

    client.post.assert_not_called()


def test_market_research_sync_list_forwards_query_contract() -> None:
    client = Mock()
    client.get.return_value = ResearchListResponse(page=2, size=3, total_num=4, total_page=2, num=1, data=[])

    Analysis(client).list_market_research(
        scope="public",
        sector_id=42,
        status="tracking",
        start_time="2026-09-01",
        end_time="2026-09-30",
        fuzzy="resolve",
        result_content_fields="outcome,thumbnail_base64",
        order_by="title",
        order_type="asc",
        page=2,
        size=3,
    )

    client.get.assert_called_once_with(
        "/api/qdata/v1/analysis/research",
        cast_to=ResearchListResponse,
        options={
            "params": {
                "scope": "public",
                "sector_id": 42,
                "status": "tracking",
                "start_time": "2026-09-01",
                "end_time": "2026-09-30",
                "fuzzy": "resolve",
                "result_content_fields": "outcome,thumbnail_base64",
                "order_by": "title",
                "order_type": "asc",
                "page": 2,
                "size": 3,
            }
        },
    )

    client.reset_mock()
    client.get.return_value = ResearchResultListResponse(page=1, size=5, total_num=0, total_page=0, num=0, data=[])
    Analysis(client).list_market_research_results(
        "research-energy-2026-001",
        start_time="2026-09-01T00:00:00Z",
        end_time="2026-09-30T00:00:00+00:00",
        fuzzy="evidence",
        result_content_fields="outcome_markdown,thumbnail_base64",
        order_by="task_name",
        order_type="asc",
        page=1,
        size=5,
    )
    client.get.assert_called_once_with(
        "/api/qdata/v1/analysis/research/research-energy-2026-001/results",
        cast_to=ResearchResultListResponse,
        options={
            "params": {
                "start_time": "2026-09-01T00:00:00Z",
                "end_time": "2026-09-30T00:00:00+00:00",
                "fuzzy": "evidence",
                "result_content_fields": "outcome_markdown,thumbnail_base64",
                "order_by": "task_name",
                "order_type": "asc",
                "page": 1,
                "size": 5,
            }
        },
    )


@pytest.mark.asyncio
async def test_market_research_async_result_matches_sync_wire_contract() -> None:
    client = Mock()
    client.post = AsyncMock(return_value=ResearchResultWriteResponse(result_id=901))

    result = await AsyncAnalysis(client).create_market_research_result(
        "research-energy-2026-001",
        body=RESULT_BODY,
    )

    assert result.result_id == 901
    client.post.assert_awaited_once_with(
        "/api/qdata/v1/analysis/research/research-energy-2026-001/results",
        cast_to=ResearchResultWriteResponse,
        options={"json": {**RESULT_BODY, "research_uid": None, "extra": {}}, "max_retries": 0},
    )


@pytest.mark.asyncio
async def test_market_research_async_root_and_list_routes() -> None:
    client = Mock()
    client.get = AsyncMock(return_value=ResearchListResponse(page=1, size=10, total_num=0, total_page=0, num=0, data=[]))
    client.post = AsyncMock(return_value=ResearchResultWriteResponse(result_id=901))
    client.put = AsyncMock()

    analysis = AsyncAnalysis(client)
    await analysis.list_market_research(scope="mine", is_editor_pick=False)
    client.get.assert_awaited_once_with(
        "/api/qdata/v1/analysis/research",
        cast_to=ResearchListResponse,
        options={"params": {"scope": "mine", "is_editor_pick": False}},
    )

    client.get.reset_mock()
    await analysis.get_market_research(ROOT_BODY["research_uid"], result_content_fields="outcome,thumbnail_base64")
    client.get.assert_awaited_once_with(
        "/api/qdata/v1/analysis/research/research-energy-2026-001",
        cast_to=ResearchAggregateResponse,
        options={"params": {"result_content_fields": "outcome,thumbnail_base64"}},
    )

    await analysis.create_market_research_result(ROOT_BODY["research_uid"], body=RESULT_BODY)
    client.post.assert_awaited_once_with(
        "/api/qdata/v1/analysis/research/research-energy-2026-001/results",
        cast_to=ResearchResultWriteResponse,
        options={"json": {**RESULT_BODY, "research_uid": None, "extra": {}}, "max_retries": 0},
    )


@pytest.mark.parametrize("typed_body", [False, True])
def test_update_market_research_result_sync(typed_body: bool) -> None:
    client = Mock()
    client.put.return_value = ResearchResultWriteResponse(result_id=901)
    payload = {**RESULT_BODY, "extra": {"source": "correction"}}
    body = ResearchResultSnapshotRequest.model_validate(payload) if typed_body else payload

    result = Analysis(client).update_market_research_result("research-1", 901, body=body)

    assert result.result_id == 901
    client.put.assert_called_once_with(
        "/api/qdata/v1/analysis/research/research-1/results/901",
        cast_to=ResearchResultWriteResponse,
        options={"json": {**payload, "research_uid": None}},
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("typed_body", [False, True])
async def test_update_market_research_result_async(typed_body: bool) -> None:
    client = Mock()
    client.put = AsyncMock(return_value=ResearchResultWriteResponse(result_id=901))
    payload = {**RESULT_BODY, "extra": {"source": "correction"}}
    body = ResearchResultSnapshotRequest.model_validate(payload) if typed_body else payload

    result = await AsyncAnalysis(client).update_market_research_result("research-1", 901, body=body)

    assert result.result_id == 901
    client.put.assert_awaited_once_with(
        "/api/qdata/v1/analysis/research/research-1/results/901",
        cast_to=ResearchResultWriteResponse,
        options={"json": {**payload, "research_uid": None}},
    )


def test_update_market_research_result_validates_before_sending() -> None:
    client = Mock()
    with pytest.raises(ValidationError):
        Analysis(client).update_market_research_result("research-1", 901, body={**RESULT_BODY, "decision_logic": "legacy"})
    client.put.assert_not_called()


@pytest.mark.asyncio
async def test_update_market_research_result_async_validates_before_sending() -> None:
    client = Mock()
    client.put = AsyncMock()
    with pytest.raises(ValidationError):
        await AsyncAnalysis(client).update_market_research_result("research-1", 901, body={**RESULT_BODY, "decision_logic": "legacy"})
    client.put.assert_not_awaited()


@pytest.mark.parametrize("return_raw_data", [False, True])
def test_delete_market_research_sync_http_contract(monkeypatch, return_raw_data: bool) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")
    payload = {"result": "success", "research_uid": ROOT_BODY["research_uid"]}
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={"code": 0, "data": payload})

    with httpx.Client(transport=httpx.MockTransport(handler)) as http_client:
        client = Dojo(api_key="test", base_url="https://dojo.test", http_client=http_client, return_raw_data=return_raw_data)
        response = client.analysis.delete_market_research(ROOT_BODY["research_uid"])

    assert len(seen) == 1
    assert seen[0].method == "DELETE"
    assert str(seen[0].url) == "https://dojo.test/api/qdata/v1/analysis/research/research-energy-2026-001"
    assert seen[0].content == b""
    assert seen[0].headers["Authorization"] == "Bearer test"
    if return_raw_data:
        assert response == payload
    else:
        assert isinstance(response, ResearchDeleteResponse)
        assert response.model_dump() == payload


@pytest.mark.asyncio
@pytest.mark.parametrize("return_raw_data", [False, True])
async def test_delete_market_research_async_http_contract(monkeypatch, return_raw_data: bool) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")
    payload = {"result": "success", "research_uid": ROOT_BODY["research_uid"]}
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={"code": 0, "data": payload})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http_client:
        client = AsyncDojo(api_key="test", base_url="https://dojo.test", http_client=http_client, return_raw_data=return_raw_data)
        response = await client.analysis.delete_market_research(ROOT_BODY["research_uid"])

    assert len(seen) == 1
    assert seen[0].method == "DELETE"
    assert str(seen[0].url) == "https://dojo.test/api/qdata/v1/analysis/research/research-energy-2026-001"
    assert seen[0].content == b""
    assert seen[0].headers["Authorization"] == "Bearer test"
    if return_raw_data:
        assert response == payload
    else:
        assert isinstance(response, ResearchDeleteResponse)
        assert response.model_dump() == payload


@pytest.mark.parametrize("status_code,error_type", [(403, PermissionDeniedError), (404, NotFoundError)])
def test_delete_market_research_sync_propagates_api_errors(monkeypatch, status_code, error_type) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")
    body = {"detail": "research cannot be deleted"}

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code, json=body)

    with httpx.Client(transport=httpx.MockTransport(handler)) as http_client:
        client = Dojo(api_key="test", base_url="https://dojo.test", http_client=http_client, max_retries=0)
        with pytest.raises(error_type) as exc_info:
            client.analysis.delete_market_research(ROOT_BODY["research_uid"])

    assert exc_info.value.status_code == status_code
    assert exc_info.value.body == body


@pytest.mark.asyncio
@pytest.mark.parametrize("status_code,error_type", [(403, PermissionDeniedError), (404, NotFoundError)])
async def test_delete_market_research_async_propagates_api_errors(monkeypatch, status_code, error_type) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")
    body = {"detail": "research cannot be deleted"}

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code, json=body)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http_client:
        client = AsyncDojo(api_key="test", base_url="https://dojo.test", http_client=http_client, max_retries=0)
        with pytest.raises(error_type) as exc_info:
            await client.analysis.delete_market_research(ROOT_BODY["research_uid"])

    assert exc_info.value.status_code == status_code
    assert exc_info.value.body == body


@pytest.mark.parametrize("value", [None, "", " \n\t"])
def test_result_request_requires_non_blank_markdown(value) -> None:
    for body in ({key: item for key, item in RESULT_BODY.items() if key != "outcome_markdown"}, {**RESULT_BODY, "outcome_markdown": value}):
        with pytest.raises(ValidationError, match="outcome_markdown"):
            ResearchResultSnapshotRequest.model_validate(body)


@pytest.mark.asyncio
@pytest.mark.parametrize("async_mode", [False, True])
@pytest.mark.parametrize("failure", [500, 422, "timeout"])
async def test_result_append_never_retries_and_reads_keep_retry_configuration(async_mode, failure):
    requests = []

    def transport(request):
        requests.append(request)
        if failure == "timeout":
            raise httpx.ReadTimeout("uncertain write", request=request)
        return httpx.Response(failure, json={"message": "outcome_markdown diagnostic", "code": failure})

    http_type, client_type = (httpx.AsyncClient, AsyncDojo) if async_mode else (httpx.Client, Dojo)
    client = client_type(api_key="test", online=True, max_retries=3, http_client=http_type(transport=httpx.MockTransport(transport)))
    client._calculate_retry_delay = lambda *args: 0
    try:
        with pytest.raises((APIStatusError, APITimeoutError)) as caught:
            result = client.analysis.create_market_research_result("research-1", body=RESULT_BODY)
            if async_mode:
                await result
        assert len(requests) == 1
        if failure != "timeout":
            assert "outcome_markdown diagnostic" in str(caught.value)
        with pytest.raises((APIStatusError, APITimeoutError)):
            result = client.get("/read-probe", cast_to=dict)
            if async_mode:
                await result
        assert len(requests) == (2 if failure == 422 else 5)
        assert client.max_retries == 3
    finally:
        if async_mode:
            await client._client.aclose()
        else:
            client._client.close()


@pytest.mark.parametrize("field", ["observation_window", "sector_id", "impact"])
def test_public_research_nullable_fields_remain_required(field):
    from dojo.types.models import PublicResearchCardResponse, ResearchCardResponse

    card = {**ROOT_BODY, "owner_user_id": "owner", "is_editor_pick": False, field: None}
    assert getattr(PublicResearchCardResponse.model_validate(card), field) is None
    assert getattr(ResearchCardResponse.model_validate(card), field) is None
    del card[field]
    with pytest.raises(ValidationError):
        PublicResearchCardResponse.model_validate(card)


def test_public_research_contract_and_sync_route():
    from dojo.types import PublicResearchCardResponse, PublicResearchListResponse

    card = {**ROOT_BODY, "owner_user_id": "owner", "is_editor_pick": False}
    assert PublicResearchCardResponse.model_validate(card).is_editor_pick is False
    with pytest.raises(ValidationError):
        PublicResearchCardResponse.model_validate({**card, "visibility": "private"})
    with pytest.raises(ValidationError):
        PublicResearchCardResponse.model_validate({k: v for k, v in card.items() if k != "is_editor_pick"})
    client = Mock()
    params = dict(
        page=1,
        size=10,
        is_editor_pick=False,
        offset=0,
        limit=25,
        impact="high",
        timeline_source="manual",
        result_content_fields="thumbnail_base64",
    )
    Analysis(client).list_public_market_research(**params)
    client.get.assert_called_once_with("/api/qdata/v1/analysis/public_research", cast_to=PublicResearchListResponse, options={"params": params})
    with pytest.raises(TypeError):
        Analysis(client).list_public_market_research(scope="mine")
    with pytest.raises(TypeError):
        Analysis(client).list_public_market_research(visibility="private")
    client.reset_mock()
    Analysis(client).list_market_research(impact="high", timeline_source="producer", visibility="private")
    assert client.get.call_args.kwargs["options"]["params"] == dict(impact="high", timeline_source="producer", visibility="private")


@pytest.mark.asyncio
async def test_public_research_async_route_and_common_filter_parity():
    from dojo.types import PublicResearchListResponse

    client = Mock()
    client.get = AsyncMock()
    params = dict(
        page=2,
        size=18,
        is_editor_pick=False,
        offset=0,
        fuzzy="supply",
        start_time="2026-10-01",
        end_time="2026-10-19",
        sector_id=42,
        status="tracking",
        impact="severe",
        timeline_source="manual",
        result_content_fields="outcome_markdown,thumbnail_base64",
        order_by="title",
        order_type="asc",
        limit=30,
    )
    await AsyncAnalysis(client).list_public_market_research(**params)
    client.get.assert_awaited_once_with("/api/qdata/v1/analysis/public_research", cast_to=PublicResearchListResponse, options={"params": params})
    client.get.reset_mock()
    await AsyncAnalysis(client).list_market_research(impact="high", timeline_source="producer", visibility="private")
    assert client.get.call_args.kwargs["options"]["params"] == dict(impact="high", timeline_source="producer", visibility="private")


@pytest.mark.asyncio
@pytest.mark.parametrize("async_mode", [False, True])
@pytest.mark.parametrize("visibility", ["private", "public"])
@pytest.mark.parametrize("research_type", [None, "", "event", "x" * 64])
async def test_create_research_type_and_visibility_http_contract(async_mode, visibility, research_type):
    import json

    requests = []
    body = {**ROOT_BODY, "visibility": visibility, "research_type": research_type}

    def transport(request):
        requests.append(request)
        sent = json.loads(request.content)
        return httpx.Response(200, json={"code": 0, "data": {**sent, "owner_user_id": "owner", "timeline": []}})

    http_type, client_type = (httpx.AsyncClient, AsyncDojo) if async_mode else (httpx.Client, Dojo)
    http_client = http_type(transport=httpx.MockTransport(transport))
    client = client_type(api_key="test", online=True, http_client=http_client, return_raw_data=False)
    try:
        response = client.analysis.create_market_research(body=body)
        if async_mode:
            response = await response
        assert response.research_type == research_type
        assert response.visibility == visibility
    finally:
        if async_mode:
            await http_client.aclose()
        else:
            http_client.close()
    assert len(requests) == 1
    assert requests[0].method == "POST" and requests[0].url.path == "/api/qdata/v1/analysis/research"
    assert json.loads(requests[0].content)["research_type"] == research_type
    assert json.loads(requests[0].content)["visibility"] == visibility


@pytest.mark.parametrize(
    "body",
    [
        {"research_type": "x" * 65},
        {"research_type": 123},
        {"visibility": "unlisted"},
        {"visibility": None},
    ],
)
def test_create_research_rejects_invalid_type_and_visibility_before_sending(body):
    client = Mock()
    with pytest.raises(ValidationError):
        Analysis(client).create_market_research(body={**ROOT_BODY, **body})
    client.post.assert_not_called()


def test_create_research_preserves_legacy_private_default_and_optional_type():
    from dojo.types.models import ResearchCreateRequest

    request = ResearchCreateRequest.model_validate({key: value for key, value in ROOT_BODY.items() if key != "visibility"})
    assert request.visibility == "private"
    assert request.research_type is None


@pytest.mark.parametrize("ambient_key", [None, "ambient-secret"])
def test_public_research_anonymous_sync_no_credentials_or_private_access(monkeypatch, ambient_key):
    from dojo import DojoError

    monkeypatch.delenv("DOJO_API_KEY", raising=False)
    if ambient_key:
        monkeypatch.setenv("DOJO_API_KEY", ambient_key)
    seen = []

    def handler(request):
        seen.append(request)
        return httpx.Response(200, json={"page": 1, "size": 10, "total_num": 0, "total_page": 0, "num": 0, "data": []})

    with httpx.Client(
        transport=httpx.MockTransport(handler), auth=("user", "password"), headers={"Authorization": "Bearer transport-secret", "Cookie": "session=secret"}
    ) as transport:
        client = Dojo(anonymous=True, online=True, http_client=transport, default_headers={"Authorization": "Bearer default-secret"})
        assert client.api_key is None and not client.auth_headers
        result = client.analysis.list_public_market_research(is_editor_pick=False, offset=0)
        assert result["data"] == []
        assert seen[0].url.path == "/api/qdata/v1/analysis/public_research"
        assert "authorization" not in seen[0].headers and "cookie" not in seen[0].headers
        assert seen[0].url.params["is_editor_pick"] == "false"
        for method, path in [("GET", "/api/qdata/v1/analysis/research"), ("POST", "/api/qdata/v1/analysis/public_research")]:
            with pytest.raises(DojoError, match="Anonymous clients only"):
                client.request(method, path, cast_to=dict)
        assert len(seen) == 1


@pytest.mark.asyncio
async def test_public_research_anonymous_async_no_credentials_or_private_access(monkeypatch):
    from dojo import DojoError

    monkeypatch.delenv("DOJO_API_KEY", raising=False)
    seen = []

    async def handler(request):
        seen.append(request)
        return httpx.Response(200, json={"page": 1, "size": 10, "total_num": 0, "total_page": 0, "num": 0, "data": []})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler), auth=("user", "password"), headers={"Cookie": "session=secret"}) as transport:
        client = AsyncDojo(anonymous=True, api_key="ignored-explicit-secret", online=True, http_client=transport)
        result = await client.analysis.list_public_market_research()
        assert result["data"] == [] and client.api_key is None
        assert seen[0].url.path == "/api/qdata/v1/analysis/public_research"
        assert "authorization" not in seen[0].headers and "cookie" not in seen[0].headers
        with pytest.raises(DojoError, match="Anonymous clients only"):
            await client.analysis.list_market_research()
        assert len(seen) == 1


@pytest.mark.parametrize("factory", [Dojo, AsyncDojo])
def test_default_clients_still_require_credentials(monkeypatch, factory):
    from dojo import DojoError

    monkeypatch.delenv("DOJO_API_KEY", raising=False)
    with pytest.raises(DojoError, match="Missing authentication credentials"):
        factory(online=True)
    with pytest.raises(DojoError, match="requires online access"):
        factory(anonymous=True, online=False)


@pytest.mark.asyncio
@pytest.mark.parametrize("async_mode", [False, True])
@pytest.mark.parametrize("body", [{"visibility": "public", "research_type": "daily-event"}, {"research_type": None}])
async def test_update_research_sends_only_explicit_fields_and_preserves_identity(async_mode, body):
    import json

    requests = []

    def transport(request):
        requests.append(request)
        return httpx.Response(200, json={"code": 0, "data": {**ROOT_BODY, **body, "owner_user_id": "owner", "timeline": []}})

    http_type, client_type = (httpx.AsyncClient, AsyncDojo) if async_mode else (httpx.Client, Dojo)
    http_client = http_type(transport=httpx.MockTransport(transport))
    client = client_type(api_key="test", online=True, http_client=http_client, return_raw_data=False, default_headers={"UserId": "user", "OrgId": "org"})
    try:
        result = client.analysis.update_market_research(ROOT_BODY["research_uid"], body=body)
        if async_mode:
            result = await result
        assert result.research_uid == ROOT_BODY["research_uid"]
        assert result.research_type == body["research_type"]
    finally:
        if async_mode:
            await http_client.aclose()
        else:
            http_client.close()
    assert len(requests) == 1
    assert requests[0].method == "PUT"
    assert requests[0].url.path == f"/api/qdata/v1/analysis/research/{ROOT_BODY['research_uid']}"
    assert json.loads(requests[0].content) == body
    assert requests[0].headers["UserId"] == "user" and requests[0].headers["OrgId"] == "org"
    assert requests[0].headers["Authorization"] == "Bearer test"


@pytest.mark.asyncio
@pytest.mark.parametrize("async_mode", [False, True])
async def test_update_research_never_retries_server_error(async_mode):
    requests = []

    def transport(request):
        requests.append(request)
        return httpx.Response(500, json={"code": 500, "message": "update outcome unknown"})

    http_type, client_type = (httpx.AsyncClient, AsyncDojo) if async_mode else (httpx.Client, Dojo)
    http_client = http_type(transport=httpx.MockTransport(transport))
    client = client_type(api_key="test", online=True, max_retries=3, http_client=http_client)
    try:
        with pytest.raises(APIStatusError):
            result = client.analysis.update_market_research(ROOT_BODY["research_uid"], body={"visibility": "public", "research_type": "daily-event"})
            if async_mode:
                await result
    finally:
        if async_mode:
            await http_client.aclose()
        else:
            http_client.close()
    assert len(requests) == 1


@pytest.mark.parametrize("body", [{"owner_user_id": "forged"}, {"title": ""}, {"research_type": "x" * 65}, {"visibility": "unlisted"}, {"sector_id": 0}])
def test_update_research_rejects_invalid_fields_before_sending(body):
    client = Mock()
    with pytest.raises(ValidationError):
        Analysis(client).update_market_research("r-0123456789abcdef", body=body)
    client.put.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.parametrize("async_mode", [False, True])
async def test_starred_scope_annotation_and_wire_parameter(async_mode):
    from typing import get_args, get_type_hints

    resource = AsyncAnalysis if async_mode else Analysis
    union = get_type_hints(resource.list_market_research)["scope"]
    scope_values = next(get_args(value) for value in get_args(union) if get_args(value))
    assert set(scope_values) == {"public", "mine", "starred"}
    seen = []

    def handler(request):
        seen.append(request)
        return httpx.Response(200, json={"page": 1, "size": 18, "total_num": 0, "total_page": 0, "num": 0, "data": []})

    http_class, sdk_class = (httpx.AsyncClient, AsyncDojo) if async_mode else (httpx.Client, Dojo)
    transport = http_class(transport=httpx.MockTransport(handler))
    sdk = sdk_class(api_key="test", online=True, http_client=transport)
    try:
        result = sdk.analysis.list_market_research(scope="starred", page=1, size=18, order_type="desc")
        if async_mode:
            await result
    finally:
        if async_mode:
            await transport.aclose()
        else:
            transport.close()
    assert len(seen) == 1 and seen[0].url.params["scope"] == "starred"
    assert seen[0].url.path == "/api/qdata/v1/analysis/research"
