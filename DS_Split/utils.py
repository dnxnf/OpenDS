# -*- coding: utf-8 -*-
import sys
def safe_print(text: str) -> None:
    """适配Windows控制台输出"""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("gbk", errors="replace").decode("gbk"))



def format_number(num: float) -> str:
    """统一数字显示格式"""
    if isinstance(num, int) or num.is_integer():
        return str(int(num))
    return f"{num:.1f}"

if __name__ == "__main__":
    safe_print("天气晴朗☀️ 记得防晒🧴")