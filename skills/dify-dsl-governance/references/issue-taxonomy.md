# 问题编码

用于给常见问题一个稳定 code，方便复盘、聚合和回归跟踪。

## 命名规则

- 用小写字母、数字和下划线
- 优先写问题类型，不写业务对象
- 同一类问题优先复用已有 code，不要反复发明近义词

## 推荐起始集合

| code | 含义 |
| --- | --- |
| `selector_drift` | selector 漂移或悬空 |
| `contract_drift` | 输入输出约定漂移 |
| `state_leak` | 状态污染或跨轮泄露 |
| `fallback_gap` | fallback 缺口 |
| `evidence_missing` | 关键证据缺失 |
| `evidence_conflict` | 关键证据冲突 |
| `idempotency_risk` | 幂等性风险 |
| `budget_overrun` | 成本或时延预算风险 |
| `schema_gap` | 关键中间对象 schema 不清 |
| `exposure_risk` | 最小暴露失败 |
| `gate_blocked` | 上线前检查阻塞 |

## 最小输出

| code | 严重度 | 位置 | 影响 | 说明 |
| --- | --- | --- | --- | --- |
|  | 阻塞项 / 高风险项 / 中风险项 / 优化项 |  |  |  |

## 规则

- 每条重要问题优先带 code。
- 同一个问题不要在同一报告里使用多个 code。
- 如果现有集合不够，再新增；新增时保持泛化，不要写行业名。
