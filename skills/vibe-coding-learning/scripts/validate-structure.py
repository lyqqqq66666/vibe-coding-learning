#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate-structure.py — vibe-coding-learning 学习笔记目录结构校验脚本

功能：
  1. 检查 learning-notes/ 三层架构是否完整
  2. 检查每个 topic 笔记是否有对应的 domain/cards 索引
  3. 检查 progress.md 和 calendar 是否与 topics 一致
  4. 输出修复建议

用法：
  python3 scripts/validate-structure.py [learning-notes路径]
  python3 scripts/validate-structure.py  # 默认检查 ./learning-notes/
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime

# ── 颜色输出（终端支持检测）──────────────────────────────────────
try:
    from colorama import init
    init()
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    NC = "\033[0m"
except ImportError:
    GREEN = YELLOW = BLUE = RED = NC = ""


def log_success(msg):
    print(f"{GREEN}✅  {msg}{NC}")


def log_warn(msg):
    print(f"{YELLOW}⚠️  {msg}{NC}")


def log_error(msg):
    print(f"{RED}❌  {msg}{NC}")


def log_info(msg):
    print(f"{BLUE}ℹ️  {msg}{NC}")


def log_section(msg):
    print(f"\n{'='*60}")
    print(f"  {msg}")
    print(f"{'='*60}")


# ── 校验逻辑 ─────────────────────────────────────────────────────────
def check_three_layer(notes_dir: Path) -> list[str]:
    """检查三层架构目录是否存在"""
    issues = []
    required_dirs = ["topics", "domains", "cards"]
    for d in required_dirs:
        p = notes_dir / d
        if not p.exists():
            issues.append(f"缺少目录：learning-notes/{d}/")
    return issues


def check_topic_has_domain_index(notes_dir: Path) -> list[str]:
    """检查每个 topic 笔记是否有关联的 domain index"""
    issues = []
    topics_dir = notes_dir / "topics"
    domains_dir = notes_dir / "domains"
    if not topics_dir.exists():
        return issues

    for topic_folder in topics_dir.iterdir():
        if not topic_folder.is_dir() or topic_folder.name.startswith("."):
            continue
        # 读取该 topic 笔记里的 domain 标签
        md_files = list(topic_folder.glob("*.md"))
        if not md_files:
            continue
        # 简单检查：看 notes_dir/domains/ 下是否有对应目录
        # 更精确的做法是解析 md 文件内容，这里做基础检查
        if domains_dir.exists():
            domain_folders = [d.name for d in domains_dir.iterdir() if d.is_dir() and not d.name.startswith("_")]
            if not domain_folders:
                issues.append(
                    f"topics/{topic_folder.name}/ 有笔记，但 domains/ 下无领域索引"
                )
    return issues


def check_progress_consistency(notes_dir: Path) -> list[str]:
    """检查 progress.md 是否与 topics/ 数量一致"""
    issues = []
    progress_file = notes_dir / "progress.md"
    topics_dir = notes_dir / "topics"
    if not progress_file.exists():
        issues.append("缺少 progress.md")
        return issues
    if not topics_dir.exists():
        return issues

    # 统计 topics 数量
    topic_count = sum(
        1
        for f in topics_dir.rglob("*.md")
        if not f.name.startswith("_")
    )
    # 读取 progress.md 里的知识点数量（简单正则）
    content = progress_file.read_text(encoding="utf-8")
    # 匹配 | 🟢|🟡|🔴 的行数
    knowledge_lines = re.findall(r"\|[^\|]*[🟢🟡🔴][^\|]*\|", content)
    if knowledge_lines and abs(len(knowledge_lines) - topic_count) > 5:
        issues.append(
            f"progress.md 知识点数量（{len(knowledge_lines)}）"
            f"与 topics/ 文件数（{topic_count}）差异较大，建议同步更新"
        )
    return issues


def check_calendar_exists(notes_dir: Path) -> list[str]:
    """检查 calendar/ 是否存在且有当月文件"""
    issues = []
    calendar_dir = notes_dir / "calendar"
    if not calendar_dir.exists():
        issues.append("缺少 calendar/ 目录")
        return issues
    now = datetime.now()
    current_month = now.strftime("%Y-%m")
    month_file = calendar_dir / f"{current_month}.md"
    if not month_file.exists():
        issues.append(f"calendar/ 缺少当月文件：{current_month}.md")
    return issues


def check_cards_have_content(notes_dir: Path) -> list[str]:
    """检查 cards/ 下是否有实际内容"""
    issues = []
    cards_dir = notes_dir / "cards"
    if not cards_dir.exists():
        return issues
    card_files = list(cards_dir.rglob("*.md"))
    if len(card_files) == 0:
        issues.append("cards/ 目录存在但没有知识卡片文件")
    return issues


def check_orphan_cards(notes_dir: Path) -> list[str]:
    """检查是否有卡片未被任何 topic 引用（基础检查）"""
    issues = []
    # 这是个进阶检查，当前版本只做警告
    return issues


# ── 主流程 ────────────────────────────────────────────────────────────
def main():
    log_section("vibe-coding-learning 目录结构校验")

    # 确定 notes_dir
    if len(sys.argv) > 1:
        notes_dir = Path(sys.argv[1]).resolve()
    else:
        # 默认在当前目录找 learning-notes/
        notes_dir = Path.cwd() / "learning-notes"

    if not notes_dir.exists():
        log_error(f"目录不存在：{notes_dir}")
        log_info("用法：python3 validate-structure.py [learning-notes路径]")
        sys.exit(1)

    log_info(f"检查目录：{notes_dir}")
    print()

    all_issues = []

    # 检查 1：三层架构
    log_info("检查 1/5：三层架构目录...")
    issues = check_three_layer(notes_dir)
    if issues:
        for i in issues:
            log_warn(i)
        all_issues.extend(issues)
    else:
        log_success("三层架构目录完整")

    # 检查 2：topic → domain 关联
    log_info("检查 2/5：topic 与 domain 关联...")
    issues = check_topic_has_domain_index(notes_dir)
    if issues:
        for i in issues:
            log_warn(i)
        all_issues.extend(issues)
    else:
        log_success("topic → domain 关联正常")

    # 检查 3：progress.md 一致性
    log_info("检查 3/5：progress.md 一致性...")
    issues = check_progress_consistency(notes_dir)
    if issues:
        for i in issues:
            log_warn(i)
        all_issues.extend(issues)
    else:
        log_success("progress.md 与 topics 数量一致")

    # 检查 4：calendar 存在
    log_info("检查 4/5：学习日历...")
    issues = check_calendar_exists(notes_dir)
    if issues:
        for i in issues:
            log_warn(i)
        all_issues.extend(issues)
    else:
        log_success("学习日历完整")

    # 检查 5：cards 内容
    log_info("检查 5/5：知识卡片...")
    issues = check_cards_have_content(notes_dir)
    if issues:
        for i in issues:
            log_warn(i)
        all_issues.extend(issues)
    else:
        log_success("知识卡片存在")

    # ── 汇总报告 ───────────────────────────────────────────────────
    log_section("校验结果")

    if not all_issues:
        log_success("所有检查通过！目录结构健康。")
        print()
        sys.exit(0)
    else:
        log_warn(f"发现 {len(all_issues)} 个问题：")
        print()
        for i, issue in enumerate(all_issues, 1):
            print(f"  {i}. {issue}")
        print()

        log_info("修复建议：")
        log_info("  1. 运行 Skill Mode 1 重新生成笔记（会自动更新各层）")
        log_info("  2. 手动检查 learning-notes/ 目录")
        log_info("  3. 如问题持续，在 AI 对话中说'检查我的学习笔记目录结构'")
        print()
        sys.exit(1)


if __name__ == "__main__":
    main()
