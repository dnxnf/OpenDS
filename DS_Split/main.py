# -*- coding: utf-8 -*-
import argparse
import time
import sys
# 终端中运行显示缺少DS_Split的module，需要提取导入此包的父目录
sys.path.append('D:/py/pycharmProjects/openDeepseek')
import urllib3
from DS_Split.api_client import get_deepseek_response
from DS_Split.command_utils import extract_commands
from DS_Split.terminal import TerminalManager
from DS_Split.config import *
from DS_Split.help_info import *  # 新增导入

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)






def main() -> None:
    """主程序入口"""
    parser = argparse.ArgumentParser(
        description="智能命令行助手 v2.0",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        'input',
        nargs='?',
        help="支持指令类型：\n"
             "- 文件操作（创建/修改/删除）\n"
             "- 应用程序启动\n"
             "- 系统查询\n"
             "- 普通问题咨询"
    )
    term_mgr = TerminalManager()

    try:
        showOpeningMessage()  # 开头的提示信息

        args = parser.parse_args()
        user_input = args.input or ""

        while True:
            if not user_input:  # 当没有输入且需要执行时
                user_input = input("请输入指令（help查看帮助）: ").strip()
                # clean_input: str
                param_explanations: object
                clean_input, params, param_explanations = parse_input(user_input)
            # 安全退出功能
            if user_input.lower() in CONFIG["stop_symbols"]:
                print("\n正在安全退出...")
                break

            if user_input.lower() == 'help':
                show_help()  # 修改为调用模块化后的函数
                user_input = ""
                continue

            # 处理请求...（后续代码保持不变）
            if param_explanations:
                print("参数调整：")
                for exp in param_explanations:
                    print(f"→ {exp}")
            print("正在处理请求...")

            start_time = time.time()
            response = get_deepseek_response(clean_input, params)
            elapsed = time.time() - start_time

            commands = extract_commands(response)
            if commands:
                print(f"\n生成命令（耗时{elapsed:.1f}s）:")
                for i, cmd in enumerate(commands, 1):
                    print(f"{i:>2}. {cmd}")

                confirm = input("\n是否执行命令？(y/n): ").lower()
                if confirm in ('y', 'yes', 'Y', 1):
                    term_mgr.execute_commands(commands)
                    print("命令已发送到终端,请勿修改正在执行的文件。")
            else:
                print(f"\n系统回复（耗时{elapsed:.1f}s）:")
                print(response)

            user_input = ""

    except KeyboardInterrupt:
        print("\n操作已中断")
    finally:
        term_mgr.safe_exit()


if __name__ == "__main__":
    main()
