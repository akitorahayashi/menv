#!/bin/bash

# Function to verify brew/cask items
verify_items() {
  local type=$1
  local brewfile_path=$2
  local cmd=(brew info)
  [[ $type == "cask" ]] && cmd+=(--cask)

  while read -r item; do
    if ! "${cmd[@]}" "$item" &>/dev/null; then
      echo "[ERROR] CI: ${type}パッケージ '$item' が見つかりません。（$brewfile_path）"
      verification_failed=true
    else
      echo "[SUCCESS] CI: ${type}パッケージ '$item' はインストール可能です。（$brewfile_path）"
    fi
  done < <(grep "^$type " "$brewfile_path" | awk -F'"' '{print $2}')
}

# Homebrewのインストール
if ! command -v brew &> /dev/null; then
    echo "[INSTALL] Homebrew ..."
    
    install_url="https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh"
    echo "[INFO] Homebrewインストールスクリプトを実行します..."
    if [ "${CI:-false}" = "true" ]; then
        echo "[INFO] CI環境では非対話型でインストールします"
        NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL "$install_url")"
    else
        /bin/bash -c "$(curl -fsSL "$install_url")"
    fi
    
    
    if ! command -v brew; then
        echo "[ERROR] Homebrewのインストールに失敗しました"
        exit 1
    fi
    echo "[OK] Homebrewバイナリのインストールが完了しました。"
    echo "[SUCCESS] Homebrew のインストール完了"
else
    echo "[SUCCESS] Homebrew はすでにインストールされています"
fi

# Brewfileのインストール
echo ""
echo "[Start] Homebrew パッケージのインストールを開始します..."

if [ $# -eq 0 ]; then
    echo "[WARN] 設定ディレクトリが指定されていません。Brewfileのインストールをスキップします。"
else
    for config_dir in "$@"; do
        brewfile_path="$config_dir/brew/Brewfile"
        echo "[INFO] 処理中のBrewfile: $brewfile_path"

        if [ -f "$brewfile_path" ]; then
            if [ "${CI:-false}" = "true" ]; then
                # CI環境ではインストールせず存在確認のみ
                echo "[INFO] CI: Brewfileのパッケージがインストール可能か確認します..."
                verification_failed=false

                verify_items "brew" "$brewfile_path"
                verify_items "cask" "$brewfile_path"

                if [ "$verification_failed" = "true" ]; then
                    echo "[ERROR] CI: Brewfileの検証に失敗しました: $brewfile_path"
                    exit 1
                else
                    echo "[SUCCESS] CI: すべてのパッケージがインストール可能です: $brewfile_path"
                fi
            else
                if ! brew bundle --file "$brewfile_path"; then
                    echo "[ERROR] Brewfileからのパッケージインストールに失敗しました: $brewfile_path"
                    exit 1
                fi
                echo "[OK] Homebrew パッケージのインストール/アップグレードが完了しました: $brewfile_path"
            fi
        else
            echo "[WARN] Brewfileが見つかりません。スキップします: $brewfile_path"
        fi
    done
fi

echo "[SUCCESS] Homebrewのセットアップが完了しました"

# CIでない場合のみHomebrew環境を検証
if [ "${CI:-false}" != "true" ]; then
    echo "[Start] Homebrew環境を検証中..."
    verification_failed=false

    # Homebrew パスの確認
    BREW_PATH=$(command -v brew)
    expected_path="$(brew --prefix)/bin/brew"
    if [[ "$BREW_PATH" != "$expected_path" ]]; then
        echo "[ERROR] Homebrewのパスが想定と異なります"
        echo "[ERROR] 期待: $expected_path"
        echo "[ERROR] 実際: $BREW_PATH"
        verification_failed=true
    else
        echo "[SUCCESS] Homebrewのパスが正しく設定されています: $BREW_PATH"
    fi

    # パッケージの確認
    if [ $# -eq 0 ]; then
        echo "[INFO] 設定ディレクトリの指定がないため、パッケージチェックをスキップします。"
    else
        for config_dir in "$@"; do
            brewfile_path="$config_dir/brew/Brewfile"
            if [ -f "$brewfile_path" ]; then
                if ! brew bundle check --file="$brewfile_path"; then
                    echo "[ERROR] Brewfileで定義されたパッケージの一部がインストールされていません: $brewfile_path"
                    verification_failed=true
                else
                    echo "[SUCCESS] すべてのパッケージがインストールされています: $brewfile_path"
                fi
            fi
        done
    fi


    if [ "$verification_failed" = "true" ]; then
        echo "[ERROR] Homebrew環境の検証に失敗しました"
        exit 1
    else
        echo "[SUCCESS] Homebrew環境の検証が完了しました"
    fi
fi