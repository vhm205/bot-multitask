import re

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

def format_number(number, is_trim_last_zero = True):
    formated =  "{:,}".format(number)
    return formated if not is_trim_last_zero else formated.rstrip("0").rstrip(".")

def remove_html_tags_regex(text):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text)
