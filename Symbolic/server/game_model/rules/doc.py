def content(line: str):
    import re
    return re.search(r"\(.*\)", line).group()[1:-1]


rules = open("rules.txt")

documentation = open("ruledoc.md", "w")
documentation.write("# Rules Symbolic Level\n")

for doc_line in filter(lambda x: x.startswith("//"), rules.readlines()):
    doc_line = doc_line[2:].strip()
    if doc_line.startswith("@rule"):
        documentation.write(
            "## {}".format(content(doc_line).capitalize())
        )
    elif doc_line.startswith("@description"):
        documentation.write(
            content(doc_line).capitalize()
        )
    elif doc_line.startswith("@action"):
        actions = content(doc_line).split(",")
        documentation.write("### Actions\n")
        for i, action in enumerate(actions):
            action = action.strip()
            documentation.write("- {}".format(action))

            if i < len(actions) - 1:
                documentation.write("\n")

    elif doc_line.startswith("@returns"):
        documentation.write(
            "```javascript\n{}```".format(content(doc_line).replace(",", ",\n"))
        )
    else:
        pass

    documentation.write('\n')
