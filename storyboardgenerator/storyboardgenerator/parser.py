from .scene import LineOfLocation, LineOfAction, LineOfTitle

import re

SCENE_PATTERN = re.compile(r"(?P<name>[A-Z0-9 ]+)\b\s*(:?\s*(?P<parenthetical>\(.*\))?)?\s*$")

ACTOR_PATTERN = re.compile(r"(?P<name>\w+)(\s*->\s*(?P<target>\w+))?\s*(:\s*(?P<parenthetical>\(.*\))?\s*(?P<speech>.*))?$")

COMMENT_PATTERN = re.compile(r"//.*")

TITLE_PATTERN = re.compile(r"#\s*(?P<name>.*)$")

# name=m.groups()['firstactor'], target=m.groups()['secondactor']


class ParseError(Exception):
    """Cannot parse this line"""


def parse(string):
    """
    :param string: A newline-delimited input from the user
    """

    lines = []

    for line in string.split("\n"):

        line = line.strip()

        if line == "":
            continue

        m = COMMENT_PATTERN.match(line)
        if m:
            continue  # ignore comment lines

        m = TITLE_PATTERN.match(line)
        if m:
            yield LineOfTitle(**m.groupdict())
            continue

        m = SCENE_PATTERN.match(line)
        if m:
            yield LineOfLocation(**m.groupdict())
            continue

        m = ACTOR_PATTERN.match(line)
        if m:
            yield LineOfAction(**m.groupdict())
            continue

        raise ParseError(line)

    return lines


def to_objects(list_of_tuples):
    return []
