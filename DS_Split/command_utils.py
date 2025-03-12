# -*- coding: utf-8 -*-
import re
from typing import List, Tuple
from DS_Split.config import CONFIG

def is_valid_command(cmd: str) -> Tuple[bool, str]:
    """增强命令验证"""
    cmd = cmd.strip()
    if not cmd:
        return False, "空命令"
    if len(cmd) < CONFIG["min_command_length"]:
        return False, "命令过短"

    lower_cmd = cmd.lower()
    for keyword in CONFIG["dangerous_keywords"]:
        if keyword in lower_cmd:
            return False, f"危险命令: {keyword}"

    valid_prefix = any(
        lower_cmd.startswith(p.lower())
        for p in CONFIG["valid_command_prefixes"]
    )
    if not valid_prefix:
        return False, "非法命令前缀"

    return True, ""

def extract_commands(response: str) -> List[str]:
    """严格命令提取"""
    cmd_block = re.search(r'```cmd\n(.*?)\n```', response, re.DOTALL)
    if not cmd_block:
        return []

    raw_commands = [
        line.strip()
        for line in cmd_block.group(1).split('\n')
        if line.strip() and not line.startswith(('//', '#'))
    ]

    valid_commands = []
    for cmd in raw_commands:
        valid, reason = is_valid_command(cmd)
        if valid:
            valid_commands.append(cmd)
        else:
            print(f"过滤无效命令: {cmd} ({reason})")

    return valid_commands