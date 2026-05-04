import subprocess

def run_git():
    with open('git_output.txt', 'w') as f:
        try:
            status = subprocess.check_output(['git', 'status'], text=True)
            f.write("--- STATUS ---\n")
            f.write(status)
            diff = subprocess.check_output(['git', 'diff'], text=True)
            f.write("\n--- DIFF ---\n")
            f.write(diff)
        except Exception as e:
            f.write(str(e))

if __name__ == '__main__':
    run_git()
