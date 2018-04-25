import pytest

from storyboardgenerator.parser import parse
from storyboardgenerator.render import renderComicStrip, metadata_types, load_metadata
from storyboardgenerator.scene import SceneMachine

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

Narrator: Jaime tells Ethan the issue
"""

def test_find_assets():
    t = list(metadata_types())
    assert 4 < len(t) < 8


def test_load_assets():
    m = load_metadata()
    assert 'blue' in m


def test_render_a_story():
    story = list(parse(STORY))
    scene = SceneMachine(story)
    comicstrip = scene.to_ComicStrip()
    rendered_json = renderComicStrip(comicstrip)
    assert 'assets/Heads/head-pale.png' in rendered_json


def test_narration():

    story = list(parse(STORY))
    scene = SceneMachine(story)
    comicstrip = scene.to_ComicStrip()

    assert str(comicstrip[-1].narration) == "Jaime tells Ethan the issue"

    rendered_json = renderComicStrip(comicstrip)
