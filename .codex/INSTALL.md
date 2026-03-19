# 安装到 Codex

把本仓库作为一个技能包暴露给 Codex 时，推荐直接暴露整个 `skills/` 目录，而不是把每个 skill 单独挂到 `~/.codex/skills/` 顶层。

这样做的目的有两个：

- `using-dify-dsl` 可以作为统一总入口，负责自动识别用户意图并路由到下游 skill。
- 包内其它 `dify-dsl-*` skill 仍然保持独立，可按需被直接点名或被入口自动调度。

## 推荐安装方式

优先直接运行仓库自带脚本：

```bash
bash scripts/install_codex_bundle.sh
```

脚本会做两件事：

- 创建 `~/.agents/skills/dify-dsl -> <repo>/skills`
- 清理当前仓库遗留在 `~/.codex/skills/` 下的散装 symlink

如果你更想手动操作，也可以按下面步骤执行。

1. 准备本仓库本地路径，例如：

```bash
/path/to/project-root
```

2. 创建 Codex 原生 skills 发现目录：

```bash
mkdir -p ~/.agents/skills
```

3. 把整个 `skills/` 目录作为一个 bundle 挂进去：

```bash
ln -s /path/to/project-root/skills ~/.agents/skills/dify-dsl
```

4. 重启 Codex。

## 从散装安装迁移

如果你之前已经把 `dify-dsl-*` 单独挂到了 `~/.codex/skills/`，推荐直接运行：

```bash
bash scripts/install_codex_bundle.sh
```

它只会移除那些“明确指向当前仓库 `skills/` 子目录”的旧 symlink，不会动别的 skill。

## 工作方式

- Codex 启动时会扫描 `~/.agents/skills/`
- `~/.agents/skills/dify-dsl/` 作为 bundle 根目录
- bundle 内会被发现的 skill 包括：
  - `using-dify-dsl`
  - `dify-dsl-brainstorming`
  - `dify-dsl-authoring`
  - `dify-dsl-review`
  - `dify-dsl-refactor`
  - 以及其余底座 / 验证 skill

## 推荐入口

日常优先从 `using-dify-dsl` 进入，再由它判断应该转到哪个下游 skill。

只有在你已经明确知道目标时，才直接点名某个 `dify-dsl-*` skill。

## 验证

```bash
find -L ~/.agents/skills/dify-dsl -maxdepth 2 -name SKILL.md | sort
```

如果安装成功，你会看到 `using-dify-dsl` 和整套 `dify-dsl-*` skill。

当前 Codex 版本在显式技能面板里仍可能列出 bundle 内的多个 `dify-dsl-*` skill。这里的目标是把本仓库作为一个 bundle 安装，并约定日常优先从 `using-dify-dsl` 进入，而不是依赖 UI 只显示一个入口。

## 兼容方式

把单个 skill 直接链接到 `~/.codex/skills/` 顶层仍然可用，但这更像“散装安装”，不利于把本仓库当成一个有统一入口的技能包来使用。
