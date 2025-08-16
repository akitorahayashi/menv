#!/bin/bash

# 依存関係をインストール
echo "[INFO] 依存関係をチェック・インストールします: nvm, jq"
dependencies_changed=false
if ! brew list nvm &> /dev/null; then
    brew install nvm
    dependencies_changed=true
fi
if ! command -v jq &> /dev/null; then
    brew install jq
    dependencies_changed=true
fi
if [ "$dependencies_changed" = true ]; then
    echo "IDEMPOTENCY_VIOLATION" >&2
fi

# nvm環境を読み込む
export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
if [ -s "$(brew --prefix nvm)/nvm.sh" ]; then
    # shellcheck source=/dev/null
    . "$(brew --prefix nvm)/nvm.sh"
else
    echo "[ERROR] nvm.sh が見つかりません。nvm のインストールを確認してください"
    exit 1
fi

echo "[Start] Node.js のセットアップを開始します..."

# .nvmrcからNode.jsのバージョンを決定
NODE_VERSION=""
for config_dir in "$@"; do
    nvmrc_path="$config_dir/node/.nvmrc"
    if [ -f "$nvmrc_path" ]; then
        echo "[INFO] .nvmrc を読み込みます: $nvmrc_path"
        # shellcheck disable=SC2002
        version_from_file=$(cat "$nvmrc_path" | tr -d '[:space:]')
        if [ -n "$version_from_file" ]; then
            NODE_VERSION="$version_from_file"
            echo "[INFO] Node.jsのバージョンを ${NODE_VERSION} に設定します"
        fi
    fi
done

if [ -z "$NODE_VERSION" ]; then
    echo "[ERROR] .nvmrcファイルが見つからないか、バージョンが指定されていません。"
    exit 1
fi
readonly NODE_VERSION

# nvm経由でNode.jsをインストール・設定
node_changed=false
echo "[INFO] 指定されたバージョンのNode.jsをインストールします..."

# `nvm install` は冪等性があり、指定バージョンがなければインストールする
if nvm install "$NODE_VERSION"; then
    echo "[SUCCESS] Node.js ${NODE_VERSION} のインストール/確認が完了しました。"
else
    echo "[ERROR] Node.js ${NODE_VERSION} のインストールに失敗しました。"
    exit 1
fi

# デフォルトエイリアスが指定バージョンになっているか確認
expected_default_target="$(nvm version "$NODE_VERSION")"
current_default_target="$(nvm alias default 2>/dev/null | awk -F'->' 'NR==1{gsub(/^[ \t]+|[ \t]+$/,"",$2); print $2}' | awk '{print $1}')"
if [[ "$current_default_target" != "$expected_default_target" ]]; then
    echo "[CONFIGURING] Node.js ${expected_default_target} をデフォルトバージョンに設定します"
    if nvm alias default "$expected_default_target"; then
        echo "[SUCCESS] デフォルトバージョンを ${expected_default_target} に設定しました"
        node_changed=true
    else
        echo "[ERROR] デフォルトバージョンの設定に失敗しました"
        exit 1
    fi
else
    echo "[CONFIGURED] Node.js ${expected_default_target} はすでにデフォルトバージョンです"
fi

if [ "$node_changed" = true ]; then
    echo "IDEMPOTENCY_VIOLATION" >&2
fi

# 現在のシェルで指定バージョンを使用
if ! nvm use "$NODE_VERSION" > /dev/null; then
    echo "[ERROR] Node.js ${NODE_VERSION} への切り替えに失敗しました"
    exit 1
fi

# npm のインストール確認
if ! command -v npm &> /dev/null; then
    echo "[ERROR] npm が見つかりません。nvm の設定と Node.js のインストールを確認してください。"
    exit 1
fi
echo "[OK] npm は利用可能です"

# Node.jsのバージョンが変更された場合、パッケージが再インストールされることをユーザーに通知
if [ "$node_changed" = true ]; then
    echo "[INFO] Node.jsのグローバルバージョンが変更されたため、グローバルパッケージを新しいバージョン用にインストールします。"
    echo "[INFO] nvmはバージョンごとにパッケージを管理するため、古いバージョンのパッケージは削除されません。"
fi

# グローバルパッケージのインストール
package_files=()
for config_dir in "$@"; do
    packages_file="$config_dir/node/global-packages.json"
    if [ -f "$packages_file" ]; then
        package_files+=("$packages_file")
    fi
done

if [ ${#package_files[@]} -eq 0 ]; then
    echo "[WARN] global-packages.json が見つかりませんでした。パッケージのインストールをスキップします。"
else
    echo "[INFO] グローバルパッケージをチェック中..."
    # jqを使用してすべてのファイルからパッケージをマージ
    packages_json=$(jq -s 'map(.globalPackages) | add | to_entries[] | "\(.key)@\(.value)"' "${package_files[@]}")

    if [ -z "$packages_json" ]; then
        echo "[WARN] global-packages.json にパッケージが定義されていません"
    else
        packages_changed=false
        while IFS= read -r entry; do
            pkg_full="$entry"
            pkg_name="${entry%@*}"
            installed_version=$(npm list -g --depth=0 "$pkg_name" 2>/dev/null | grep -E "$pkg_name@[0-9]" | awk -F'@' '{print $NF}' || true)
            required_version=$(echo "$pkg_full" | awk -F'@' '{print $NF}')
            if [ "$required_version" == "latest" ]; then
                if [ -z "$installed_version" ]; then
                    if npm install -g "$pkg_full"; then
                        echo "[SUCCESS] $pkg_name のインストールが完了しました"
                        packages_changed=true
                    else
                        echo "[ERROR] $pkg_name のインストールに失敗しました"
                        exit 1
                    fi
                else
                    echo "[INSTALLED] $pkg_name (latest)"
                fi
            elif [ "$installed_version" != "$required_version" ]; then
                if npm install -g "$pkg_full"; then
                    echo "[SUCCESS] $pkg_name の更新が完了しました"
                    packages_changed=true
                else
                    echo "[ERROR] $pkg_name の更新に失敗しました"
                    exit 1
                fi
            else
                echo "[INSTALLED] $pkg_name"
            fi
        done <<< "$packages_json"
        if [ "$packages_changed" = true ]; then
            echo "IDEMPOTENCY_VIOLATION" >&2
        fi
    fi
fi

echo "[SUCCESS] Node.js 環境のセットアップが完了しました"

# Node.js 環境の検証
echo ""
echo "==== Start: Node.js 環境を検証中... ===="
verification_failed=false

# 期待されるバージョンがインストール時に決定した`NODE_VERSION`であるべき
EXPECTED_VERSION_STRING=$(nvm version "$NODE_VERSION")
CURRENT_VERSION_STRING=$(nvm current)

if [ "$CURRENT_VERSION_STRING" != "$EXPECTED_VERSION_STRING" ]; then
    echo "[ERROR] Node.jsのバージョンが期待値と異なります。期待: ${NODE_VERSION} (${EXPECTED_VERSION_STRING}), 現在: ${CURRENT_VERSION_STRING}"
    verification_failed=true
else
    echo "[SUCCESS] Node.js: $(node --version)"
    echo "[SUCCESS] npm: $(npm --version)"
fi

# グローバルパッケージの検証
if [ ${#package_files[@]} -gt 0 ]; then
    # jqを使用してすべてのファイルからパッケージ名をマージ
    packages_to_check=$(jq -s 'map(.globalPackages) | add | keys[]' "${package_files[@]}")
    missing=0
    if [ -n "$packages_to_check" ]; then
        while IFS= read -r pkg; do
            package_name=$(echo "$pkg" | tr -d '"') # remove quotes
            if ! npm list -g "$package_name" &>/dev/null; then
                echo "[ERROR] グローバルパッケージ $package_name がインストールされていません"
                ((missing++))
            else
                echo "[SUCCESS] グローバルパッケージ $package_name がインストールされています"
            fi
        done <<< "$packages_to_check"
    fi
    if [ "$missing" -gt 0 ]; then
        verification_failed=true
    fi
fi

if [ "$verification_failed" = "true" ]; then
    echo "[ERROR] Node.js 環境の検証に失敗しました"
    exit 1
else
    echo "[SUCCESS] Node.js 環境の検証が完了しました"
fi