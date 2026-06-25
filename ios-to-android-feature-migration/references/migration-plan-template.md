# Android Migration Plan Template

Use this template for:

```text
.huangdonghong/feature-migration/<feature-slug>/Android迁移方案.md
```

The plan must be written before Android code changes and must be confirmed by the user before implementation.

## Header

```markdown
# <功能名> Android迁移方案

- 作者：huangdonghong
- Android仓库：famo-android
- iOS仓库：drama-ios
- 输入业务文档：<path>
- 输入技术文档：<path>
- 输出目录：.huangdonghong/feature-migration/<feature-slug>/
- 状态：待确认
```

## Required Sections

### 1. 迁移目标

- State the exact Android user-facing behavior to deliver.
- State the iOS feature scope being migrated.
- State any explicitly excluded behavior.

### 2. iOS事实摘要

Summarize only facts supported by feature-discovery documents or targeted code evidence:

- User path and entry points.
- Business rules and state transitions.
- API/RPC/model fields.
- Configuration, experiment, feature flag, and server switch dependencies.
- Resource, string, and analytics dependencies.
- Empty, loading, error, disabled, fallback, and compatibility behavior.

### 3. iOS证据抽查结论

- List inspected iOS files/classes/functions.
- Record confirmed facts.
- Record conflicts between documents and code.
- Record missing evidence.
- Mark conflicts that block implementation decisions.

### 4. Android现状与差异

- Existing Android entry points and nearest feature patterns.
- Existing modules and ownership boundaries.
- Existing protocol/API/resource/storage/analytics capabilities.
- Behavior gaps between iOS and Android.
- Android-specific compatibility or product differences.

### 5. Android实现方案

Provide a single decision-complete implementation path:

- Target module and package.
- Classes, layouts, resources, protocol interfaces, and data models to add or modify.
- Data flow and state flow.
- Network/RPC integration.
- Local storage and cache rules.
- UI implementation approach and lifecycle handling.
- Resource, string, and efox/configuration handling.
- Analytics/logging changes.
- Error, empty, loading, disabled, fallback, and edge states.

Do not list competing options as the conclusion. If alternatives were considered, put them in a short "discarded alternatives" note with the chosen path clearly stated.

### 6. 文件改动清单

List expected Android files grouped by purpose:

- Production code.
- Resources and strings.
- Protocol/header interfaces.
- Documentation.

Keep this scoped to the confirmed migration only.

### 7. 验证计划

List only validation allowed by the Android project constraints:

- Static searches.
- Text checks.
- `git diff --check`.
- Manual acceptance scenarios.

Explicitly state prohibited commands that will not be run, such as Gradle, adb, sdkmanager, or emulator commands, when the project rules prohibit them.

### 8. 风险与待确认问题

- Blocking questions that must be resolved before coding.
- Non-blocking risks.
- Missing evidence.
- Product or backend dependencies.

If any blocking question remains, set plan status to "阻塞，待确认" and do not implement.
