# -*- coding: utf-8 -*-
import textwrap
from typing import Dict

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from DS_Split.config import *

session = requests.Session()
retries = Retry(
    total=CONFIG["max_retries"],
    backoff_factor=0.5,
    status_forcelist={500, 502, 503, 504, 524},
    allowed_methods=frozenset(['POST']),
)
# 优化速度
adapter = HTTPAdapter(
    max_retries=retries,
    pool_connections=20,  # 默认10 → 20（保持的长连接数）
    pool_maxsize=100,  # 默认10 → 100（最大连接数）
    pool_block=False  # 非阻塞模式（需配合线程池使用）
)
session.mount('https://', adapter)

# 对api的提示词



def get_deepseek_response(question: str, params: Dict = None) -> str:
    """获取DeepSeek API响应"""
    headers = {
        "Authorization": f"Bearer {CONFIG['api_key']}",
        "Content-Type": "application/json",
        "User-Agent": "CLI-Assistant/2.0"
    }
    if params is None:
        params = {}

    payload = {
        "model": CONFIG['api_name'],
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ],
        "max_tokens": params.get('max_tokens', CONFIG["max_tokens"]),
        "temperature": params.get('temperature', CONFIG["temperature"]),
        "top_p": params.get('top_p', CONFIG['top_p']),
    }

    try:
        response = session.post(
            CONFIG["api_url"],
            headers=headers,
            json=payload,
            verify=False,
            timeout = params.get('max_timeout', CONFIG["max_timeout"]),
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]

        # 响应内容验证
        if 0 < len(content) < CONFIG["max_tokens"] * 3:
            return content.encode('utf-8', errors='replace').decode('utf-8')
        return "响应内容长度异常"

    except requests.exceptions.RequestException as e:
        return f"API请求失败: {str(e)}"
    except Exception:
        return "响应解析异常"
