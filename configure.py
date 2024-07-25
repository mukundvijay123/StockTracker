import json
import os
import platform
import subprocess


def detect_os():
    if os.name == 'nt':
        return 'Windows'
    elif os.name == 'posix':
        if platform.system() == 'Darwin':
            return 'macOS'
        elif platform.system() == 'Linux':
            return 'Linux'
        else:
            return 'Unix-like'
    else:
        return 'Unknown'


def set_env_var_unix(name, value, shell_rc_file):
    home_dir = os.path.expanduser("~")
    shell_rc_path = os.path.join(home_dir, shell_rc_file)
    
    # Read the current contents of the shell configuration file
    with open(shell_rc_path, 'r') as shell_rc:
        lines = shell_rc.readlines()
    
    # Check if the environment variable already exists and update it if necessary
    var_exists = False
    for i, line in enumerate(lines):
        if line.startswith(f'export {name}='):
            var_exists = True
            lines[i] = f'export {name}="{value}"\n'
            break
    
    # If the variable does not exist, append it to the shell configuration file
    if not var_exists:
        lines.append(f'\nexport {name}="{value}"\n')
    
    # Write the updated contents back to the shell configuration file
    with open(shell_rc_path, 'w') as shell_rc:
        shell_rc.writelines(lines)
    
    # Source the shell configuration file to make the change effective immediately (for the current session)
    os.system(f'source {shell_rc_path}')


def set_env_var(name, value):
    current_os = detect_os()
    
    if current_os == 'Windows':
        print("windows not yet supported")
        #subprocess.run(['setx', name, value])
    elif current_os in ['Linux', 'macOS', 'Unix-like']:
        shell_rc_file = '.bashrc'
        if current_os == 'macOS':
            shell_rc_file = '.zshrc'
        
        set_env_var_unix(name, value, shell_rc_file)
    else:
        raise Exception("Unsupported operating system")


def create_conf(folder_path):
    if os.path.exists(folder_path):
        if "STOCKS" not in os.environ or os.environ.get("STOCKS") != folder_path:
            set_env_var("STOCKS", folder_path)
        
        config_dict = {}
        config_dict["folderPath"] = folder_path
        config_fp = open(os.path.join(folder_path, "json/config.json"), "w+")
        json.dump(config_dict, config_fp, indent=4)
        config_fp.close()

        profile_dict = {}
        profile_dict["Name"] = input("Enter your name: ")
        profile_dict["ExchangeData"] = os.path.join(folder_path, "data/ExchangeData")
        profile_dict["DerivedData"] = os.path.join(folder_path, "data/DerivedData")
        profile_dict["TempData"] = os.path.join(folder_path, "data/TempData")
        profile_dict["Tickers"] = os.path.join(folder_path, "json/ticker.json")
        profile_fp = open(os.path.join(folder_path, "json/profile.json"), "w+")
        json.dump(profile_dict, profile_fp, indent=4)
        profile_fp.close()
    else:
        raise Exception("Path doesn't exist")


def get_path():
    with open("config.json", "r") as config_fp:
        config_dict = json.load(config_fp)
    return config_dict


if __name__ == "__main__":
    print(os.environ.get("STOCKS"))
    print(os.getcwd())
    create_conf(os.getcwd())
