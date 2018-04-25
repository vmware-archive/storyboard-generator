import pytest
from storyboardgenerator.comicstrip import Entity, Panel, RenderedActor, CostExceededError, Words


def test_single_cost():
    e1 = Entity(cost=3)

    cost = e1.cost

    assert len(cost) == 1

    for _ in cost:
        assert cost[_] == 3


def test_recursive_cost():

    e1 = Entity(cost=1)
    e2 = Entity(cost=2)
    e3 = Entity(cost=3)

    e1.append(e2)
    e1.append(e3)

    cost = e1.cost

    assert len(cost) == 1

    for _ in cost:
        assert cost[_] == 6


    e2.append(e3)

    cost = e1.cost

    assert len(cost) == 1

    for _ in cost:
        assert cost[_] == 9

def test_cost_exceeded():
    panel = Panel()

    e2 = RenderedActor()
    e3 = RenderedActor()

    panel.append(e2)
    panel.append(e3)

    print(panel)

    with pytest.raises(CostExceededError) as excinfo:
        e4 = RenderedActor()
        panel.append(e4)

def test_cost_exceeded_recursive():
    shortwords = Words(value="These are some words that fit.")
    longwords = Words(value="A very long sequence of words that will push above the capacity of a single panel and force an exception to be raised.")

    panel = Panel()
    actor = RenderedActor()

    actor.append(shortwords)
    panel.append(actor)
    print(panel)

    # this will fail
    panel = Panel()
    actor = RenderedActor()

    with pytest.raises(CostExceededError) as excinfo:
        actor.append(shortwords)
        actor.append(longwords)
        panel.append(actor)
        print(panel)
