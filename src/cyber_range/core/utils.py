from __future__ import annotations

from typing import Iterable, Sequence, TypeVar

T = TypeVar("T")


def safe_choice(seq: Sequence[T] | Iterable[T], rnd) -> T:
    """Random choice using the model's RNG; converts iterables to tuple once.

    Avoids importing random globally, relies on provided RNG with .choice.
    """
    if not isinstance(seq, Sequence):
        seq = tuple(seq)
    return rnd.choice(seq)

