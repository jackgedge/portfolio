import os
import sys

ENV_NAME = 'portfolio'
ENV_FILE = '.env'

def check_conda():
# Check conda installed
    exit_status: int = os.system("command -v conda >/dev/null 2>&1")

    # Raise error if not installed
    if exit_status != 0:
        raise RuntimeError("Conda is not installed or is not on PATH. Please install conda or add it to your PATH.")

    # Script continues only if conda is found
    print("Conda is available!")

def conda_env_exists(env_name: str) -> bool:
    output: str = os.popen("conda env list 2>/dev/null").read()

    for line in output.splitlines():
        parts: list[str] = line.split()
        if parts and parts[0] == env_name:
            return True

    return False

def create_conda_env(dry_run: bool = False):
    
    cmd = "conda env create -f environment.yml"
    if dry_run:
        cmd += " --dry-run"

    # Create conda env from environment.yml
    create_status: int = os.system(cmd)

    if create_status != 0:
        raise RuntimeError(f"Conda command failed: {cmd}")

    print("Conda environment created successfully!")

    if dry_run:
        print("Dry-run succeeded; no environment was created.")
    else:
        print("Conda environment was created successfully.")

def create_dotenv(dry_run: bool = False):
    file_name = ".env"

    required_vars = [
        "WEBDAV_HOSTNAME",
        "WEBDAV_LOGIN",
        "WEBDAV_PASSWORD",
        "PORTFOLIO_DIR",
    ]

    existing_values = {}

    # Load existing .env if present
    if os.path.exists(file_name) and os.path.isfile(file_name):
        print(f"{file_name} already exists.")
        with open(file_name, "r") as f:
            content = f.read()

        # Parse existing values
        for line in content.splitlines():
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key in required_vars:
                existing_values[key] = value

    # Find missing or empty vars
    missing_or_empty = [
        var for var in required_vars
        if var not in existing_values or existing_values[var] == ""
    ]

    if not missing_or_empty:
        print("All required vars are populated; nothing to prompt.")
        return

    print("Prompting for missing/empty vars:")
    for var in missing_or_empty:
        value = input(f"{var}: ").strip()
        existing_values[var] = value

    # Build final content (all required vars, in order)
    file_content = "\n".join(
        f'{var}="{existing_values.get(var, "")}"'
        for var in required_vars
    ) + "\n"

    if dry_run:
        print("[dry-run] Would write .env with:")
        print(file_content)
        return

    with open(file_name, "w") as f:
        f.write(file_content)

    print(f"{file_name} updated successfully.")

def create_systemd_service(systemd: bool = False):
    file_name = "portfolio.service"
    
    service_file_exists: bool = os.path.exists(file_name) and os.path.isfile()
    
    if service_file_exists:
        response: str = input(f"{file_name} exists. Create new one? [N]/y: ") or 'n'
        if response.lower() in ('y', 'yes'):
            #TODO
            pass
        else:
            pass
            
if __name__ == "__main__":
    dry_run: bool = "--dry-run" in sys.argv or "-n" in sys.argv
    systemd: bool = "--systemd" in sys.argv or "-d" in sys.argv

    check_conda()

    if not conda_env_exists(ENV_NAME):
        create_conda_env(dry_run=dry_run)
    else:
        print(f"{ENV_NAME} already exists.")

    create_dotenv(dry_run=dry_run)