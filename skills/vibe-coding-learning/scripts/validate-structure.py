#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate-structure.py — vibe-coding-learning 学习笔记目录结构校验脚本

功能：
 1. 检查 learning-notes/ 三层架构是否完整
 2. 检查每个 topic 笔记的 YAML frontmatter 是否有 domain 字段，且对应 domain index 存在
 3. 检查 progress.md 和 calendar 是否与 topics 一致
 4. 检查所有 md 文件是否有合法 YAML frontmatter（M1 创建的笔记）
 5. 输出修复建议

用法：
  python3 scripts/validate-structure.py [learning-notes路径]
  python3 scripts/validate-structure.py  # 默认检查 ./learning-notes/
  python3 scripts/validate-structure.py --fix  # 尝试自动修复（实验性）
"""

import os
import sys
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

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


# ── YAML Frontmatter 解析 ─────────────────────────────────────────

def parse_frontmatter(content: str) -> Optional[dict]:
    """
    解析 Markdown 文件的 YAML frontmatter。
    格式：
    ---
    title: "..."
    domain: backend
    ---
    """
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None

    fm_text = match.group(1)
    result = {}
    for line in fm_text.split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            # 去掉引号
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            result[key] = value
    return result


def check_file_has_frontmatter(md_file: Path) -> tuple[bool, Optional[dict]]:
    """
    检查文件是否有 YAML frontmatter。
    返回：(是否有 frontmatter, 解析出的字段字典)
    """
    try:
        content = md_file.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        return (fm is not None, fm)
    except Exception:
        return (False, None)


# ── 校验逻辑 ─────────────────────────────────────────────────────

def check_three_layer(notes_dir: Path) -> list[str]:
    """检查三层架构目录是否存在"""
    issues = []
    required_dirs = ["topics", "domains", "cards"]
    for d in required_dirs:
        p = notes_dir / d
        if not p.exists():
            issues.append(f"缺少目录：learning-notes/{d}/")
    return issues


def check_frontmatter_exists(notes_dir: Path) -> list[str]:
    """
    检查 topics/ 下所有 md 文件是否有 YAML frontmatter。
    M1 创建的笔记必须有 frontmatter。
    """
    issues = []
    topics_dir = notes_dir / "topics"
    if not topics_dir.exists():
        return issues

    for md_file in topics_dir.rglob("*.md"):
        if md_file.name.startswith("_"):
            continue
        has_fm, fm_dict = check_file_has_frontmatter(md_file)
        if not has_fm:
            rel_path = md_file.relative_to(notes_dir)
            issues.append(f"缺少 YAML frontmatter：{rel_path}")
        else:
            # 检查必需字段
            required_fields = ["title", "date", "domain", "status"]
            for field in required_fields:
                if field not in fm_dict:
                    rel_path = md_file.relative_to(notes_dir)
                    issues.append(f"frontmatter 缺少 `{field}` 字段：{rel_path}")

    return issues


def check_domain_index_exists(notes_dir: Path) -> list[str]:
    """
    检查每个 topic 笔记的 domain 字段是否有对应的 domain index 文件。
    这是 Claude 反馈的短板：之前只检查目录存在，不解析 md 内容。
    """
    issues = []
    topics_dir = notes_dir / "topics"
    domains_dir = notes_dir / "domains"

    if not topics_dir.exists() or not domains_dir.exists():
        return issues

    for md_file in topics_dir.rglob("*.md"):
        if md_file.name.startswith("_"):
            continue

        has_fm, fm_dict = check_file_has_frontmatter(md_file)
        if not has_fm or "domain" not in fm_dict:
            continue

        domain = fm_dict["domain"].strip()
        if not domain:
            continue

        # 检查 domains/[domain]/_index.md 是否存在
        domain_index = domains_dir / domain / "_index.md"
        if not domain_index.exists():
            rel_path = md_file.relative_to(notes_dir)
            issues.append(
                f"domain index 不存在：domains/{domain}/_index.md "
                f"（引用自 {rel_path}）"
            )

    return issues


def check_status_field(notes_dir: Path) -> list[str]:
    """
    检查 M1 创建的笔记 status 字段是否为 processed（而非 inbox）。
    如果 status 为 inbox，说明 M1 Step 8 未正确设置。
    """
    issues = []
    topics_dir = notes_dir / "topics"
    if not topics_dir.exists():
        return issues

    for md_file in topics_dir.rglob("*.md"):
        if md_file.name.startswith("_"):
            continue

        has_fm, fm_dict = check_file_has_frontmatter(md_file)
        if not has_fm:
            continue

        status = fm_dict.get("status", "").strip()
        if status == "inbox":
            rel_path = md_file.relative_to(notes_dir)
            issues.append(
                f"笔记状态为 inbox（应为 processed）：{rel_path}"
                f"  → 建议运行 M1 重新保存"
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

    # 统计 topics 数量（有 frontmatter 的）
    topic_count = 0
    for md_file in topics_dir.rglob("*.md"):
        if md_file.name.startswith("_"):
            continue
        has_fm, _ = check_file_has_frontmatter(md_file)
        if has_fm:
            topic_count += 1

    # 读取 progress.md 里的知识点数量（简单正则）
    content = progress_file.read_text(encoding="utf-8")
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


def check_review_fields(notes_dir: Path) -> list[str]:
    """
    检查笔记的 last_review_date 和 review_count 字段是否合理。
    Claude 反馈：last_review_date 字段没有写入流程。
    """
    issues = []
    topics_dir = notes_dir / "topics"
    if not topics_dir.exists():
        return issues

    for md_file in topics_dir.rglob("*.md"):
        if md_file.name.startswith("_"):
            continue

        has_fm, fm_dict = check_file_has_frontmatter(md_file)
        if not has_fm:
            continue

        # 检查 last_review_date 格式（如果有值）
        last_review = fm_dict.get("last_review_date", "").strip()
        if last_review and last_review != "null":
            # 简单检查是否是 YYYY-MM-DD 格式
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", last_review):
                rel_path = md_file.relative_to(notes_dir)
                issues.append(
                    f"last_review_date 格式错误：{rel_path}（应为 YYYY-MM-DD）"
                )

        # 检查 review_count 是否为数字
        review_count = fm_dict.get("review_count", "0").strip()
        try:
            int(review_count)
        except ValueError:
            rel_path = md_file.relative_to(notes_dir)
            issues.append(f"review_count 应为数字：{rel_path}")

    return issues


# ── 主流程 ────────────────────────────────────────────────────────────
def main():
    log_section("vibe-coding-learning 目录结构校验")

    # 确定 notes_dir
    fix_mode = "--fix" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    if args:
        notes_dir = Path(args[0]).resolve()
    else:
        # 默认在当前目录找 learning-notes/
        notes_dir = Path.cwd() / "learning-notes"

    if not notes_dir.exists():
        log_error(f"目录不存在：{notes_dir}")
        log_info("用法：python3 validate-structure.py [learning-notes路径] [--fix]")
        sys.exit(1)

    log_info(f"检查目录：{notes_dir}")
    print()

    all_issues = []

    # 检查 1：三层架构
    log_info("检查 1/7：三层架构目录...")
    issues = check_three_layer(notes_dir)
    if issues:
        for i in issues:
            log_warn(i)
        all_issues.extend(issues)
    else:
        log_success("三层架构目录完整")

    # 检查 2：YAML frontmatter 存在性（新增 — 解决 Claude 反馈）
    log_info("检查 2/7：YAML frontmatter 存在性...")
    issues = check_frontmatter_exists(notes_dir)
    if issues:
        for i in issues:
            log_warn(i)
        all_issues.extend(issues)
    else:
        log_success("所有笔记均有 YAML frontmatter")

    # 检查 3：domain index 存在性（升级 — 解析 md 内容）
    log_info("检查 3/7：domain index 与 frontmatter 一致性...")
    issues = check_domain_index_exists(notes_dir)
    if issues:
        for i in issues:
            log_warn(i)
        all_issues.extend(issues)
    else:
        log_success("domain index 与 frontmatter 一致")

    # 检查 4：status 字段合理性（新增 — 解决状态机闭环问题）
    log_info("检查 4/7：笔记 status 字段...")
    issues = check_status_field(notes_dir)
    if issues:
        for i in issues:
            log_warn(i)
        all_issues.extend(issues)
    else:
        log_success("笔记 status 字段正常（无 inbox 残留）")

    # 检查 5：review 字段格式（新增 — 解决 last_review_date 问题）
    log_info("检查 5/7：review 字段格式...")
    issues = check_review_fields(notes_dir)
    if issues:
        for i in issues:
            log_warn(i)
        all_issues.extend(issues)
    else:
        log_success("review 字段格式正常")

    # 检查 6：progress.md 一致性
    log_info("检查 6/7：progress.md 一致性...")
    issues = check_progress_consistency(notes_dir)
    if issues:
        for i in issues:
            log_warn(i)
        all_issues.extend(issues)
    else:
        log_success("progress.md 与 topics 数量一致")

    # 检查 7：calendar 和 cards
    log_info("检查 7/7：学习日历和知识卡片...")
    issues = check_calendar_exists(notes_dir)
    issues += check_cards_have_content(notes_dir)
    if issues:
        for i in issues:
            log_warn(i)
        all_issues.extend(issues)
    else:
        log_success("学习日历和知识卡片完整")

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
        log_info("  1. 运行 Skill Mode 1 重新生成笔记（会自动更新各层和 frontmatter）")
        log_info("  2. 手动检查 learning-notes/ 目录")
        log_info("  3. 如问题持续，在 AI 对话中说'检查我的学习笔记目录结构'")
        print()
        sys.exit(1)


if __name__ == "__main__":
    main()
