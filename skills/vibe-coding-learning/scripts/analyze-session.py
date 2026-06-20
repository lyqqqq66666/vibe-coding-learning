#!/usr/bin/env python3
"""
analyze-session.py — 分析本次编码会话的复杂度，推荐执行深度

输出（stdout）：light / standard / deep

判断维度：
1. 代码变更行数（git diff 或文件大小变化）
2. 涉及文件数量
3. 是否跨多个技术领域
4. 是否有新的复杂概念（错误处理、异步、数据库事务等）

用法：
  python3 scripts/analyze-session.py                          # 分析整个项目最近会话
  python3 scripts/analyze-session.py --project /path/to/project  # 指定项目路径
  python3 scripts/analyze-session.py --quick                   # 快速模式（只看文件数量）
  python3 scripts/analyze-session.py --files f1.py f2.py     # 指定文件列表
"""

import argparse
import os
import sys
import subprocess
import glob
from datetime import datetime, timedelta
from pathlib import Path


def get_recent_modified_files(project_dir: str, hours: int = 2) -> list[str]:
    """获取最近 N 小时内修改的 Python/JS/TS/Go 文件"""
    project_path = Path(project_dir)
    cutoff = datetime.now().timestamp() - (hours * 3600)
    recent_files = []

    extensions = ["*.py", "*.js", "*.ts", "*.go", "*.java", "*.rs", "*.cpp", "*.c", "*.html", "*.css"]

    for ext in extensions:
        for file_path in project_path.rglob(ext):
            try:
                if file_path.is_file() and file_path.stat().st_mtime > cutoff:
                    # 跳过依赖目录
                    parts = file_path.relative_to(project_path).parts
                    if any(p in parts for p in ["node_modules", ".venv", "venv", "__pycache__", "dist", "build"]):
                        continue
                    recent_files.append(str(file_path))
            except Exception:
                continue

    return recent_files


def count_lines_of_code(files: list[str]) -> int:
    """统计文件列表的总代码行数（粗略）"""
    total = 0
    for f in files:
        try:
            with open(f, "r", encoding="utf-8", errors="ignore") as fp:
                total += len(fp.readlines())
        except Exception:
            continue
    return total


def detect_complexity_markers(files: list[str]) -> dict:
    """检测代码中是否包含复杂概念关键词"""
    complexity_keywords = {
        "async": ["async", "await", "Promise", "coroutine"],
        "error_handling": ["try:", "except:", "catch", "error", "Exception"],
        "database": ["SQL", "cursor", "execute", "migration", "transaction"],
        "auth_security": ["JWT", "bcrypt", "hash", "encrypt", "decorator", "middleware"],
        "concurrency": ["thread", "lock", "queue", "celery", "redis"],
        "architecture": ["abstract", "interface", "inheritance", "composition", "pattern"],
    }

    detected = {}
    all_content = ""

    for f in files[:10]:  # 最多读 10 个文件，避免太慢
        try:
            with open(f, "r", encoding="utf-8", errors="ignore") as fp:
                content = fp.read()
                all_content += content
        except Exception:
            continue

    for category, keywords in complexity_keywords.items():
        if any(kw in all_content for kw in keywords):
            detected[category] = True

    return detected


def get_git_changed_files(project_dir: str) -> list[str]:
    """尝试用 git diff 获取本次会话变更的文件"""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
            cwd=project_dir,
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            files = [os.path.join(project_dir, f.strip()) for f in result.stdout.strip().split("\n") if f.strip()]
            return [f for f in files if os.path.exists(f)]
    except Exception:
        pass

    #  fallback：尝试 git status
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=project_dir,
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            files = []
            for line in result.stdout.strip().split("\n"):
                if line.strip():
                    f = line.strip().split(None, 1)
                    if len(f) >= 2:
                        files.append(os.path.join(project_dir, f[1]))
            return [f for f in files if os.path.exists(f)]
    except Exception:
        pass

    return []


def recommend_depth(files: list[str], project_dir: str = None) -> str:
    """
    根据文件列表推荐执行深度

    规则：
    - light：1-3 个文件，总代码 < 100 行，无复杂概念
    - standard：4-10 个文件，或总代码 100-500 行，或含 1-2 个复杂概念
    - deep：>10 个文件，或总代码 > 500 行，或含 >2 个复杂概念，或跨多个技术栈
    """
    if not files:
        return "standard"  # 没检测到文件，用标准模式

    num_files = len(files)
    total_lines = count_lines_of_code(files)
    complexity = detect_complexity_markers(files)

    # 检测是否跨多个技术栈（通过文件扩展名）
    exts = set()
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext:
            exts.add(ext)

    num_complex_markers = len(complexity)

    # 决策逻辑
    if num_files <= 2 and total_lines < 100 and num_complex_markers == 0:
        return "light"
    elif (
        num_files <= 8
        and total_lines < 500
        and num_complex_markers <= 2
        and len(exts) <= 2
    ):
        return "standard"
    else:
        return "deep"


def main():
    parser = argparse.ArgumentParser(description="分析编码会话复杂度，推荐执行深度")
    parser.add_argument("--project", default=".", help="项目根目录路径")
    parser.add_argument("--quick", action="store_true", help="快速模式（只看文件数量）")
    parser.add_argument("--files", nargs="+", help="指定文件列表（跳过自动检测）")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出详细分析结果")
    args = parser.parse_args()

    project_dir = os.path.abspath(args.project)

    # 获取文件列表
    if args.files:
        files = [f for f in args.files if os.path.exists(f)]
    else:
        # 先尝试 git，再 fallback 到最近修改文件
        files = get_git_changed_files(project_dir)
        if not files:
            files = get_recent_modified_files(project_dir, hours=3)

    if not files:
        # 没找到文件，输出 standard（保守默认）
        if args.json:
            print('{"depth": "standard", "reason": "no_files_detected", "file_count": 0}')
        else:
            print("standard")
        return

    # 推荐深度
    depth = recommend_depth(files, project_dir)

    if args.json:
        import json
        result = {
            "depth": depth,
            "file_count": len(files),
            "total_lines": count_lines_of_code(files),
            "complexity_markers": detect_complexity_markers(files),
            "files": files[:10],  # 最多列 10 个
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(depth)


if __name__ == "__main__":
    main()
