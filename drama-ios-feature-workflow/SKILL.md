---
name: drama-ios-feature-workflow
description: Use when starting, clarifying, planning, approving, implementing, or handing off a new iOS business feature in drama-ios, especially for requests mentioning iOS 新需求工作流, requirement_contract, tech_plan, CONFIRM_REQUIREMENT, APPROVE_PLAN, REQUEST_CHANGES, or SKIP_BLOCKER. Enforces feature snapshots, requirement and plan approval gates, and the project document templates.
---

# drama-ios：iOS 新需求工作流

按本 Skill 推进 drama-ios 的新业务需求。完整阶段规则见 [references/ios-feature-workflow.md](references/ios-feature-workflow.md)；需求文档模板在 [assets](assets)。

## 硬性门禁

- 未通过计划审批且用户未明确回复 `APPROVE_PLAN` 前，不得修改生产代码。
- 仅在 `requirement_contract.md` 无未决事项且用户明确回复 `CONFIRM_REQUIREMENT` 后，才可将需求契约标记为“已确认”、推进技术评审并生成可推进的 `tech_plan.md`。
- 新增文案的多语言 key 未确认时，属于阻塞项；不得进入技术评审、审批或编码。
- 审批后若必须扩大影响范围或改变已审批方案，暂停编码，记录变更并重新取得用户确认后再继续。

## 工作流

### 启动

1. 由需求名生成可读的下划线风格 `<feature-id>`。
2. 若 `.huangdonghong/feature/<feature-id>/` 已存在，先读取其中的 `snapshot_index.md`、`approval.md`（如存在）和最近 checkpoint。
3. 若不存在，创建目录，并从 `assets/` 创建 `snapshot_index.md`、`intake.md`、`decision_log.md`、`requirement_contract.md`、`tech_plan.md`、`approval.md` 与 `handoff.md`。
4. 先填写 `snapshot_index.md` 与 `intake.md`；在会话中完成需求澄清。仅把稳定结论写入 `decision_log.md`。

### 需求澄清与契约

1. 以 `requirement_contract.md` 作为需求事实唯一来源；阻塞项和解除条件同时记录到 `decision_log.md`。
2. `requirement_contract.md` 草稿已创建不代表澄清完成，存在任何阻塞或待确认项时阶段保持为“需求澄清”。
3. 收到 `CONFIRM_REQUIREMENT` 时，读取契约、索引和决策日志；若仍有未决事项，拒绝推进并列出剩余项。
4. 若无未决事项，将契约标记为“已确认”，更新快照阶段与 checkpoint，并在决策日志记录确认；随后开始技术评审。

### 技术评审与审批

1. 基于已确认的契约和代码静态阅读，写出唯一选定方案到 `tech_plan.md`。不得保留未收敛结论。
2. 新增 Objective-C 或 Swift 源文件时，将 `Drama.xcodeproj/project.pbxproj` 列入影响范围，仅用于工程引用和 target membership。
3. 逐项检查 `approval.md` 门禁。任一门禁未通过时，不得提示 `APPROVE_PLAN`。
4. 门禁通过后才可请求用户回复 `APPROVE_PLAN`。收到后记录审批基准，进入编码。
5. 收到 `REQUEST_CHANGES: ...` 或 `SKIP_BLOCKER: ...` 时，按完整规则更新相关文档和决策日志，再重新评估门禁。

### 编码与交付

1. 只修改审批范围内的文件与模块，并遵循仓库的 `AGENTS.md` 和编码约定。
2. 审批后的 `tech_plan.md` 是不可反向改写的审批基准；实际实现、偏离、验证和风险写入 `handoff.md`。
3. 完成后更新 `handoff.md`，写明实际改动范围、验证结果、未验证项、已知风险和后续事项。

## 文档规则

- 历史 checkpoint 和历史功能快照只读，只追加，不重写或迁移。
- 用标题、段落和编号列表表达需求事实、范围、规则和技术结论；checkbox 仅用于状态、待确认项和验证；表格仅用于多字段状态矩阵。
- 不手动修改 `lang.json`、`Localizable.strings` 等多语言产物；仅在文档中确认建议 key、默认中英文文案和使用场景。
- `decision_log.md` 仅追加稳定决策与变更，不记录搜索结果、普通进度或文件修改流水账。

需要精确阶段定义、确认口令处理、模板字段或审批基准规则时，先读取 [references/ios-feature-workflow.md](references/ios-feature-workflow.md)。
