import subprocess
import sys
import os
from datetime import datetime

def run_command(command):
    """コマンドを実行し、結果を返す"""
    try:
        result = subprocess.run(command, shell=True, check=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, f"エラー: {e.stderr}"

def git_status():
    """Gitの状態を確認"""
    success, output = run_command("git status")
    if success:
        print("\n=== Gitの状態 ===")
        print(output)
    return success

def git_pull():
    """リモートからプル"""
    print("\n📥 リモートからプル中...")
    success, output = run_command("git pull")
    if success:
        print("✅ プル成功")
        print(output)
    else:
        print("❌ プル失敗")
        print(output)
    return success

def git_push(commit_message=None):
    """変更をプッシュ"""
    # 変更されたファイルを確認
    success, output = run_command("git status --porcelain")
    if not success:
        print("❌ 状態の確認に失敗しました")
        return False

    if not output.strip():
        print("📝 変更されたファイルはありません")
        return True

    # 変更されたファイルを表示
    print("\n=== 変更されたファイル ===")
    print(output)

    # コミットメッセージの取得
    if not commit_message:
        commit_message = input("\n💬 コミットメッセージを入力してください: ")
        if not commit_message:
            commit_message = f"Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    # 変更をステージングに追加
    print("\n📁 変更をステージングに追加中...")
    success, output = run_command("git add .")
    if not success:
        print("❌ ステージングに失敗しました")
        print(output)
        return False

    # コミット
    print("\n💾 変更をコミット中...")
    success, output = run_command(f'git commit -m "{commit_message}"')
    if not success:
        print("❌ コミットに失敗しました")
        print(output)
        return False

    # プッシュ
    print("\n📤 リモートにプッシュ中...")
    success, output = run_command("git push")
    if success:
        print("✅ プッシュ成功")
        print(output)
    else:
        print("❌ プッシュ失敗")
        print(output)
    return success

def main():
    """メイン処理"""
    if not os.path.exists('.git'):
        print("❌ このディレクトリはGitリポジトリではありません")
        return

    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python git_manager.py pull        # リモートからプル")
        print("  python git_manager.py push        # 変更をプッシュ")
        print("  python git_manager.py status      # 状態を確認")
        return

    command = sys.argv[1].lower()
    
    if command == "pull":
        git_pull()
    elif command == "push":
        commit_message = sys.argv[2] if len(sys.argv) > 2 else None
        git_push(commit_message)
    elif command == "status":
        git_status()
    else:
        print(f"❌ 不明なコマンド: {command}")

if __name__ == "__main__":
    main() 