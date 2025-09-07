# DailyNewsDigest

DailyNewsDigest 是一个旨在从 Hacker News 获取每日新闻摘要的 Python 项目。它自动化了新闻故事、评论和原始文章内容的获取、处理和发布。

## 高层架构

项目包含以下主要组件：

1.  **数据采集层 (Data Acquisition Layer)**：
    负责从 Hacker News 获取热门新闻故事及其相关评论，并从外部 URL 抓取原始文章内容。
    -   `data_acquisition/hackernews.py`: 从 Hacker News API 获取数据。
    -   `data_acquisition/web_scraper.py`: 从文章 URL 提取内容。

2.  **数据处理层 (Data Processing Layer)**：
    此层负责从抓取的文章中提取相关内容，并利用 AI 能力对新闻内容和评论进行摘要。
    -   `data_processing/llm_summarizer.py`: 使用 LLM 对内容进行摘要。

3.  **数据输出层 (Data Output Layer)**：
    管理处理后的数据格式化，将其导出到 Notion 表格，并将格式化的内容推送到各种媒体渠道。
    -   `data_output/notion_publisher.py`: 将摘要发布到 Notion 数据库。

4.  **通知层 (Notification Layer)**：
    旨在通过电子邮件或其他开发者中心化的通信渠道提供执行结果的反馈。
    -   `notification/telegram_notifier.py`: 通过 Telegram 发送通知。

## 安装

1.  克隆仓库：
    `git clone https://github.com/your-username/DailyNewsDigest.git`
    `cd DailyNewsDigest`

2.  安装依赖：
    `pip install -r requirements.txt`

    项目依赖包括：
    -   `pydantic`
    -   `pydantic-settings`
    -   `python-dotenv`
    -   `aiohttp`
    -   `beautifulsoup4`
    -   `trafilatura`
    -   `openai`
    -   `notion-client`
    -   `python-telegram-bot`
    -   `pytest`
    -   `flake8`

## 使用方法

配置必要的环境变量（例如 Notion API 密钥、数据库 ID、Telegram Bot Token 和 Chat ID 等）。一个 `.env.template` 文件可作为参考。

运行主应用程序：
`python main.py`

## 常见开发任务

-   **运行 Python 脚本**：`python your_script_name.py`
-   **安装依赖**：`pip install -r requirements.txt`
-   **代码 Linting**：`flake8 .`
-   **运行测试**：`pytest`