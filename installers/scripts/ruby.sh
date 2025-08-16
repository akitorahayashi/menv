#!/bin/bash

unset RBENV_VERSION

# 依存関係をインストール
echo "[INFO] 依存関係をチェック・インストールします: openssl, rbenv"
changed=false

# Rubyのコンパイルエラーを防ぐため、opensslを先にインストール
if ! brew list openssl >/dev/null 2>&1 && ! brew list openssl@3 >/dev/null 2>&1; then
    echo "[INSTALL] openssl (for Ruby compilation)"
    if brew install openssl; then
        echo "[SUCCESS] openssl をインストールしました"
        changed=true
    else
        echo "[ERROR] openssl のインストールに失敗しました"
        exit 1
    fi
fi

# rbenv をインストール (ruby-build は依存関係として自動でインストールされる)
if ! command -v rbenv &> /dev/null; then
    echo "[INSTALL] rbenv"
    if brew install rbenv; then
        echo "[SUCCESS] rbenv をインストールしました (ruby-build も自動でインストールされます)"
        changed=true
        eval "$(rbenv init -)"
        rbenv rehash
    else
        echo "[ERROR] rbenv のインストールに失敗しました"
        exit 1
    fi
fi

echo "==== Start: Ruby環境のセットアップを開始します..."

# rbenvを初期化して、以降のコマンドでrbenvのRubyが使われるようにする
eval "$(rbenv init -)"

# .ruby-versionファイルからRubyのバージョンを決定
RUBY_VERSION=""
for config_dir in "$@"; do
    version_file="$config_dir/ruby/.ruby-version"
    if [ -f "$version_file" ]; then
        echo "[INFO] .ruby-version を読み込みます: $version_file"
        version_from_file=$(tr -d '[:space:]' < "$version_file")
        if [ -n "$version_from_file" ]; then
            RUBY_VERSION="$version_from_file"
            echo "[INFO] Rubyのバージョンを ${RUBY_VERSION} に設定します"
        fi
    fi
done

if [ -z "$RUBY_VERSION" ]; then
    echo "[ERROR] .ruby-versionファイルが見つからないか、バージョンが指定されていません。"
    exit 1
fi
readonly RUBY_VERSION

# 指定されたバージョンのRubyがインストールされていなければインストール
if ! rbenv versions --bare | grep -q "^${RUBY_VERSION}$"; then
    echo "[INSTALL] Ruby ${RUBY_VERSION}"
    # openssl@3 を優先し、なければフォールバック
    if brew list --versions openssl@3 >/dev/null 2>&1; then
        export RUBY_CONFIGURE_OPTS="--with-openssl-dir=$(brew --prefix openssl@3)"
    else
        export RUBY_CONFIGURE_OPTS="--with-openssl-dir=$(brew --prefix openssl)"
    fi
    if ! rbenv install -s "${RUBY_VERSION}"; then
        echo "[ERROR] Ruby ${RUBY_VERSION} のインストールに失敗しました"
        exit 1
    fi
    unset RUBY_CONFIGURE_OPTS
    changed=true
else
    echo "[INFO] Ruby ${RUBY_VERSION} はすでにインストールされています"
fi

# グローバルバージョンを指定されたバージョンに設定
if [ "$(rbenv global)" != "${RUBY_VERSION}" ]; then
    echo "[CONFIG] rbenv global を ${RUBY_VERSION} に設定します"
    rbenv global "${RUBY_VERSION}"
    rbenv rehash
    changed=true
else
    echo "[INFO] rbenv global はすでに ${RUBY_VERSION} に設定されています"
fi

# gemのインストール処理
gem_file_path=""
for config_dir in "$@"; do
    if [ -f "$config_dir/ruby/global-gems.rb" ]; then
        gem_file_path="$config_dir/ruby/global-gems.rb"
        echo "[INFO] gem設定ファイルとして $gem_file_path を使用します"
        break # 最初に見つかったものを使用
    fi
done

if [ -z "$gem_file_path" ]; then
    echo "[INFO] global-gems.rbが見つかりません。gemのインストールをスキップします"
else
    readonly BUNDLER_VERSION="2.5.22"
    echo "[INFO] Bundlerのバージョンを確認しています... (必須: ${BUNDLER_VERSION})"
    current_version=$(bundle -v | grep -oE '[0-9]+\.[0-9]+\.[0-9]+(\.[a-zA-Z0-9]+)*' || echo "not-installed")

    if [ "$current_version" != "$BUNDLER_VERSION" ]; then
        echo "[INSTALL] Bundler v${BUNDLER_VERSION} をインストールします..."
        if gem install bundler -v "${BUNDLER_VERSION}" --no-document; then
            changed=true
        else
            echo "[ERROR] Bundler v${BUNDLER_VERSION} のインストールに失敗しました"
            exit 1
        fi
        rbenv rehash
    else
        echo "[INFO] Bundlerはすでにバージョン ${BUNDLER_VERSION} です"
    fi
fi

# 最終的な環境情報を表示
bundler_version=$(bundle -v 2>/dev/null || echo 'bundler未インストール')
echo "[INFO] Ruby環境: $(ruby -v) / $(gem -v) / ${bundler_version}"
echo "[SUCCESS] Ruby環境のセットアップが完了しました"

if [ "$changed" = true ]; then
    echo "IDEMPOTENCY_VIOLATION" >&2
fi

echo "==== Start: Ruby環境を検証中..."
# rbenvチェック
if ! command -v rbenv >/dev/null 2>&1; then
    echo "[ERROR] rbenvコマンドが見つかりません"
    exit 1
fi
# rbenvが関数としてロードされているか確認
if ! type rbenv | grep -q 'function'; then
    eval "$(rbenv init -)"
fi

echo "[SUCCESS] rbenv: $(rbenv --version)"

# Rubyバージョンチェック
if [ "$(rbenv version-name)" != "${RUBY_VERSION}" ]; then
    echo "[ERROR] Rubyのバージョンが${RUBY_VERSION}ではありません"
    exit 1
else
    echo "[SUCCESS] Ruby: $(ruby -v)"
fi

# bundlerチェック
if [ -n "$gem_file_path" ]; then
    if ! command -v bundle >/dev/null 2>&1; then
        echo "[ERROR] bundlerコマンドが見つかりません"
        exit 1
    fi

    # bundlerのバージョンが指定通りであることを確認
    current_version=$(bundle -v | grep -oE '[0-9]+\.[0-9]+\.[0-9]+(\.[a-zA-Z0-9]+)*' || echo "not-installed")

    if [ "$current_version" != "$BUNDLER_VERSION" ]; then
        echo "[ERROR] bundlerのバージョンが異なります。期待: ${BUNDLER_VERSION}, 現在: ${current_version}"
        exit 1
    else
        echo "[SUCCESS] bundler: $(bundle -v)"
    fi
fi

echo "[SUCCESS] Ruby環境の検証が完了しました"