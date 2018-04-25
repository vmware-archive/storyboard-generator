
from .parser import parse
from .scene import SceneMachine
from .render import renderComicStrip
from .render import actorAttributes


def everything(story_text):
    story = list(parse(story_text))
    scene = SceneMachine(story)
    comicstrip = scene.to_ComicStrip()
    rendered_json = renderComicStrip(comicstrip)
    return rendered_json
