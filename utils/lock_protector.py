"""Wraps an object with lock protection."""
from contextlib import contextmanager
import threading


class LockProtector(object):
  """Wraps an object with lock protection.

  Supports a limit to lock acquisition order by adding references to "inner"
   LockProtector instances.
  Checks that the inner locks should not be acquired prior to this protector
   by the same thread.
  The check is recursive and not allow circular inner relationship.
  """
  def __init__(self, obj):
    """Constructor.

    Args:
      obj: Object to be protected by lock.
    """
    assert obj is not None
    self._obj = obj
    self._lock = threading.Lock()
    self._owner_thread = None
    self._inner_protectors = set()

  def get_lock(self):
    """Returns the lock object."""
    return self._lock

  @contextmanager
  def lock(self):
    """Context manager that yield the object protected by lock."""
    self._check_inner_protectors(set())
    self._lock.acquire()
    self._owner_thread = threading.current_thread()
    try:
      yield self._obj
    finally:
      self._owner_thread = None
      self._lock.release()

  def add_inner_protector(self, inner):
    """Adds reference to an inner lock protector."""
    assert isinstance(inner, LockProtector)
    self._inner_protectors.add(inner)

  def _check_inner_protectors(self, outer_protectors):
    """Checks that none of the inner protectors are locked.

    Args:
      outer_protectors: Set of outer protectors used to avoid circularity.
    """
    assert isinstance(outer_protectors, set)
    if self in outer_protectors:
      raise RuntimeError('Circular inner protector detected')
    outer_protectors.add(self)
    for inner in self._inner_protectors:
      assert isinstance(inner, LockProtector)
      inner._check_inner_protectors(outer_protectors)
      if inner._lock.locked() and (
         inner._owner_thread == threading.current_thread()):
        raise RuntimeError(
            'An inner protector {} is already locked by current thread'.format(
                inner))
    outer_protectors.remove(self)
