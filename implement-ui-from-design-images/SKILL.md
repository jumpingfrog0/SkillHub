---
name: implement-ui-from-design-images
description: Analyze local UI design images and translate them into an implementation-ready UI structure, component reuse decisions, asset plan, implementation constraints, and visual validation plan. Use standalone or from another development workflow when UI references are stored in a design_images directory, when new icons are supplied under design_images/icons, or when a task requires precise design-image reading before UI implementation. When a formal staged workflow is active, require explicit caller stage and precision-read authorization before inspecting images or code.
---

# 从设计图实施 UI

精读本地设计图片，形成可执行的 UI 结构、组件、资源和验证结论。既可独立使用，也可作为其他开发工作流的条件门禁。

## 调用边界

- 独立调用时，根据用户请求完成设计精读；只有用户同时授权实施时才修改代码。
- 被其他工作流调用时，服从调用方提供的阶段、审批基准、影响范围和文档规则，不自行推进或绕过调用方门禁。
- 正式分阶段工作流处于活动状态时，不得把用户补充 `design_images/`、目录出现或本 Skill 自动触发解释为精读授权。
- 只处理设计理解和 UI 落地决策，不确认业务需求，不改变用户可见规则，不决定外部工作流的确认或审批状态。
- 遵循目标仓库的 `AGENTS.md`、平台规范和验证限制。

## 执行模式与阶段保护

只支持以下执行模式：

- `standalone`：用户独立要求精读设计图；用户的明确请求构成本次精读授权。
- `implementation-read`：由其他工作流调用，执行完整设计精读和 UI 落地判断。

检测到正式工作流处于活动状态时，必须按 `implementation-read` 处理，不得自行降级为 `standalone`。在打开设计图片、运行 Pillow、搜索目标代码或写入任何文档前，逐项检查：

1. `caller_workflow` 已明确。
2. `caller_stage` 已明确。
3. `execution_mode=implementation-read`。
4. `precision_read_authorized=true`。
5. `approval_boundary` 已提供，并声明当前阶段允许精读。

任一项缺失、冲突或未授权时立即停止，只返回“调用条件不完整或尚未到精读阶段”。不得枚举图片内容、读取原始像素、检查组件调用方、形成 UI/资源方案或修改调用方文档。调用方阶段规则始终优先于本 Skill 的目录触发条件。

## 输入契约

开始前确定以下输入。独立调用使用 `execution_mode=standalone`；被其他工作流调用时，前五项必须由调用方显式提供，不得从目录或会话措辞推断：

1. `caller_workflow`，独立调用时填写 `standalone`。
2. `caller_stage`，独立调用时填写 `standalone`。
3. `execution_mode`。
4. `precision_read_authorized`。
5. `approval_boundary`。
6. 任务根目录或明确的 `design_images` 路径。
7. 已确认的视觉、交互和内容约束。
8. 目标平台、现有实现范围及可复用组件范围。
9. 用户或调用方明确声明的图片倍率；未声明时使用默认倍率。
10. 允许执行的验证方式。
11. 已有的设计输入 fingerprint；首次精读或不存在时留空。

## 目录与倍率

按以下优先级解析设计目录：

1. 使用用户或调用方明确给出的 `design_images` 路径。
2. 已给出任务根目录时，使用 `<task-root>/design_images/`。
3. 独立调用且未给出路径时，使用当前任务目录下的 `design_images/`。
4. 默认目录不存在时报告材料缺失，不做仓库级模糊搜索。

目录语义固定为：

```text
design_images/
  <页面、弹窗或状态设计图>
  icons/
    <新增图标或图片资源>
```

- 将 `design_images/` 根目录中的图片作为页面、弹窗或状态设计图。
- 枚举设计图时排除 `icons/`，随后单独枚举并检查 `design_images/icons/`。
- 将 `icons/` 中的文件作为独立原始资源，不得当作完整设计页面，也不得从页面截图重新裁切同一资源。
- 默认所有设计图和图标均为 `1x`；只有用户或调用方明确声明其他倍率时才覆盖。
- 默认按 `1 px = 1 设计布局单位` 解释；其他倍率按 `布局尺寸 = 原始像素尺寸 ÷ 倍率` 换算。
- 不得根据文件名、画布大小、设备分辨率或视觉观感自行推断倍率。
- 同一目录需要混用不同倍率时，要求调用方明确每组文件的倍率，不得混合猜测。

## Fingerprint 与复用

- 在允许精读的阶段，按排序后的相对路径和文件内容计算 `design_images/` 的单一 fingerprint；计算范围包含 `icons/`，不使用修改时间。
- 已有 fingerprint 与本次 fingerprint 相同时，直接复用已有设计精读结论，不重复打开图片、读取原始像素或重新测量。
- fingerprint 不同时，重新精读设计稿；不增加其他自动失效条件。
- 用户或调用方明确要求重新精读时，无论 fingerprint 是否相同都重新执行。
- 只保存和传递 fingerprint，不为复用机制增加独立状态、详细测量快照或额外 checkpoint。

## 精读流程

开始完整精读前先执行 fingerprint 复用判断。命中复用时跳过步骤 1 至 3，沿用已有设计结论继续完成当前调用范围内的 UI 落地与门禁判断。

### 1. 检查材料

完整枚举设计图和图标，记录文件类型、原始像素尺寸、颜色模式、Alpha、声明倍率和可读状态。检查是否缺少关键页面、交互状态、异常状态或资源。

### 2. 原始像素读取

- 使用 Pillow 按原始文件读取本地位图的尺寸、mode、Alpha、有效像素边界和需要核对的颜色或坐标。
- 逐张以原始清晰度进行视觉检查，不以缩略图、压缩预览或主观观感代替精读。
- 需要读取 Figma 等设计平台时，使用对应的专用设计读取 skill；本 Skill 继续负责统一落地判断和输出。
- 将详细像素、间距、坐标和颜色采样保留为当前执行依据，除非用户明确要求，不创建或写入详细测量文档。

### 3. 还原设计语义

梳理页面层级、布局分区、内容优先级、滚动与固定区域、点击区域、默认/选中/禁用/加载/失败状态、弹出与关闭行为，以及不同设计图之间的状态变化。区分业务交互基准与视觉基准，不用参考实现覆盖已确认的设计约束。

### 4. 形成 UI 结构

结合目标代码静态阅读，将 UI 按单一职责划分为容器、区块和可复用单元。避免把无关状态和交互集中到单一巨型组件，也不要在未检查现有能力前重复创建组件。

对候选复用组件执行确定性判断：

1. 与设计一致时直接复用。
2. 差异有限且共享影响可控时，检查全部调用方后做最小修改。
3. 修改会明显影响其他功能时，保留共享组件并使用任务范围内的专用组件。
4. 原有 UI 划分不合理时，在授权范围内按单一职责重新拆分或合并。

### 5. 形成资源方案

- 优先使用 `design_images/icons/` 中已提供的原始资源，并核对格式、像素尺寸、Alpha、透明边距、设计显示尺寸和缩放方式。
- 明确每项资源是复用、迁移、新增还是不需要接入。
- 将具体平台资源目录、命名、工程引用和 target 接入交给目标平台规则决定。
- 资源缺失、版本冲突、用途不明或需要猜测时，将其标记为阻塞项。

### 6. 执行门禁判断

只有以下条件全部满足，设计精读门禁才可通过：

- 设计材料可读，声明倍率明确，所需页面与状态足以支持实施。
- UI 层级、交互区域和关键状态已完成核对。
- 组件复用、最小修改、专用组件和职责拆分已收敛。
- 图片与图标资源的来源和处理方式已明确。
- 未发现与已确认用户可见规则冲突的设计内容。
- 实施范围和视觉验证计划明确。

发现设计内容会改变用户可见行为时，返回需求确认；发现实现需要超出调用方审批范围时，返回计划审批。仅影响内部 UI 组织且处于预授权范围内的调整，可作为技术决策继续推进。

## 输出契约

向用户或调用方返回以下结论，不输出冗长测量流水账：

1. `caller_workflow`、`caller_stage`、`execution_mode` 和本次授权检查结果。
2. 设计目录、材料完整性和实际采用的倍率。
3. 本次设计输入 fingerprint，以及本次是复用还是重新精读。
4. 页面、状态和图标清单。
5. UI 结构与职责划分。
6. 组件复用、最小修改或专用组件决策。
7. 资源处理和平台接入要求。
8. 阻塞项及解除条件。
9. 是否改变用户可见行为。
10. 是否超出授权或审批范围。
11. 视觉验证计划。
12. 门禁结论：通过、阻塞、退回需求确认或退回计划审批。

独立调用且用户已授权实施时，门禁通过后按上述结论编码并验证。被其他工作流调用时，将结论交回调用方，由调用方决定文档记录、阶段推进和实施授权。
