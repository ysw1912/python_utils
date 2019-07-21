"""Tests LockProtector class."""
import time

import pytest

from utils.apply_func import parallel_apply
from utils.lock_protector import LockProtector


class _TestObject(object):
  """Object used for testing."""

  def __init__(self):
    """Constructor."""
    self.counter = 0

  def increment(self):
    """Emulates a critical section."""
    current_value = self.counter
    time.sleep(0.01)
    current_value += 1
    self.counter = current_value


@pytest.fixture()
def test_obj():
  """Sets up pytest fixture."""
  return _TestObject()


@pytest.mark.parametrize('parallelism', [10, 50, 100])
def test_lock_protector(test_obj, parallelism):
  """Tests LockProtector class."""
  protector = LockProtector(test_obj)

  def thread_func(_):
    with protector.lock() as obj:
      assert isinstance(obj, _TestObject)
      obj.increment()

  parallel_apply(
      apply_func=thread_func,
      iterable=range(parallelism),
      num_threads=parallelism)
  assert test_obj.counter == parallelism


def test_lock_acquisition_order(test_obj):
  """Tests lock acquisition order."""
  protector1 = LockProtector(test_obj)
  protector2 = LockProtector(test_obj)
  protector3 = LockProtector(test_obj)
  protector2.add_inner_protector(protector1)
  protector3.add_inner_protector(protector2)

  with protector3.lock():
    with protector2.lock():
      with protector1.lock():
        pass

  with pytest.raises(RuntimeError):
    with protector1.lock():
      with protector2.lock():
        pass
  with pytest.raises(RuntimeError):
    with protector1.lock():
      with protector3.lock():
        pass
  with pytest.raises(RuntimeError):
    with protector2.lock():
      with protector3.lock():
        pass


def test_inner_lock_circularity(test_obj):
  """Tests inner lock circularity."""
  protector1 = LockProtector(test_obj)
  protector2 = LockProtector(test_obj)
  protector3 = LockProtector(test_obj)
  protector2.add_inner_protector(protector1)
  protector3.add_inner_protector(protector2)
  protector1.add_inner_protector(protector3)

  for p in [protector1, protector2, protector3]:
    with pytest.raises(RuntimeError):
      with p.lock():
        pass


def test_multi_threads_lock(test_obj):
  """Tests lock in multi threads."""
  protector1 = LockProtector(test_obj)
  protector2 = LockProtector(test_obj)
  protector2.add_inner_protector(protector1)

  def _thread1():
    """Thread1 acquires inner protector1."""
    time.sleep(0.5)
    with protector1.lock():
      time.sleep(1)

  def _thread2():
    """It is okay for thread2 to acquire protector2 while protector1 is held by
    thread1."""
    while not protector1.get_lock().locked():
      time.sleep(0.1)
    with protector2.lock():
      with protector1.lock():
        pass

  thread_funcs = [_thread1, _thread2]
  parallel_apply(lambda x: x(), thread_funcs, num_threads=len(thread_funcs))
