import pytest

from storyboardgenerator.parser import parse, ParseError, to_objects, SCENE_PATTERN, ACTOR_PATTERN, TITLE_PATTERN
from storyboardgenerator.scene import SceneMachine, parse_paranthetical

STORY = """
# Title

// comments

ROOM 1 (computer)
Jamie: (blue shirt)
Sign: App Owner: Jaime
Narrator: Ethan looks up the villain VM's owner, Jaime.

ROOM 2: (stuff)
Ethan: (purple shirt,anxious)
Ethan -> Jaime: Here's the situation...
Narrator: Ethan calls Jamie and explains the situation.

Jaime -> Ethan: It's okay to power off the VM.
Narrator: Jaime tells Ethan the issue is being fixed and it's ok to restart the VM as a temporary workaround.
Ethan: (happy) This is going to be easy.


SCENE
Character: (property)
Character: thought text
Character -> Character: (property,emotion) speech text


ROOM 1
Jaime: (blue shirt)
ROOM 2
Ethan: (purple shirt)
Jaime -> Ethan: (phone) It's ok to power off the VM.

Ethan: That was easy  (thought bubble)
Ethan -> Ethan:  What was I thinking?   (speech bubble)

Narrator: Jaime tells Ethan the issue  (renders outside)
Narrator -> Jaime: Jaime is the application owner  (renders inside)
"""

@pytest.mark.parametrize("victim,locationname,properties", [
    ("ROOM", "ROOM", []),
    ("ROOM 1 (computer)", "ROOM 1", ["computer"]),
    ("ROOM 2", "ROOM 2", []),
    ("ROOM 3: (stuff)", "ROOM 3", ["stuff"]),
    ("ROOM 4: (stuff space)", "ROOM 4", ["stuff space"]),
    ("ROOM 5: (stuff, morestuff)", "ROOM 5", ["stuff", "morestuff"]),
])
def test_scene_pattern(victim, locationname, properties):
    m = SCENE_PATTERN.match(victim)

    g = m.groupdict()

    assert locationname == g['name']

    props = parse_paranthetical(g['parenthetical'])
    assert properties == props


@pytest.mark.parametrize("victim,name,properties,words", [
    ("Character: (property)", "Character", ['property'], "words"),
    ("Character: thought text", "Character", [], "words"),
    ("Character -> Target: (trailing) speech text", "Character", ["trailing"], "words"),
    ("Character -> Target: (comma,emotion) speech text", "Character", ["comma", "emotion"], "words"),
])
def test_action_pattern(victim, name, properties, words):
    m = ACTOR_PATTERN.match(victim)

    g = m.groupdict()

    assert name == g['name']


    props = parse_paranthetical(g['parenthetical'])
    print(g, props)

    assert properties == props


@pytest.mark.parametrize("victim,name", [
    ("# Title", "Title"),
])
def test_title_pattern(victim, name):
    m = TITLE_PATTERN.match(victim)

    g = m.groupdict()

    assert name == g['name']


def test_story_txt():
    try:
        story = list(parse(STORY))

    except ParseError as pe:
        print(str(pe))
        raise

    assert len(story) == 25
    print(story)

def test_story_txt_to_Scene():
    story = list(parse(STORY))

    scene = SceneMachine(story).to_ComicStrip()

    from pprint import pprint
    pprint(scene)

    print(str(scene))
    assert 'Jamie' in str(scene)

    assert scene.name == "Title"
