# src/help_info.py
# -*- coding: utf-8 -*-
from DS_Split.config import get_work_dir, CONFIG

HELP_CONTENT = f"""
a
使用指南：
1. 文件操作示例：
   - 创建文件：'桌面新建日记.txt'
   - 修改文件：'添加日志到D:\\data\\log.txt'

2. 应用操作：
   - '用Excel打开报表.xlsx'
   - '启动Chrome访问deepseek.com'

3. 系统查询：
   - '查看网络配置'
   - '显示磁盘使用情况'

4. 普通问题：
   - '李白有哪些代表作'
   - '如何优化系统性能'

5. 安全控制：
   - 自动拦截危险命令
   - 执行前需二次确认

6. 其他：
   - 输入exit/quit/000退出
   - 输入help显示本帮助
   
7. 后置参数: e.g. 在桌面新建文件，写入长恨歌全文 -t 8192 or 4 -tt 360 or 2(生成文件较长，请指定较长的tokens和time)
    '-t': max，tokens,"生成的最大token数（<10时为基准值的倍数），默认{CONFIG['max_tokens']}",
    '-tt': max_timeout,"请求超时时间（<10时为基准值的倍数），默认{CONFIG['max_timeout']}s"
    '-temp': temperature,"调整生成随机性（0.1~1.0，默认{CONFIG['temperature']}）",
    '-topp': top_p,"控制生成多样性（0.1~1.0，默认{CONFIG['top_p']}）",

    查看和修改参数请到config文件
"""


def show_help() -> None:
    """显示帮助信息"""
    print(HELP_CONTENT)


def showOpeningMessage() -> None:
    print(f"\n{'=' * 30}")
    print(f"当前工作目录: {get_work_dir()}")
    print(f"安全退出符: {CONFIG['stop_symbols']}")
    print('需要参数请输入\'help\'或到config.py查看')
    print(f"{'=' * 30}\n")
