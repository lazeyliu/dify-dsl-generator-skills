# 验证报告 Schema

`run_validation_suite.py --json-out` 输出的 JSON 报告使用下面这组顶层字段。

## 顶层字段

- `schema_version`
  报告 schema 版本，当前为 `1.0`。
- `generated_at_utc`
  报告生成时间，ISO 8601 UTC 字符串。
- `repo_root`
  仓库根目录绝对路径。
- `cases_roots`
  本轮参与扫描的 case 根目录数组。
- `case_count`
  本轮纳入报告的 case 数。
- `skip_replay`
  是否跳过 replay 断言。
- `cases`
  每个 case 的摘要数组。
- `entry_skill_coverage`
  入口 skill -> 命中的 case 名列表。
- `route_coverage`
  底座 skill -> 命中的 case 名列表。
- `structure_errors`
  case 结构校验错误数组。
- `lint_errors`
  case lint 期望不一致错误数组。
- `replay_errors`
  replay 断言错误数组。
- `missing_routes`
  当前仍未被任何 case 覆盖的底座 skill 数组。
- `missing_entry_skills`
  当前仍未被任何 case 覆盖的入口 skill 数组。
- `structure_ok`
  本轮 case 结构校验是否全部通过。
- `lint_ok`
  本轮 deterministic lint 校验是否全部通过。
- `replay_ok`
  本轮 replay 断言是否全部通过。
- `suite_ok`
  整体套件是否通过。

## case 摘要字段

每个 `cases[*]` 对象至少包含：

- `case_dir`
- `goal`
- `entry_skill`
- `expected_routes`
- `target`
- `structure_ok`
- `lint_status`
- `lint_error_count`
- `lint_warning_count`
- `replay_status`

其中 `replay_status` 取值：

- `passed`
- `failed`
- `skipped`

其中 `lint_status` 取值：

- `clean`
- `issues`
- `skipped`

## 对比脚本

对比两次报告：

```bash
python3 skills/dify-dsl-forward-testing/scripts/compare_validation_reports.py old.json new.json
```

输出 JSON diff：

```bash
python3 skills/dify-dsl-forward-testing/scripts/compare_validation_reports.py old.json new.json --json-out diff.json
```
