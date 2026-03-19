#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd -P)"
skills_root="${repo_root}/skills"
agents_root="${HOME}/.agents/skills"
codex_root="${HOME}/.codex/skills"
bundle_link="${agents_root}/dify-dsl"

canonical_path() {
  python3 - "$1" <<'PY'
import os
import sys

print(os.path.realpath(sys.argv[1]))
PY
}

mkdir -p "${agents_root}" "${codex_root}"

while IFS= read -r skill_name; do
  flat_link="${codex_root}/${skill_name}"
  expected_target="${skills_root}/${skill_name}"

  if [[ -L "${flat_link}" ]]; then
    resolved_target="$(canonical_path "${flat_link}")"
    resolved_expected="$(canonical_path "${expected_target}")"
    if [[ "${resolved_target}" == "${resolved_expected}" ]]; then
      rm "${flat_link}"
      printf '已移除散装链接: %s\n' "${flat_link}"
    fi
  fi
done < <(find "${skills_root}" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort)

if [[ -L "${bundle_link}" ]]; then
  current_target="$(readlink "${bundle_link}")"
  resolved_bundle_target="$(canonical_path "${bundle_link}")"
  resolved_skills_root="$(canonical_path "${skills_root}")"
  if [[ "${resolved_bundle_target}" == "${resolved_skills_root}" ]]; then
    printf 'bundle 链接已存在: %s -> %s\n' "${bundle_link}" "${current_target}"
  else
    printf '错误: 目标已存在且指向其他位置: %s -> %s\n' "${bundle_link}" "${current_target}" >&2
    exit 1
  fi
elif [[ -e "${bundle_link}" ]]; then
  printf '错误: 目标已存在且不是符号链接: %s\n' "${bundle_link}" >&2
  exit 1
else
  ln -s "${skills_root}" "${bundle_link}"
  printf '已创建 bundle 链接: %s -> %s\n' "${bundle_link}" "${skills_root}"
fi

printf '\n当前 bundle 可见 skill:\n'
find -L "${bundle_link}" -maxdepth 2 -name SKILL.md | sort
