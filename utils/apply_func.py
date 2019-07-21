"""Utility functions to apply a function to a list of elements."""
import math
import threading


def _split_list_into_n_chunks(list_obj, num_chunks):
  """Splits the input list into N chunks.

  Args:
    list_obj: List-like object that supports [:] operator.
    num_chunks: Number of chunks.
  Returns:
    A generator for each split chunk.
  """
  assert isinstance(list_obj, list)
  assert isinstance(num_chunks, int)

  total_size = len(list_obj)
  chunk_size = int(math.floor(total_size / num_chunks))
  round_up_count = total_size - chunk_size * num_chunks

  start_idx = 0
  for ix in range(num_chunks):
    next_idx = start_idx + chunk_size
    if ix < round_up_count:
      next_idx += 1
    yield list_obj[start_idx:next_idx]
    start_idx = next_idx


def parallel_apply(apply_func, iterable, num_threads):
  """Parallel-applies a function to a list-like object using multi-threads.

  Args:
    apply_func: Callable to apply to each element of the list.
    iterable: An iterable object.
    num_threads: Number of threads to use.
  """
  assert callable(apply_func)
  assert isinstance(num_threads, int)

  if isinstance(iterable, list):
    list_obj = iterable
  else:
    list_obj = list(iterable)
  if not list_obj:
    return

  def _thread_target_func(each_chunk):
    """Target function for the threads."""
    for elem in each_chunk:
      apply_func(elem)

  threads = list()
  for chunk in _split_list_into_n_chunks(list_obj, num_threads):
    t = threading.Thread(target=_thread_target_func, args=(chunk,))
    threads.append(t)
  for t in threads:
    t.start()
  for t in threads:
    t.join()
