"""
Tests for core_rws module.

Checks under several circumstances whether the result of CoreRWS is a weakly sum
free partition and whether the length of this partition matches the expected
value.
"""


from core_rws import CoreRWS
from utils import is_weakly_sum_free_partition


ANSWERS = [2, 7, 21, 61, 180, 536, 1593, 4733]


def test_core_rws_equal():
    """
    Checks whether CoreRWS behaves properly when the aim is equal to the
    greatest value it can reach.
    """
    for k, aim in enumerate(ANSWERS):
        core_rws = CoreRWS(k + 1, aim)
        partition = core_rws()
        assert is_weakly_sum_free_partition(partition)
        assert len(core_rws) == aim


def test_core_rws_greater():
    """
    Checks whether CoreRWS behaves properly when the aim is greater than the
    greatest value it can reach.
    """
    for k, aim in enumerate(ANSWERS):
        core_rws = CoreRWS(k + 1)
        partition = core_rws()
        assert is_weakly_sum_free_partition(partition)
        assert len(core_rws) == aim


def test_core_rws_less():
    """
    Checks whether CoreRWS behaves properly when the aim is less than the
    greatest value it can reach.
    """
    for k, aim in enumerate(ANSWERS):
        aim = aim - aim * k // 8
        core_rws = CoreRWS(k + 1, aim)
        partition = core_rws()
        assert is_weakly_sum_free_partition(partition)
        assert len(core_rws) == aim
