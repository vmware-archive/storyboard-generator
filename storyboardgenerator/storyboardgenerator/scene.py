

import attr
import itertools
from .comicstrip import ComicStrip, Panel, RenderedActor, Words, CostExceededError


@attr.s
class LineOfEntity(object):
    name = attr.ib()
    parenthetical = attr.ib(default="")


@attr.s
class LineOfAction(LineOfEntity):
    """An actor can talk, and has a location"""
    target = attr.ib(default=None)
    speech = attr.ib(default="")
    def __init__(self, target, **kwargs):
        if target == "":
            target = None
        super().__init__(target=target, **kwargs)

class LineOfTitle(LineOfEntity):
    """Title of the strip"""

@attr.s
class LineOfLocation(LineOfEntity):
    """A location, has a name"""
    properties = attr.ib(default=[])


# A ConceptualEntity is a mutable bag of properties. Actors have Locations.
@attr.s
class ConceptualEntity(object):
    name = attr.ib()
    properties = attr.ib(default=[])


@attr.s
class Actor(ConceptualEntity):
    """An actor can talk, and has a starting location"""
    starting_location = attr.ib(default=None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_location = self.starting_location


@attr.s
class Location(ConceptualEntity):
    """A Location has no special attributes"""


def parse_paranthetical(paran):
    """
    :param: A paranthetical-string is a comma-delimited list of barewords: (foo,bar)
    :return: A list of barewords
    """
    if paran is None:
        return []
    return [s.strip().lower() for s in paran[1:-1].split(",")]


class SceneMachine(object):
    @property
    def first_location(self):
        for e in self.lines:
            if type(e) == LineOfLocation:
                return self.locations[e.name]

    def __init__(self, lines):
        self.actors = {}  # keyed by actor name
        self.locations = {}
        self.lines = lines

        # Locations
        for e in self.lines:
            if type(e) == LineOfLocation:
                if e.name not in self.locations:
                    self.locations[e.name] = e

        # Left Side actors
        most_recently_seen_location = self.first_location
        for e in self.lines:
            if type(e) == LineOfLocation:
                most_recently_seen_location = e
            elif type(e) == LineOfAction:
                actorname = e.name
                if actorname not in self.actors:
                    self.actors[actorname] = Actor(name=actorname, starting_location=most_recently_seen_location, properties=parse_paranthetical(e.parenthetical))

        # Right Side actors that have been mentioned, but never given properties
        most_recently_seen_location = self.first_location
        for e in self.lines:
            if type(e) == LineOfLocation:
                most_recently_seen_location = e
            elif type(e) == LineOfAction:
                actorname = e.target
                if actorname and actorname not in self.actors:
                    self.actors[actorname] = Actor(name=actorname, starting_location=most_recently_seen_location, properties=['startmentioned'])

    def to_ComicStrip(self):
        """
        Iterate over all input lines, and construct:
         * a list of all Actors and Locations in comic strip, with their Initial States
         * a list of all ChangeEvents that occur in the comic strip, citing their Actors and Locations

        Emit:
         * a comicstrip.ComicStrip tree, with discrete objects
        """

        comicstrip = ComicStrip()

        current_panel = Panel()
        sticky_location = self.first_location
        actions = []

        # Render speech objects with real object references

        # Iterate over every line of input, and accumulate changes
        for e in self.lines:
            new_prop_bag = parse_paranthetical(e.parenthetical)

            if type(e) == LineOfTitle:
                comicstrip.name = e.name
                continue

            # The Location changed. We need a new panel. Seal off this one, and start a new one.
            if type(e) == LineOfLocation:
                comicstrip.append(current_panel)

                current_panel = Panel()
                sticky_location = self.locations[e.name]
                if new_prop_bag:
                    sticky_location.properties = new_prop_bag.copy()
                current_panel.props = sticky_location.properties.copy()
                continue

            # Narration for this panel
            if type(e) == LineOfAction and e.name == "Narrator":
                # Are they talking? Include their words
                if e.speech:
                    words = Words(value=e.speech)
                    if not e.target:
                        words._kind = "thought"
                    current_panel.narration = words

                continue

            # An Action is happening. We need to add the speaker to this Panel.
            if type(e) == LineOfAction:
                actorname = e.name

                changing_actor = self.actors[actorname]

                if new_prop_bag:
                    changing_actor.properties = new_prop_bag.copy()

                new_speaker = RenderedActor()
                new_speaker.name = actorname

                print(changing_actor)
                new_speaker.props = changing_actor.properties.copy()

                # Are they talking? Include their words
                if e.speech:
                    words = Words(value=e.speech)
                    if not e.target:
                        words._kind = "thought"
                    new_speaker.append(words)

                try:
                    current_panel.append(new_speaker)
                except CostExceededError:
                    # We want out of space inside this panel. Make a new panel.
                    comicstrip.append(current_panel)
                    current_panel = Panel()
                    current_panel.props = sticky_location.properties.copy()


                # TODO Try to put the listener in this panel?

        comicstrip.append(current_panel)

        return comicstrip


MAX_TEXT_LENGTH_IN_PANEL = len("Must be a virtual infrastructure issue. Let me route this to the virtualization team.")
def text_fits_in_one_panel(textlist):
    accumulator = 0
    for t in textlist:
        accumulator += len(t)

    return accumulator <= MAX_TEXT_LENGTH_IN_PANEL
