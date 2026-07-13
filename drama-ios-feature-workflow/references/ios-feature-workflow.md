# iOS 新需求工作流

本工作流用于在 drama-ios 项目内启动和推进新的 iOS 业务需求。核心目标是把需求澄清、技术收敛、审批、编码和交付分开管理，保留关键决策追溯，同时避免每轮生成重复的大文档。

## 工作模式

只使用轻量快照评审模式。

历史快照只读，不得修改。

需求目录结构为：

```text
.huangdonghong/feature/<feature-id>/
  snapshot_index.md
  intake.md
  decision_log.md
  requirement_contract.md
  tech_plan.md
  approval.md
  handoff.md
```

`snapshot_index.md` 是需求入口和 checkpoint 时间线。其他文档按阶段逐步生成，不要求在启动时一次性填满。

## 模板位置

Skill 模板放在：

```text
.agents/skills/drama-ios-feature-workflow/assets/
```

模板文件包括：

```text
snapshot_index.md        # 需求入口、当前状态和 checkpoint 时间线
intake.md                # 原始需求、材料来源、目标模块和初始缺口
decision_log.md          # 已确认规则、关键决策、需求变更和技术变更
requirement_contract.md  # 功能范围、非目标、业务规则、协议、资源、文案和验收标准
tech_plan.md             # 唯一选定方案、影响范围、关键数据流、风险和验证计划
approval.md              # 门禁检查、审批记录和审批基准
handoff.md               # 交付摘要、验证结果、未验证项、已知风险和后续事项
```

编码过程状态由 Codex 会话维护，稳定决策写入 `decision_log.md`，最终交付写入 `handoff.md`。

## 文档表达规则

需求事实使用标题、段落和编号列表表达。

checkbox 只用于状态跟踪、待确认项、任务完成情况和验证执行情况。

表格只用于材料来源、门禁检查、验证结果、阻塞项等多字段状态矩阵。

不得用 checkbox 表达功能范围、业务规则和最终技术结论。

## 阶段状态规则

阶段固定为：

- 需求接收
- 需求澄清
- 需求契约已确认
- 技术评审
- 待审批
- 已审批
- 编码中
- 验证完成

生成 `requirement_contract.md` 只表示需求契约草稿已生成，不代表需求澄清完成。

只要存在阻塞项、待确认项或用户 review 未完成，当前阶段必须保持为 `需求澄清`。

只有用户明确确认需求契约后，才允许把 `requirement_contract.md` 状态标记为 `已确认`，并把当前阶段推进为 `需求契约已确认`。

只有 `requirement_contract.md` 状态为 `已确认`，才允许进入技术评审并生成可推进的 `tech_plan.md`。

`snapshot_index.md` 的 checkpoint 必须区分“需求契约草稿已生成”和“需求契约已确认”。

用户确认需求契约的固定口令为：

```text
CONFIRM_REQUIREMENT
```

收到 `CONFIRM_REQUIREMENT` 后，Agent 必须：

1. 读取 `snapshot_index.md`、`requirement_contract.md` 和 `decision_log.md`。
2. 检查 `requirement_contract.md` 是否仍有未决事项。
3. 如果仍有未决事项，拒绝推进，保持当前阶段为 `需求澄清`，并输出剩余未决事项。
4. 如果无未决事项，把 `requirement_contract.md` 状态标记为 `已确认`。
5. 把 `snapshot_index.md` 当前阶段推进为 `需求契约已确认`，并追加 checkpoint。
6. 在 `decision_log.md` 记录需求契约确认。
7. 进入技术评审，生成或更新 `tech_plan.md`。

`CONFIRM_REQUIREMENT` 只表示需求契约已确认，不代表技术方案已审批，不允许进入编码，不允许生成通过状态的 `approval.md`。

## 启动规则

当用户要求启动 iOS 新需求工作流时，Agent 必须：

1. 根据需求名称生成可读的 `<feature-id>`，例如 `房间公屏@功能` 使用 `room_public_mention`。
2. 创建 `.huangdonghong/feature/<feature-id>/snapshot_index.md`。
3. 创建 `.huangdonghong/feature/<feature-id>/intake.md`。
4. 按用户输入的主要结构整理原始需求，记录材料来源、目标模块和初始缺口。
5. 在 Codex 会话中完成第一轮需求澄清。
6. 不得进入编码阶段，除非 `approval.md` 已记录门禁通过，并且用户明确回复 `APPROVE_PLAN`。

如果已存在需求目录，Agent 必须先读取 `snapshot_index.md`，确认当前状态、审批基准和最近 checkpoint，再继续推进。

## 需求澄清规则

需求澄清阶段优先在 Codex 会话中完成，不为每轮问答创建完整文档。

只有稳定结论才写入文档。稳定结论包括：

- 会影响编码范围的功能边界。
- 会影响接口、协议、消息字段的数据规则。
- 会影响图片资源、i18n key、路由跳转的资源规则。
- 会影响状态模型、展示条件、失败处理的业务规则。
- 会影响验收标准的产品规则。

澄清过程中可以生成 `requirement_contract.md` 草稿。该文件只记录当前已确认内容和未决事项，不记录临时推理过程。

如果仍存在阻塞项，不得把 `requirement_contract.md` 标记为 `已确认`，不得生成可审批技术方案。阻塞项必须写入 `decision_log.md`，并明确解除条件。

## 多语言规则

新增文案必须确认多语言 key。

Agent 只在文档中给出建议 key、中文默认文案、英文默认文案和使用场景。

Agent 不修改 `lang.json`、`Localizable.strings` 等多语言产物。多语言文件由开发者通过自动化脚本更新。

多语言 key 未确认时属于阻塞项，不得进入技术评审、可审批技术方案或编码。

## 技术评审规则

技术评审阶段优先在 Codex 会话中完成，不为每轮方案讨论创建完整文档。

Agent 必须基于已确认的 `requirement_contract.md` 和代码静态阅读输出唯一选定方案，并生成 `tech_plan.md`。

`tech_plan.md` 必须包含：

1. 目标和非目标。
2. 唯一选定方案。
3. 影响范围。
4. 关键数据流和状态流。
5. 风险和缓解方案。
6. 验证计划。

若技术方案新增 Objective-C/Swift 源码文件，必须把 `Drama.xcodeproj/project.pbxproj` 列入影响范围，用途仅限工程引用和 target membership。

进入审批前，`tech_plan.md` 不得保留未收敛结论。无法收敛的内容必须回到 Codex 会话继续确认，并追加到 `decision_log.md`。

## 决策日志规则

`decision_log.md` 只追加稳定决策和变更，不写执行流水账。

必须记录：

- 用户确认的业务规则。
- 用户确认的接口、协议、资源、文案、跳转规则。
- 技术方案中的关键取舍。
- 编码中发现审批方案需要变化的原因和用户确认结果。
- 用户明确跳过阻塞项的记录。

不得把普通任务进度、文件修改清单、临时搜索结果写入 `decision_log.md`。

## 计划审批门禁

生成 `approval.md` 前必须满足：

- 阻塞项为空，用户已明确跳过的阻塞项已记录在 `decision_log.md`。
- 必须确认问题为空。
- `requirement_contract.md` 已由用户明确确认，状态为 `已确认`。
- `requirement_contract.md` 已明确功能范围和验收标准。
- 新增文案的多语言 key 已确认。
- `tech_plan.md` 已收敛为唯一选定方案。
- 实施范围明确。
- 验证计划明确。

如果门禁不通过：

- 不得提示用户 `APPROVE_PLAN`。
- 不得进入编码。
- 必须在 `decision_log.md` 记录剩余阻塞项和解除条件。

## 计划审批

只有 `approval.md` 记录门禁通过后，才允许提示用户审批技术方案。

用户可回复：

```text
APPROVE_PLAN
```

用户要求调整方案时回复：

```text
REQUEST_CHANGES: <需要调整的内容>
```

用户允许跳过阻塞项时回复：

```text
SKIP_BLOCKER: <跳过的阻塞项和允许的替代方案>
```

收到 `REQUEST_CHANGES` 后，Agent 必须更新 `decision_log.md`，并根据变更内容更新 `requirement_contract.md`、`tech_plan.md`、`approval.md`。

收到 `APPROVE_PLAN` 后，Agent 必须在 `approval.md` 记录审批结果和审批基准，再进入编码。

## 技术方案审批基准规则

`tech_plan.md` 在审批前可以根据技术评审结果正常迭代。

收到 `APPROVE_PLAN` 后，`tech_plan.md` 成为本次审批对应的技术方案基准，不再作为最终实现文档维护。

审批后不得按最终代码反向改写 `tech_plan.md` 的方案正文。若需要标记状态，只允许追加简短说明，例如“本文件为本次 `APPROVE_PLAN` 对应的技术方案基准”。

编码中发现必须扩大影响范围或改变已审批方案时，Agent 必须暂停编码，说明变化原因和影响，并先更新 `decision_log.md`；必要时同步更新 `tech_plan.md` 和 `approval.md` 形成新的审批基准，用户确认后才允许继续。

功能完成后的实际交付、最终实现与审批基准的差异、未验证项和风险统一写入 `handoff.md`。

## 编码实施

进入编码后，Agent 必须遵守：

1. 只修改 `tech_plan.md` 和 `approval.md` 列出的范围。
2. 如果需要扩大范围，先暂停并说明原因，用户确认后再更新 `decision_log.md`、`tech_plan.md`、`approval.md`。
3. 不猜服务端接口、消息协议、路由规则、图片资源和 i18n key。
4. 不新增未审批的依赖。
5. 不维护单独的实现流水账文档。
6. 不静默忽略构建、测试、lint 和项目约定检查失败。

编码过程状态保留在 Codex 会话中。稳定决策变化写入 `decision_log.md`，最终交付写入 `handoff.md`。

## 验证与交付

完成后必须生成或更新 `handoff.md`，至少包含：

- 交付摘要。
- 实际改动范围。
- 偏离审批方案的内容。
- 验证结果。
- 未验证项。
- 已知风险。
- 后续事项。

如果无法运行某些验证，必须明确说明原因。

## 历史快照规则

历史功能快照保持只读，不迁移、不重写。
