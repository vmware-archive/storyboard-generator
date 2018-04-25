import attr
from collections import UserList, Counter


class CostExceededError(Exception):
    """Attempted to exceed the capacity of this entity with the cost of itself and its children."""


class Entity(UserList):
    """Each entity takes up space inside a panel."""
    _cost = 0
    _capacity = {}
    name = ""
    props = []

    def __init__(self, cost=None, capacity=None, **kwargs):
        super().__init__(**kwargs)
        self.props = []
        if cost is not None:
            self._cost = cost

    @property
    def cost(self):
        myself = Counter({type(self): self._cost})

        for c in self:
            if hasattr(c, "cost"):
                myself += c.cost

        return myself

    def children(self, cls):
        return [c for c in self if isinstance(c, cls)]

    def __repr__(self):
        return "{cls}(name={x.name!r}, props={x.props}, children={c})".format(cls=self.__class__.__name__, x=self, c=super().__repr__())

    def append(self, item):
        """
        If the cost would be exceeded, raise CostExceededError exception instead of appending.
        TODO: This function is not aware of Parents. If a child is added successfully, it could be modified to exceed later.
        """

        # costless objects are free!
        if hasattr(item, "cost") and hasattr(self, "_capacity"):
            proposed = item.cost + self.cost

            for concept in self._capacity:
                if concept in proposed:
                    if self._capacity[concept] < proposed[concept]:
                        raise CostExceededError(concept)

            #print("Compare:", proposed, self._capacity)
        super().append(item)


class RenderedActor(Entity):
    """A person or other speaking object. Owns its own Words. Is NOT a global construct. References art."""
    _cost = 1


class Words(Entity):
    _data = ""

    def __init__(self, value="", kind="speech", **kwargs):
        super().__init__(**kwargs)
        self._data = value
        self._kind = kind

    def __repr__(self):
        return "{cls}(kind={x._kind!r}, value={x._data!r})".format(cls=self.__class__.__name__, x=self)

    def __str__(self):
        return self._data

    @property
    def _cost(self):
        return len(self._data)


class ComicStrip(Entity):
    """A comic strip consists of a Sequence of Panels, and a collection of previously-used assets."""
    title = None

class Panel(Entity):
    """
    A Panel contains references to Actors & Text, and can be serialized to an Asset list.
    A Panel doesn't know its own position.
    TODO: Should spoken/thought text be a child of the Panel?
    """

    _capacity = {
        # Class, maximum cost
        RenderedActor: 2,
        Words: 85
    }
    narration = None
