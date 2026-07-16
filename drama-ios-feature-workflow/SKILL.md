---
name: drama-ios-feature-workflow
description: Use only when the user explicitly asks to follow the drama-ios iOS 新需求工作流, or when the request mentions workflow artifacts or commands such as requirement_contract, tech_plan, CONFIRM_REQUIREMENT, APPROVE_PLAN, REQUEST_CHANGES, or SKIP_BLOCKER. Do not use for ordinary refactor advice, code review, bug fixing, read-only implementation discovery, or architecture discussion unless the user asks to enter the formal feature workflow.
---

# drama-ios：iOS 新需求工作流

按本 Skill 推进 drama-ios 的新业务需求。完整阶段规则见 [references/工作流说明.md](references/工作流说明.md)；需求文档模板在 [assets](assets)。

## 硬性门禁

- 未通过计划审批且用户未明确回复 `APPROVE_PLAN` 前，不得修改生产代码。
- 仅在 `需求契约.md` 无未决事项且用户明确回复 `CONFIRM_REQUIREMENT` 后，才可将需求契约标记为“已确认”、推进技术评审并生成可推进的 `技术方案.md`。
- 新增文案的多语言 key 未确认时，属于阻塞项；不得进入技术评审、审批或编码。
- 需求契约只确认用户可见结果、业务规则、验收标准、设计/内容约束和外部能力语义；除确认后的多语言 key 外，不得写入客户端内部类、方法、回调、模块、文件、工程接入、数据流、算法、现有资源名或精确协议/字段标识。
- 审批后若必须扩大影响范围或改变已审批方案，暂停编码，记录变更并重新取得用户确认后再继续。

## 工作流

### 启动

1. 由需求名生成可读的下划线风格 `<feature-id>`。
2. 若 `.huangdonghong/feature/<feature-id>/` 已存在，先读取其中的 `快照索引.md`、`计划审批.md`（如存在）和最近 checkpoint。若目录仅包含旧版英文文件名，按《工作流说明》的旧版映射继续读取，且不得自动重命名或迁移。
3. 若不存在，创建目录，并从 `assets/` 创建 `快照索引.md`、`需求接收.md`、`决策日志.md`、`需求契约.md`、`技术方案.md`、`计划审批.md` 与 `交付文档.md`。
4. 先填写 `快照索引.md` 与 `需求接收.md`；在会话中完成需求澄清。仅把稳定结论写入 `决策日志.md`。

### 需求澄清与契约

1. 以 `需求契约.md` 作为需求事实唯一来源；只记录业务语义，不提前选定内部实现。阻塞项和解除条件同时记录到 `决策日志.md` 的需求确认记录。
2. `需求契约.md` 草稿已创建不代表澄清完成，存在任何阻塞或待确认项时阶段保持为“需求澄清”。
3. 需求澄清阶段允许做最小静态阅读，以确认外部能力是否存在和识别业务风险；不得据此选定模块、方法、文件或数据流。
4. 收到 `CONFIRM_REQUIREMENT` 时，读取契约、索引和决策日志，先完成契约边界检查；若存在未决事项、缺少用户可见失败行为/验收/外部能力语义，或混入内部实现细节，拒绝推进并列出剩余项。内部实现细节移入技术评审处理，不要求用户通过需求确认审批实现路径。
5. 若无未决事项，将契约标记为“已确认”，更新快照阶段与 checkpoint，并在决策日志记录确认；随后开始技术评审。

### 技术评审与审批

1. 基于已确认的契约和代码静态阅读，写出唯一选定方案到 `技术方案.md`，并完成“需求语义 → 实现映射”。精确接口、消息字段、资源、内部模块、文件、数据流和失败策略均在本阶段收敛；不得保留未收敛结论。
2. 新增 Objective-C 或 Swift 源文件时，将 `Drama.xcodeproj/project.pbxproj` 列入影响范围，仅用于工程引用和 target membership。
3. 技术评审发现外部能力不足、实现方案会改变用户可见行为，或存在必须由用户选择的产品取舍时，退回需求澄清，更新需求事实后重新取得 `CONFIRM_REQUIREMENT`。
4. 仅影响实现、且不改变需求契约业务语义的技术变更，记录在技术决策中并按计划审批规则处理，不回写或扩大需求契约。
5. 逐项检查 `计划审批.md` 门禁。任一门禁未通过时，不得提示 `APPROVE_PLAN`。
6. 门禁通过后才可请求用户回复 `APPROVE_PLAN`。收到后记录审批基准，进入编码。
7. 收到 `REQUEST_CHANGES: ...` 或 `SKIP_BLOCKER: ...` 时，按完整规则更新相关文档和决策日志，再重新评估门禁。

### 编码与交付

1. 只修改审批范围内的文件与模块，并遵循仓库的 `AGENTS.md` 和编码约定。
2. 审批后的 `技术方案.md` 是不可反向改写的审批基准；实际实现、偏离、验证和风险写入 `交付文档.md`。
3. 完成后更新 `交付文档.md`，写明实际改动范围、验证结果、未验证项、已知风险和后续事项。

## 文档规则

- 历史 checkpoint 和历史功能快照只读，只追加，不重写或迁移。
- 用标题、段落和编号列表表达需求事实、范围、规则和技术结论；checkbox 仅用于状态、待确认项和验证；表格仅用于多字段状态矩阵。
- 不手动修改 `lang.json`、`Localizable.strings` 等多语言产物；仅在文档中确认建议 key、默认中英文文案和使用场景。
- `决策日志.md` 仅追加稳定决策与变更，不记录搜索结果、普通进度或文件修改流水账；需求确认记录与技术决策记录必须分开。

需要精确阶段定义、确认口令处理、模板字段或审批基准规则时，先读取 [references/工作流说明.md](references/工作流说明.md)。
