# menv CLIにおける共通Agent Skills導入計画 (SSOT版)

## 1. 概要と目的

本計画では、`menv` リポジトリ内の単一ディレクトリ（SSOT）でエージェントスキルを一元管理し、Ansibleを通じて `Codex CLI`, `Claude Code`, `Gemini CLI` の全環境へ同一のスキルセットをシンボリックリンクとして展開します。

これにより、エージェントごとのスキル差分を排除し、どのツールを使用しても統一されたワークフローと能力（共通インターフェース）を提供します。

## 2. ディレクトリ構成 (SSOT)

ツール別のディレクトリ分けを廃止し、全てのスキルを `common/coder/skills/` 直下でフラットに管理します。

**ソースディレクトリ (SSOT):**

```text
src/menv/ansible/roles/nodejs/config/common/coder/skills/
├── svo-cli-design/         # [共通スキル (SVO CLI設計)]
│   ├── SKILL.md            # 共通定義 (Open Agent Skills標準)
│   └── agents/             # 各エージェント（Codex/Gemini等）用のメタデータ
│       └── openai.yaml     # Codex用など (他ツールは無視する前提)

```

## 3. 展開戦略とAnsible実装計画

`src/menv/ansible/roles/nodejs/tasks/coder.yml` を修正し、定義された共通スキル群を3つのターゲット環境へ一括展開するロジックを実装します。

### 3.1. ターゲット環境

以下のディレクトリに対し、共通スキルへのシンボリックリンクを作成します。

* `~/.codex/skills/`
* `~/.claude/skills/`
* `~/.gemini/skills/`

### 3.2. Ansible タスク設計

メンテナビリティを高めるため、スキルリストとターゲットツールリストを組み合わせて処理します。

**ロジックの概要:**

1. **ターゲットディレクトリの確保**: 各ツールの `skills` ディレクトリを作成。
2. **クロス展開 (Matrix Deployment)**: 「全スキル」×「全ツール」の組み合わせでリンクを作成。

**`coder.yml` への追加実装案:**

```yaml
# 1. スキル格納用ディレクトリの作成
- name: "Ensure Agent Skills base directories exist"
  ansible.builtin.file:
    path: "{{ ansible_env.HOME }}/.{{ item }}/skills"
    state: directory
    mode: "0755"
  loop:
    - codex
    - claude
    - gemini

# 2. 共通スキルの展開 (SSOT -> 各ツール)
# メンテナビリティのため、loop処理で一括定義
- name: "Deploy Common Agent Skills to all CLIs"
  ansible.builtin.file:
    # SSOT: 共通のスキルソースを参照
    src: "{{ local_config_root }}/nodejs/common/coder/skills/{{ item.skill }}"
    # Destination: 各ツールのフォルダへ配置
    dest: "{{ ansible_env.HOME }}/.{{ item.tool }}/skills/{{ item.skill }}"
    state: link
    force: true
  loop:
    # ネストされたループ、または `with_nested` 的なリスト定義で展開
    # 例: svo-cli-design を 3つのツールへ展開
    - { skill: 'svo-cli-design', tool: 'codex' }
    - { skill: 'svo-cli-design', tool: 'claude' }
    - { skill: 'svo-cli-design', tool: 'gemini' }

```

*(実装時は `with_nested` や `product` フィルタを使用して、スキルが増えた際の記述量を減らす工夫も可能です)*

## 4. 共通インターフェースの維持方針

### 4.1. Open Agent Skills 標準への準拠

全てのスキルは、各ツールが共通して解釈可能な「Open Agent Skills標準」に準拠した `SKILL.md` を核とします。

* **SKILL.md**: スキルの目的、使用法、プロンプト指示を記述。これは全ツールで共通解釈されます。
* **Scripts**: シェルスクリプト等はPOSIX準拠などを意識し、どのエージェントが実行しても動作するようにします。

### 4.2. ツール固有ファイルの扱い

* Codex CLI等で必要となる `agents/openai.yaml` 等が含まれていても、ClaudeやGeminiは単にそれを無視する（または参照しない）ため、同一ディレクトリを配布しても副作用はありません。これにより、完全なポータビリティを維持できます。

## 5. 期待される効果

1. **運用コストの最小化**: `SKILL.md` を一箇所修正するだけで、Codex, Claude, Gemini の全ての挙動が同期して改善されます。
2. **一貫性 (Consistency)**: 「CodexではできるがClaudeではできない」といったスキルの分断を防ぎます。
3. **SSOTの確立**: リポジトリ上の `config/common/coder/skills` が唯一の正解となり、環境構築の再現性が保証されます。

この計画に基づき、`coder.yml` の修正と共通スキルディレクトリの作成を進めることを推奨します。