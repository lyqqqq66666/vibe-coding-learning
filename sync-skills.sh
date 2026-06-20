#!/usr/bin/env bash
# =============================================================================
# sync-skills.sh — vibe-coding-learning Skill 同步脚本
#
# 功能：将项目 skills/vibe-coding-learning/ 同步到各 AI 工具的全局目录
#
# 用法：
#   bash sync-skills.sh                  # 同步到所有 enabled 的目标
#   bash sync-skills.sh --target=trae   # 只同步到 Trae
#   bash sync-skills.sh --target=all    # 显式同步所有目标
#   bash sync-skills.sh --dry-run       # 预览但不实际复制
#   bash sync-skills.sh --config=./custom-config.json
#
# Git Hook 触发：
#   .githooks/post-push  → git push 后自动调用
#   .githooks/post-merge → git merge 后自动调用
# =============================================================================

set -uo pipefail

# ── 路径解析 ──────────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_SOURCE="${SCRIPT_DIR}/skills/vibe-coding-learning"
CONFIG_FILE="${SCRIPT_DIR}/sync-config.json"

# ── 颜色输出 ──────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info()    { echo -e "${BLUE}[INFO]${NC}  $1"; }
log_success() { echo -e "${GREEN}[OK]${NC}    $1"; }
log_warn()    { echo -e "${YELLOW}[WARN]${NC}  $1"; }
log_error()   { echo -e "${RED}[ERROR]${NC} $1"; }

# ── 默认值 ─────────────────────────────────────────────────────────────────────
DRY_RUN=false
TARGET_FILTER=""
CUSTOM_CONFIG=""

# ── 参数解析 ──────────────────────────────────────────────────────────────────
for arg in "$@"; do
  case $arg in
    --target=*)
      TARGET_FILTER="${arg#*=}"
      ;;
    --dry-run)
      DRY_RUN=true
      ;;
    --config=*)
      CUSTOM_CONFIG="${arg#*=}"
      CONFIG_FILE="$CUSTOM_CONFIG"
      ;;
    --help|-h)
      head -12 "$0" | tail -11
      exit 0
      ;;
    *)
      log_error "未知参数: $arg"
      exit 1
      ;;
  esac
done

# ── 检查源目录 ────────────────────────────────────────────────────────────────
if [ ! -d "$SKILL_SOURCE" ]; then
  log_error "Skill 源目录不存在: $SKILL_SOURCE"
  log_error "请确认当前位于项目根目录，且 skills/vibe-coding-learning/ 存在。"
  exit 1
fi

if [ ! -f "$SKILL_SOURCE/SKILL.md" ]; then
  log_error "Skill 源目录缺少 SKILL.md: $SKILL_SOURCE/SKILL.md"
  exit 1
fi

# ── 读取配置 ─────────────────────────────────────────────────────────────────
if [ ! -f "$CONFIG_FILE" ]; then
  log_error "配置文件不存在: $CONFIG_FILE"
  log_error "请先创建 sync-config.json"
  exit 1
fi

log_info "读取配置: $CONFIG_FILE"
log_info "Skill 源:  $SKILL_SOURCE"
echo ""

# ── 用 python 解析 json（写临时脚本避免 here-doc 参数传递问题）────────────
TMP_PY=$(mktemp /tmp/sync-parse-XXXXXX.py)
trap "rm -f $TMP_PY" EXIT

cat > "$TMP_PY" << 'PYEOF'
import json, sys, os

config_path = sys.argv[1]
target_filter = sys.argv[2]

with open(config_path, "r") as f:
    config = json.load(f)

skill_name = config.get("skill_name", "vibe-coding-learning")
targets = config.get("targets", {})

for name, info in targets.items():
    if target_filter and target_filter not in (name, "all"):
        continue
    if not info.get("enabled", True):
        continue
    path = info.get("path", "")
    path = os.path.expanduser(path)
    print(f"{name}|{path}|{skill_name}")
PYEOF

TARGETS_DATA=$(python3 "$TMP_PY" "$CONFIG_FILE" "$TARGET_FILTER")

if [ -z "$TARGETS_DATA" ]; then
  log_warn "没有匹配的目标（target_filter=$TARGET_FILTER，或所有目标均已禁用）"
  exit 0
fi

# ── 执行同步 ──────────────────────────────────────────────────────────────────
SYNC_COUNT=0
SKIP_COUNT=0

while IFS='|' read -r TARGET_NAME TARGET_PATH SKILL_NAME; do

  DEST="${TARGET_PATH}/${SKILL_NAME}"

  # 检查目标目录的父目录是否存在
  PARENT_DIR="$(dirname "$DEST")"
  if [ ! -d "$PARENT_DIR" ]; then
    log_warn "$TARGET_NAME: 父目录不存在，跳过: $PARENT_DIR"
    log_warn "  提示：如果已安装该 AI 工具，请检查 sync-config.json 中的路径是否正确。"
    SKIP_COUNT=$((SKIP_COUNT + 1))
    continue
  fi

  # dry-run 模式
  if [ "$DRY_RUN" = true ]; then
    log_info "[dry-run] $TARGET_NAME: $SKILL_SOURCE → $DEST"
    continue
  fi

  # 执行同步（用 rsync 如果可用，否则用 cp）
  mkdir -p "$DEST"
  if command -v rsync &>/dev/null; then
    rsync -a --delete "$SKILL_SOURCE/" "$DEST/"
  else
    # 删除目标中源已删除的文件
    rm -rf "${DEST:?}/"*
    cp -r "$SKILL_SOURCE/"* "$DEST/"
  fi

  if [ $? -eq 0 ]; then
    log_success "$TARGET_NAME: 已同步到 $DEST"
    SYNC_COUNT=$((SYNC_COUNT + 1))
  else
    log_error "$TARGET_NAME: 同步失败: $DEST"
  fi

done <<< "$TARGETS_DATA"

echo ""
log_info "同步完成: ${GREEN}${SYNC_COUNT}${NC} 个成功, ${YELLOW}${SKIP_COUNT}${NC} 个跳过"

if [ "$DRY_RUN" = true ]; then
  echo ""
  log_info "这是 dry-run 预览，未实际复制文件。去掉 --dry-run 参数后执行真实同步。"
fi

exit 0
