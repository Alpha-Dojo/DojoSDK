# DojoSDK 项目开发指南 (Agent Instructions)

这个文档记录了 DojoSDK 项目的整体代码结构、核心设计理念以及必须严格遵守的开发规范。作为辅助开发的 Agent，你在处理任何相关的需求和代码修改时，**必须优先阅读并遵循**本文件中的所有规则。

## 1. 项目代码结构 (Project Structure)
项目的主要代码位于 `dojo/` 目录下：
*   **`dojo/client/`**: 客户端核心模块。
    *   `base.py`: 底层 HTTP 请求逻辑、错误封装和重试机制。
    *   `sync.py`: 同步客户端 `Dojo`。
    *   `async_client.py`: 异步客户端 `AsyncDojo`。
*   **`dojo/datasource/`**: 数据源抽象层。
    *   支持在线通过 HTTP API 获取数据（如 `api.py`）。
    *   支持离线拉取数据：通过 HuggingFace 或 ModelScope 下载本地离线文件并解析 (Parquet 格式)，主要逻辑在 `huggingface.py` 及相关模块中。
*   **`dojo/resources/`**: 业务逻辑模块。每个文件对应一类 API 端点 (如 `stocks.py`, `forex.py`, `macro.py` 等)，负责具体接口的路径定义、参数拼装和调用。
*   **`dojo/types/`**: 数据类型定义。所有 API 接口的入参和出参必须在这里使用 `Pydantic` 进行严格类型校验与序列化定义。

## 2. 核心设计理念 (Core Design)
*   **多数据源架构**: 接口拉取数据不直接硬编码 HTTP 请求，而是通过统一的 `DataSource` 协议 (`fetch` 和 `fetch_df` 方法)，使得 SDK 可以在线上的 API 请求和离线数据集模式之间透明、无缝地切换。
*   **同步与异步并存**: 借助 `httpx` 和 `anyio`，底层实现一份逻辑，同时对外提供一致的同步 (`Dojo`) 和异步 (`AsyncDojo`) API。
*   **类型安全**: 全面采用 `pydantic` 模型和 Python 类型提示 (Type Hinting)，保障数据传输和解析的正确性与安全性。

## 3. Agent 开发与协作规范 (Development Guidelines)
在执行开发任务时，你**绝对不能违反**以下操作规则：

### 🚫 严禁使用的命令与工具
1.  **绝对禁止使用任何 `git` 相关命令**：在这个项目中，你不能调用 `git add`、`git commit`、`git status` 等任何与 Git 版本控制相关的命令。
2.  **绝对禁止直接使用 `python` 或 `pip` 运行脚本与测试**：此项目使用 `uv` 管理依赖和环境，任何环境相关的命令或测试运行必须使用 `uv`，例如：使用 `uv run pytest` 而不是 `pytest` 或 `python -m pytest`。

### ✅ 代码编写与依赖要求
1.  **网络请求**: 所有网络请求逻辑只能使用 `httpx`。
2.  **数据类型**: 所有数据实体、请求体、响应体必须使用 `pydantic` 定义 `BaseModel`。
3.  **异步兼容**: 所有的并发逻辑应尽量借助 `anyio`，以保证最佳的异步环境兼容性（例如使用 `anyio.to_thread` 执行同步阻塞函数）。
4.  **离线数据源适配 (双端兼容)**: 当你需要修改 `dojo/datasource/huggingface.py` 及离线下载相关的逻辑时，你必须同时考虑并兼容 **HuggingFace** 和 **ModelScope** 两个平台。任何针对单平台的优化（如重试机制、缓存目录清理逻辑等）都必须适配另一个平台。

> **Reminder:** 在开始具体的代码修改前，请仔细核对本指南中的约束条件，确保没有遗漏（特别是 `uv` 的使用和 `git` 命令的禁用要求）。
