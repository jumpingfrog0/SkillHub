---
name: feature-discovery
description: 用于探索已有业务功能、梳理当前业务规则和技术实现，并在需要时沉淀为业务梳理和技术实现梳理文档。Use when asked to investigate an existing feature, trace business rules, map implementation code paths, or generate feature discovery documentation. This skill is read-only by default and does not propose implementation plans or modify production code.
---

# Feature Discovery

使用这个 skill 探索已有功能，并记录当前实际存在的业务行为和技术实现。默认产物是结构化的现状理解；只有当用户明确要求写文档、沉淀文档或生成文档时，才产出两份文档：

- `<feature-name>业务梳理.md`
- `<feature-name>技术实现梳理.md`

## 边界

- 不修改生产代码。
- 不写实现方案、方案选项、推荐方案、修改范围或任务拆分。
- 不把推测写成事实。明确区分已确认事实、推测行为和待确认问题。
- 重要结论优先给出证据，例如文件路径、类名、方法名、接口名、配置 key、实验名、feature flag、埋点名或资源标识。
- 配置、实验、feature flag、开关和埋点是必须显式检查的对象。如果未发现，记录“未发现”或“待确认”，不要静默省略。

## 项目约束

在探索或写文档前，先阅读并遵守当前仓库适用的项目约束，例如：

- `AGENTS.md`
- README
- 既有文档规范
- 验证限制
- 文档输出目录和命名规则

这个 skill 只定义通用方法论。具体项目约束由当前仓库决定。如果仓库指定了文档目录，使用项目指定目录；如果没有指定目录且用户要求写文档，默认使用 `docs/feature-discovery/`。

## 工作流

1. 从用户请求中确认探索范围：
   - 功能名称
   - 目标平台或模块
   - 已知入口、页面、接口、命令、屏幕或用户动作
   - 用户是只需要探索回复，还是明确要求写入文档
2. 在下结论或选择文档路径前，先阅读项目约束。
3. 定位入口：
   - 路由、页面、控制器、Fragment、Activity、组件、命令、handler、service 或 API
   - 用户动作、回调、delegate、observer、listener、生命周期方法或 reducer
4. 追踪当前行为：
   - 用户路径
   - 业务规则
   - 状态变化
   - API 和数据流
   - 持久化和缓存行为
   - 配置、实验、开关、降级、资源、文案和埋点依赖
5. 建立技术实现地图：
   - 关键文件
   - 关键类、结构体、方法、函数或组件
   - 调用链路
   - 数据模型和响应处理
   - 错误、空态、加载、禁用、兜底和边界状态
6. 归纳发现：
   - 区分已确认事实和推测行为
   - 列出缺失证据和待确认问题
   - 避免提出改动建议；如果用户另行要求实现工作，那已经超出本 skill 的默认范围
7. 如果要写文档，先读取 `references/` 中的模板，并按项目约束填充：
   - `references/business-doc-template.md`
   - `references/technical-implementation-template.md`

## 输出规则

只回复、不写文件时，保持以下结构：

1. 业务梳理
2. 技术实现梳理
3. 已确认事实
4. 待确认问题

写文件时：

- 除非用户另有要求，只写两份探索文档。
- 文件名使用功能名加固定后缀：`业务梳理.md` 和 `技术实现梳理.md`。
- 如果项目已有文档目录约定，使用项目文档目录。
- 关键结论必须尽量包含证据。
- 对缺失的配置、实验、开关、埋点、资源或文案证据进行显式标注。
