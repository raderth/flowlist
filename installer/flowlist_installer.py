import os
import subprocess

REPO_URL = "https://github.com/raderth/flowlist.git"
REPO_NAME = "flowlist"
import shutil
PYTHON_EXEC = shutil.which("python") or shutil.which("python3")

def run(cmd, check=True):
    print(f"Running: {' '.join(cmd)}")
    subprocess.check_call(cmd, shell=True if os.name == 'nt' else False)

def get_venv_python():
    return os.path.join("venv", "Scripts" if os.name == "nt" else "bin", "python")

def is_installed():
    return os.path.isdir(REPO_NAME) and os.path.isdir("venv")

def clone_repo():
    if not os.path.isdir(REPO_NAME) or not os.listdir(REPO_NAME):
        print(f"Cloning {REPO_URL}...")
        run(["git", "clone", REPO_URL])
    else:
        print("Flowlist repo already exists. Skipping clone.")


def install():
    clone_repo()

    print("Creating virtual environment...")
    run([PYTHON_EXEC, "-m", "venv", "venv"])

    venv_python = get_venv_python()

    print("Installing dependencies...")
    req_file = os.path.join(REPO_NAME, "requirements.txt")
    if os.path.exists(req_file):
        run([venv_python, "-m", "pip", "install", "-r", req_file])
    else:
        run([venv_python, "-m", "pip", "install", "flask", "discord.py"])

def run_app():
    venv_python = get_venv_python()
    main_py = os.path.join(REPO_NAME, "web", "main.py")
    if not os.path.exists(main_py):
        print("main.py not found!")
        return
    print("Launching Flowlist...")
    run([venv_python, main_py])


def main():
    if not is_installed():
        print("Flowlist not found. Installing...")
        install()
    else:
        print("Flowlist already installed. Running...")
    run_app()

if __name__ == "__main__":
    main()
