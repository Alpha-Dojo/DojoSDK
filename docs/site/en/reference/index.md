# Reference

This category records stable interfaces, contracts, and lists that
callers can rely on.

- [Offline compatibility removals for the next major release](offline-deprecations.md): interfaces pending removal, replacements, the removal gate, and migration examples.

## MarketResearch write contract (0.1.31)

`create_market_research_result(research_uid, *, body)` appends one result and requires HTML `outcome` plus non-blank Markdown `outcome_markdown`. Missing, empty, null, or whitespace-only Markdown is rejected before sending. Historical responses may still omit Markdown and default to an empty string.

Sync and async appends force `max_retries=0` without changing retry configuration for reads. A 500, timeout, or connection failure may follow a successful write; read back the result and resolve manually before appending again. HTTP error messages support both FastAPI `detail` and qdata `message`; the original response remains available as exception `body`.

## MarketResearch result content contract (0.1.32)

Result snapshots accept an optional `thumbnail_base64` field containing a Base64-encoded thumbnail cover image. This applies to `initial_result` during research creation, result appends, and result corrections.

Research lists, `public_research` lists, research detail, and result history queries all accept `result_content_fields`. It is a comma-separated selection of `outcome`, `outcome_markdown`, and `thumbnail_base64`, for example `result_content_fields="outcome,thumbnail_base64"`. Unselected content fields are returned as `None`; omitting the parameter returns all three fields. The server applies the same selection to `producer_payload`.

Use `client.analysis.list_public_market_research(page=1, size=10)` for strictly public research; AsyncDojo provides the same async method. It reads `/api/qdata/v1/analysis/public_research`, accepts no scope/visibility, and adds no public detail or write API. Domain filters, sorting and both pagination forms are supported; false and offset=0 are preserved. PublicResearchListResponse / PublicResearchCardResponse require public visibility and is_editor_pick. The required observation_window/sector_id/impact fields allow null. Existing list_market_research keeps its route and adds impact/timeline_source/visibility filters.


`create_market_research(body=...)` accepts optional `research_type` (a string up to 64 characters, or null) in both sync and async clients. `visibility` accepts `private` or `public`; the SDK preserves the existing `private` default and always sends it. Typed research card responses (`return_raw_data=False`) from create, detail, and list expose optional `research_type`, defaulting to None when absent.


Use `Dojo(anonymous=True, online=True)` or `AsyncDojo(anonymous=True, online=True)` to read the public research list without an API key. This opt-in mode ignores explicit/environment keys, strips Authorization/Cookie, and locally rejects all operations except GET public_research. Default authenticated behavior is unchanged. Optional identity headers must come from a trusted server; anonymous callers need none.


`analysis.update_market_research(research_uid, body=...)` uses `PUT /api/qdata/v1/analysis/research/{research_uid}` and returns the research aggregate in sync and async clients. `ResearchUpdateRequest` sends only explicitly supplied fields, preserving explicit nulls; `{"visibility":"public","research_type":"daily-event"}` leaves title/description/extra untouched. It does not append a result and forces `max_retries=0`. Resolve an unknown response by reading the research ID or manual review without replaying result appends.


Use `list_market_research(scope="starred")` for the current caller's starred research in sync or async mode. Allowed scopes are public/mine/starred; the public-only list still accepts no scope. Sort direction is asc/desc without quotes.
