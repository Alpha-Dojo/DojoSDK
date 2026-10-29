# Reference

本分类记录调用方可以依赖的稳定接口、契约与清单。

- [下一代大版本的离线兼容性移除清单](offline-deprecations.md)：待移除接口、替代方案、移除门槛与迁移示例。

## MarketResearch 写入契约（0.1.31）

`create_market_research_result(research_uid, *, body)` 追加一次结果，必须同时提供 HTML `outcome` 和非空白 Markdown `outcome_markdown`；缺失、空字符串、null 或纯空白 Markdown 会在发送前拒绝。历史响应仍允许缺失 Markdown，并按空字符串读取。

同步与异步结果追加均强制 `max_retries=0`，不改变客户端读请求的重试配置。500、超时和连接失败可能存在写入副作用；先读取结果核验，再人工决定恢复，禁止盲目重复追加。HTTP 错误文本同时支持 FastAPI `detail` 和 qdata `message`，原始响应仍保存在异常 `body` 中。

## MarketResearch 结果内容契约（0.1.32）

结果快照可通过可空的 `thumbnail_base64` 字段写入 Base64 编码的缩略封面图，包括创建 research 时的 `initial_result`、追加 result 和修正 result。

research 列表、`public_research` 列表、research 详情和 result 历史查询均接受 `result_content_fields`。该参数使用逗号分隔，可选择 `outcome`、`outcome_markdown` 和 `thumbnail_base64`，例如 `result_content_fields="outcome,thumbnail_base64"`。未选择的内容字段返回 `None`；不传参数时返回全部三个字段。服务端也会按相同选择过滤 `producer_payload`。

纯公开研究使用 `client.analysis.list_public_market_research(page=1, size=10)`；AsyncDojo 使用同名异步方法。此方法固定读取 `/api/qdata/v1/analysis/public_research`，不接受 scope/visibility，不提供公开研究的写入或详情能力。支持行业、研究状态、impact、timeline_source、is_editor_pick、日期、搜索、排序及两组分页参数；false/offset=0 原样保留。响应 PublicResearchListResponse / PublicResearchCardResponse 中 visibility 固定 public，is_editor_pick 必填，observation_window/sector_id/impact 字段必填但允许 null。通用 list_market_research 继续查询原路径，现支持 impact/timeline_source/visibility。


`create_market_research(body=...)` 的 `research_type` 为可选字符串（最多 64 字符，可为 null），同步和异步客户端均原样发送。`visibility` 支持 `private`、`public`，SDK 为兼容既有调用保留默认 `private`，发送时始终包含该字段。类型化研究卡响应（`return_raw_data=False`）在创建、详情和列表中均提供可选 `research_type`；未返回时为 None。


公开列表无需 API key：`Dojo(anonymous=True, online=True)` 或 `AsyncDojo(anonymous=True, online=True)`。该模式忽略显式/环境 API key，发出请求时移除 Authorization/Cookie，并在本地拒绝 public_research GET 以外的路径和写操作。默认认证模式保持原样。可选 UserId/OrgId 只能由可信服务端构造；匿名访问不需要这些 Header。


`analysis.update_market_research(research_uid, body=...)` 对应 `PUT /api/qdata/v1/analysis/research/{research_uid}`，同步/异步均返回研究卡详情。`ResearchUpdateRequest` 仅发送显式提供的字段（保留显式 null），例如 `{"visibility":"public","research_type":"daily-event"}` 不会清空 title/description/extra。该方法不追加研究结果，写请求固定 `max_retries=0`；未知响应后应按研究 ID 读取或人工处理，不重放研究结果追加。


通用研究列表 `list_market_research(scope="starred")` 查询当前调用者收藏，支持同步/异步。scope 可取 public/mine/starred；公开列表方法仍不接收 scope。排序值为 asc/desc，不含引号。
