# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import time
from typing import Optional, List
import win32con
from .config import CONFIG, get_work_dir


class TerminalManager:
    """CMD终端管理器"""

    def __init__(self):
        self.process: Optional[subprocess.Popen] = None

    def init_cmd(self) -> None:
        """初始化CMD窗口"""
        if self.process and self.process.poll() is None:
            return

        try:
            creation_flags = subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0

            startup_info = subprocess.STARTUPINFO()
            # note 终端隐藏标识,新注释的，原来有
            startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            # if sys.platform == "win32":
            #     startup_info.wShowWindow = subprocess.SW_SHOW  # 新增代码

            self.process = subprocess.Popen(
                ['cmd.exe' if sys.platform == 'win32' else 'bash'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                creationflags=creation_flags,
                startupinfo=startup_info if sys.platform == "win32" else None,
                cwd=get_work_dir()
            )
            time.sleep(CONFIG["cmd_init_delay"])  # 1.5秒延迟
            setup_commands = [
                '@echo off',
                'prompt [CLI]$G$_',
                'cls',
                'echo 终端已初始化'
            ]
            for cmd in setup_commands:
                self.process.stdin.write(f"{cmd}\n")
                self.process.stdin.flush()
                time.sleep(0.2)

        except Exception as e:
            print(f"CMD初始化失败: {str(e)}")
            raise

    def execute_commands(self, commands: List[str]) -> None:
        """执行命令序列"""
        if not commands:
            return

        try:
            self.init_cmd()
            self.process.stdin.write(f"echo [开始执行 {len(commands)}条命令] > con\n")

            for idx, cmd in enumerate(commands, 1):
                full_cmd = (
                    f"echo [进度 {idx}/{len(commands)}] > con && "
                    f"{cmd}"
                )
                self.process.stdin.write(full_cmd + "\n")
                self.process.stdin.flush()
                time.sleep(CONFIG["command_interval"])

            self.process.stdin.write("echo [执行完成] > con\n")

        except (BrokenPipeError, OSError) as e:
            print(f"命令发送失败: {str(e)}")
            self.process = None
        except Exception as e:
            print(f"执行错误: {str(e)}")
            self.safe_exit()

    def safe_exit(self) -> None:
        """安全退出"""
        if self.process:
            try:
                self.process.stdin.write("exit\n")
                self.process.stdin.flush()
                time.sleep(1)
                if self.process.poll() is None:
                    self.process.terminate()
                    self.process.wait(2)
            except Exception:
                pass
            finally:
                self.process = None
