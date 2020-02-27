import re


def setup():
    BASE_COMMANDS = [
        ("inbox", ""),
        ("outbox", ""),
        ("copyfrom", "{}"),
        ("copyto", "{}"),
        ("add", "{}"),
        ("sub", "{}"),
        ("bumpup", "{}"),
        ("bumpdn", "{}"),
        ("jump", "{}"),
        ("jumpz", "{}"),
        ("jumpn", "{}"),
    ]
    max_len = max(len(c[0]) for c in BASE_COMMANDS) + 1
    base_commands = {
        command: "    " + command.upper() + " " * (max_len - len(command)) + arg
        for command, arg in BASE_COMMANDS
    }
    base_commands.update({"label": "{}:"})

    additional_commands = {
        "b>": (("inbox", ""),),
        "b<": (("outbox", ""),),
        "c>": (("copyto", "{0}"),),
        "c<": (("copyfrom", "{0}"),),
        "+": (("add", "{0}"),),
        "-": (("sub", "{0}"),),
        "u>": (("add", "{0}"),),
        "u<": (("sub", "{0}"),),
        "::": (("label", "{0}"),),
        "~:": (("jump", "{0}"),),
        "-:": (("jumpn", "{0}"),),
        "0:": (("jumpz", "{0}"),),
        "=>": (("jump", "{0}"),),
        "->": (("jumpn", "{0}"),),
        "0>": (("jumpz", "{0}"),),
        "place": (("inbox", ""), ("copyto", "{0}"),),
        "take": (("copyfrom", "{0}"), ("outbox", ""),),
        "through": (("inbox", ""), ("outbox", ""),),
        "gt": (("copyfrom", "{0}"), ("sub", "{1}"),),
        "lt": (("copyfrom", "{1}"), ("sub", "{0}"),),
        "move": (("copyfrom", "{0}"), ("copyto", "{1}"),),
        "swap": (
            ("copyfrom", "{0}"),
            ("copyto", "{2}"),
            ("copyfrom", "{1}"),
            ("copyto", "{0}"),
            ("copyfrom", "{2}"),
            ("copyto", "{1}"),
        ),
        "i>": (("inbox", ""), ("copyto", "{0}"),),
        "i<": (("copyfrom", "{0}"), ("outbox", ""),),
        ">>": (("inbox", ""), ("outbox", ""),),
        ">": (("copyfrom", "{0}"), ("sub", "{1}"),),
        "<": (("copyfrom", "{1}"), ("sub", "{0}"),),
        "~>": (("copyfrom", "{0}"), ("copyto", "{1}"),),
        "<>": (
            ("copyfrom", "{0}"),
            ("copyto", "{2}"),
            ("copyfrom", "{1}"),
            ("copyto", "{0}"),
            ("copyfrom", "{2}"),
            ("copyto", "{1}"),
        ),
    }
    return base_commands, additional_commands


COMMANDS, ADDITIONAL_COMMANDS = setup()


def read_commands(program):
    commands = []
    for line in program:
        line = line.strip()
        if not line or line.startswith(("#", "//", "--")):
            continue
        match = re.match(r"(.+):$", line)
        if match:
            commands.append(("label", (match.groups(1))))
            continue
        name, *args = line.split()
        commands.append((name.lower(), args))
    return commands


def to_hrm(commands):
    hrm_commands = []
    for name, args in commands:
        additional_commands = ADDITIONAL_COMMANDS.get(name, None)
        if additional_commands is None:
            hrm_commands.append((name, (args[:1] or [None])[0]))
            continue
        for command, value in additional_commands:
            hrm_commands.append((command, value.format(*args)))
    return hrm_commands


def format_hrm(commands):
    return "\n".join(COMMANDS[name].format(arg) for name, arg in commands)


while True:
    level = input("level: ")
    try:
        f = open("./levels/{}".format(level))
    except FileNotFoundError:
        print("File doesn't exist")
        continue
    with f:
        mhrm_commands = read_commands(f)
    hrm_commands = to_hrm(mhrm_commands)
    print("\n\n{}\n\n".format(format_hrm(hrm_commands)))
