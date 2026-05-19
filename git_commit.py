import subprocess

try:
    # 1. Stage all changes
    subprocess.run(["git", "add", "."], check=True)
    print("Success: Staged all changes.")
    
    # 2. Commit changes
    commit_message = "Fix: responsive control layout, fallback placeholder asset, and supply history date pagination"
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    print(f"Success: Committed with message: '{commit_message}'")
    
    # 3. Inform about push (optional)
    print("\nIf you want to push to the remote repository, run: git push")
except subprocess.CalledProcessError as e:
    print(f"Error during Git execution: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
