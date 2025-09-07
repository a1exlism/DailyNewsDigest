# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## High-Level Architecture

This project aims to create a daily news digest from Hacker News, involving the following main components:

1.  **Data Acquisition Layer**: Responsible for fetching top news stories from Hacker News and their associated comments, as well as the original article content from external URLs.
2.  **Data Processing Layer**: This layer will handle the extraction of relevant content from fetched articles, summarizing both news content and comments using AI capabilities.
3.  **Data Output Layer**: Manages the formatting of processed data, exporting it to Notion tables, and pushing the formatted content to various media channels.
4.  **Notification Layer**: Designed to provide feedback on execution results, likely through email or other developer-centric communication channels.

## Common Development Tasks

Since this is a new project, common commands will evolve. Initially, these might include:

- **Run a Python script**: `python your_script_name.py`
- **Install dependencies**: `pip install -r requirements.txt` (once a `requirements.txt` is created)
- **Linting**: Tools like `flake8` or `black` may be integrated. Example: `flake8 .`
- **Testing**: A testing framework like `pytest` is likely to be used. Example: `pytest` or `pytest path/to/your_test.py`

## Claude Code 行为规范

- **语言**: 始终以中文（简体）回应。
- **敏感信息**: 不允许读取 `.env` 等敏感字段。
- **日志**: 对所有关键逻辑/业务代码提供 INFO 或 DEBUG 日志。
- **Prompts 配置**: 在 `config/prompts.py` 中，所有外部输入均应通过 `content` 变量处理。
- **文档记录**:
  - **TODO.md**: 记录待办事项，格式为 Markdown 待办事项列表。每次通过 `TodoWrite` 工具添加或调整任务时，应相应地在此文件进行记录。
  - **CHANGELOG.md**: 记录项目更新和变更，格式为分类列表。每次重要的任务完成或功能更新后，应在此文件 CHANGELOG 下进行记录。
