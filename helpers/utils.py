def extract_text_from_command(command: str) -> str:
    cmd = command.split()
    text = ' '.join(cmd[1:])
    return cmd, text

def extract_option_from_command(command: str):
    cmd = command.split()
    cmd.pop(0)
    option = {}

    for opt in cmd:
        key, value = opt.split('=')
        option[key] = value

    return option
