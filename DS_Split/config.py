# -*- coding: utf-8 -*-
import os
import textwrap
from typing import Dict, Any, Tuple, List
import re
from DS_Split.utils import format_number

API_URL = ""
API_KEY = ""
API_NAME = "DeepSeek-V3"

CONFIG: Dict[str, Any] = {
    "api_url": API_URL,
    "api_key": API_KEY,
    "api_name": API_NAME,
    "stop_symbols": {'quit', 'exit', '000'},
    "max_tokens": 2048,  # 基准token数
    "max_timeout": 180,  # 基准超时（秒）
    # "max_max_tokens": 20487,   # 最大允许token数
    # "max_max_timeout": 1815,        # 最大允许超时
    "temperature": 0.3,
    "top_p": 0.95,
    "cmd_init_delay": 1.5,
    "command_interval": 0.3,
    "min_command_length": 1,
    "valid_command_prefixes": (
        'echo', 'start', 'copy', 'del', 'mkdir',
        'cd', 'curl', 'type', 'move', 'ren', 'notepad'
    ),
    "dangerous_keywords": (
        'format', 'rmdir /s', 'delregedit',
        'shutdown', 'chkdsk', '*.*'
        # 'taskkill'
    ),

    "max_retries": 3,
    "stream": False
}

SYSTEM_PROMPT = textwrap.dedent(
    "你是一个智能助手，请根据需求选择响应方式：\n"
        "【需要系统操作时】\n"
        "1. 生成Windows CMD命令，用```cmd包裹\n"
        "2. 使用%USERPROFILE%之类的环境变量来替代具体的用户路径，处理空格用双引号\n"
        "3. 示例：\n"
        "用户：创建诗歌文件\n -> 响应：```cmd\necho 静夜思 > poem.txt\necho 床前明月光， >> poem.txt\n```\n\n"
        "用户：当前目录是什么 → 响应：```cmd\necho %cd%\n```\n" 
        "用户：有哪些文件 → 响应：```cmd\ndir\n```"
        "注意，请确保生成的命令可以在终端中直接执行！！"
        "【普通问题时】\n"
        "1. 直接自然语言回答\n"
        "2. 示例：\n"
        "用户：李白有多少首诗\n, -> 响应：李白现存诗歌约1010首。"
        "【不确定需不需要系统操作时】"
        "1.自然语言给出建议，并给出可能需要的cmd命令\n"
        "2. 示例：\n"
        "用户：我想看电影\n, -> 响应：先用自然语言给出看电影的建议（如推荐用户合适的电影，以及不同的看电影方式）"
    "，然后给出对应的cmd命令，如打开浏览器跳转到电影网站，并询问是否执行。"

).strip()

def parse_input(raw_input: str) -> tuple[str, dict[str, int | float | Any], list[str]]:
    """
    解析带参数的指令
    返回：(原始指令, 参数字典)
    :rtype: object
    """
    # 参数模式匹配
    base_config = {
        "max_tokens": CONFIG.get("max_tokens"),
        "timeout": CONFIG.get("max_timeout")
    }
    arg_pattern = r"(-\w+)\s+(\d+\.?\d*)"
    matches = re.findall(arg_pattern, raw_input)

    # 提取参数
    params = {}
    explanations = []

    for key, value in matches:
        key = key.lstrip('-').lower()
        try:
            num_value = float(value)
            is_int = num_value.is_integer()
            num_value = int(num_value) if is_int else num_value
        except ValueError:
            continue
        explanation = ""

        # 参数类型转换
        if key in ['t', 'token', 'tokens', 'max_tokens']:
            base = base_config["max_tokens"]
            if num_value <= 10:
                final = base * num_value
                explanation = f"max_tokens = {base} × {num_value} = {int(final)}"
            else:
                final = num_value
                explanation = f"max_tokens = {int(final)} (绝对值)"
            params["max_tokens"] = final

        elif key in ['tt', 'time', 'times', 'timeout' ]:
            base = base_config["timeout"]
            if num_value <= 10:
                final = base * num_value
                explanation = f"timeout = {base} × {num_value} = {final:.1f}秒"
            else:
                final = num_value
                explanation = f"timeout = {final:.1f}秒 (绝对值)"
            params["max_timeout"] = final

        elif key in ['c', 'temp', 'temperature']:
            params['temperature'] = float(value)
            explanations.append(f"temperature = {format_number(num_value)}")
        elif key in ['p', 'topp']:
            params['top_p'] = float(value)
            explanations.append(f"temperature = {format_number(num_value)}")
        if explanation:
            explanations.append(explanation)

    # 移除参数后的原始指令
    clean_input = re.sub(arg_pattern, '', raw_input).strip()
    return clean_input, params, explanations


def get_work_dir() -> str:
    """获取当前工作目录"""
    return os.getcwd()
