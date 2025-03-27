

def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    print(lines)
    for line in lines:
        if line.startswith("# "):
            return line.strip("#").lstrip()
    return Exception("There is no header!")