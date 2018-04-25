

from storyboardgenerator.comicstrip import Panel, Entity, Words

def test_run_out_of_space():
    a1 = Entity()


def test_word_to_string():
    w = Words("foo")

    assert str(w) == "foo"
    assert "Words" in repr(w)
