import re


# test = """
# // variables
# a = "Hello, "
# b = world!
# c=100
#
# /*
# prompt with variables
# d="This is a test."
# e=3.14
# d and e will not work.
# */
# // f = true /* not work either */
# /*
# another comment but ok */
# prompt = {
# {a}{b} /* not work */ /*still not work*/
# // line comment
# generate an image of {c} cat sitting on a mat.
# }
# prompt {
# the second prompt will not work.
# }
# """

_VAR_NAME_REGEX = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
_PROMPT_START_RE = re.compile(r'\bprompt\b', re.ASCII)
_PLACEHOLDER_RE = re.compile(r'\{([A-Za-z_][A-Za-z0-9_]*)\}', re.ASCII)

RESERVED_VARIABLES = ["prompt"]


def _is_prompt_start(line: str) -> bool:
    # Accept: prompt={, prompt = {, prompt= {, prompt {
    # Reject: prompt=content, promptly=1, prompt_text=...
    s = line.strip()
    if not s.startswith("prompt"):
        return False

    # must have "{" after prompt (possibly with spaces and '=')
    # and "prompt" must be a standalone token prefix
    # e.g. "promptly" should not match
    if len(s) > 6 and (s[6].isalnum() or s[6] == "_"):
        return False
    return "{" in s


def remove_comments(text: str) -> str:
    lines = text.splitlines()
    result_lines = []
    in_block = False

    for raw_line in lines:
        line = raw_line

        # handle block comments
        i = 0
        out = ""

        while i < len(line):
            if not in_block:
                start = line.find("/*", i)
                if start == -1:
                    out += line[i:]
                    break
                out += line[i:start]
                i = start + 2
                in_block = True
            else:
                end = line.find("*/", i)
                if end == -1:
                    i = len(line)
                    break
                i = end + 2
                in_block = False

        cleaned = out.strip()

        # handle line start //
        if cleaned.lstrip().startswith("//"):
            continue

        if cleaned:
            result_lines.append(cleaned)

    return "\n".join(result_lines)


def get_variables(comments_removed_prompt_code: str) -> dict:
    variables: dict[str, str] = {}

    for raw_line in comments_removed_prompt_code.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        # stop at first prompt block
        if _is_prompt_start(line):
            break

        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if not key or not _VAR_NAME_REGEX.match(key):
            continue

        # Optional: disallow reserved keywords
        if key in RESERVED_VARIABLES:
            continue

        # strip surrounding quotes
        if len(value) >= 2 and ((value[0] == value[-1] == '"') or (value[0] == value[-1] == "'")):
            value = value[1:-1]

        variables[key] = value

    return variables


def get_raw_prompt(comments_removed_prompt_code: str) -> str:
    # get first prompt block content
    # prompt format: prompt = { ... } or prompt { ... }
    s = comments_removed_prompt_code
    prompt_start = _PROMPT_START_RE.search(s)

    if not prompt_start:
        return ""

    i = prompt_start.end()

    # skip whitespace
    n = len(s)
    while i < n and s[i].isspace():
        i += 1

    # optional '='
    if i < n and s[i] == '=':
        i += 1
        while i < n and s[i].isspace():
            i += 1

    # expect '{'
    if i >= n or s[i] != '{':
        return ""

    # expect '}' to close
    i += 1
    content_start = i
    depth = 1
    while i < n:
        content_char = s[i]
        if content_char == '{':
            depth += 1
        elif content_char == '}':
            depth -= 1
            if depth == 0:
                return s[content_start:i].strip()
        i += 1

    # if unclosed
    return ""


def get_prompt_output(raw_prompt: str, variables: dict[str, str]) -> str:
    def replace_placeholder(match: re.Match) -> str:
        var_name = match.group(1)
        return variables.get(var_name, match.group(0))

    return _PLACEHOLDER_RE.sub(replace_placeholder, raw_prompt)


# for test

# def __main__():
#
#     comments_removed_prompt_code = remove_comments(test)
#     print(comments_removed_prompt_code)
#
#     variables = get_variables(comments_removed_prompt_code)
#     print(variables)
#
#     raw_prompt = get_raw_prompt(comments_removed_prompt_code)
#     print(f"Raw prompt:\n{raw_prompt}")
#
#     prompt_output = get_prompt_output(raw_prompt, variables)
#     print(f"Final prompt:\n{prompt_output}")
#
#
# if __name__ == "__main__":
#     __main__()
