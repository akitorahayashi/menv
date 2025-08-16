#!/bin/bash

# 依存関係をインストール
echo "[INFO] 依存関係をチェック・インストールします: visual-studio-code"
if ! brew list --cask visual-studio-code &> /dev/null; then
    brew install --cask visual-studio-code
    echo "IDEMPOTENCY_VIOLATION" >&2
fi

echo "[Start] VS Code のセットアップを開始します..."
vscode_target_dir="$HOME/Library/Application Support/Code/User"

# VS Code アプリケーションの存在確認
if [ ! -d "/Applications/Visual Studio Code.app" ]; then
    echo "[WARN] Visual Studio Code がインストールされていません。スキップします。"
    exit 0 # インストールされていなければエラーではない
fi
echo "[SUCCESS] Visual Studio Code はすでにインストールされています"

# ターゲットディレクトリの作成
mkdir -p "$vscode_target_dir"

# 設定ファイルのシンボリックリンクを作成
if [ $# -eq 0 ]; then
    echo "[WARN] 設定ディレクトリが指定されていません。VS Code設定のセットアップをスキップします。"
else
    for config_dir_base in "$@"; do
        config_dir="$config_dir_base/vscode"
        if [ -d "$config_dir" ]; then
            echo "[INFO] VS Code設定を $config_dir からセットアップします..."
            shopt -s nullglob
            for file in "$config_dir"/*; do
                if [ -f "$file" ]; then
                    filename=$(basename "$file")
                    target_file="$vscode_target_dir/$filename"

                    # シンボリックリンクの作成
                    if ln -sf "$file" "$target_file"; then
                        echo "[SUCCESS] VS Code設定ファイル $filename のシンボリックリンクを作成しました。"
                    else
                        echo "[ERROR] VS Code設定ファイル $filename のシンボリックリンク作成に失敗しました。"
                        exit 1
                    fi
                fi
            done
            shopt -u nullglob
        fi
    done
fi

echo "[SUCCESS] VS Code環境のセットアップが完了しました"

echo ""
echo "==== Start: VS Code環境を検証中... ===="
verification_failed=false

# 実際にシンボリックリンクが作成されているかを確認
if [ $# -eq 0 ]; then
    echo "[INFO] 設定ディレクトリの指定がないため、検証をスキップします。"
else
    linked_files_total=0
    for config_dir_base in "$@"; do
        config_dir="$config_dir_base/vscode"
        if [ -d "$config_dir" ]; then
            shopt -s nullglob
            for file in "$config_dir"/*; do
                if [ -f "$file" ]; then
                    filename=$(basename "$file")
                    target_file="$vscode_target_dir/$filename"
                    ((linked_files_total++))

                    if [ -L "$target_file" ]; then
                        link_target=$(readlink "$target_file")
                        # 最後のディレクトリの設定が適用されているはずなので、その場合のみOK
                        # この検証は完全ではないが、少なくともリンクが存在し、いずれかの設定ファイルを指していることを確認
                        echo "[INFO] VS Code設定ファイル $filename は $link_target を指しています。"
                    else
                        echo "[ERROR] VS Code設定ファイル $filename のシンボリックリンクが作成されていません。"
                        verification_failed=true
                    fi
                fi
            done
            shopt -u nullglob
        fi
    done

    if [ "$linked_files_total" -eq 0 ]; then
        echo "[WARN] VS Code用の設定ファイルがどの設定ディレクトリにも見つかりませんでした。"
    fi
fi


if [ "$verification_failed" = "true" ]; then
    echo "[ERROR] VS Code環境の検証に失敗しました"
    exit 1
else
    echo "[OK] VS Code環境の検証が完了しました"
fi