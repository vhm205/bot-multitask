def extract_text_from_command(command: str) -> str:
    cmd = command.split()
    text = ' '.join(cmd[1:])
    return cmd, text
