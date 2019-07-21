"""Tests utility functions."""
import pytest

from utils.apply_func import _split_list_into_n_chunks


@pytest.mark.parametrize('num_chunks', [3, 4])
def test_split_list_into_n_chunks(num_chunks):
  """Tests _split_list_into_n_chunks function."""
  list_obj = [1, 2, 3, 4, 5, 6, 7]
  actual_chunks = []
  for chunk in _split_list_into_n_chunks(list_obj, num_chunks=num_chunks):
    actual_chunks.append(chunk)
  if num_chunks == 3:
    assert actual_chunks == [[1, 2, 3], [4, 5], [6, 7]]
  elif num_chunks == 4:
    assert actual_chunks == [[1, 2], [3, 4], [5, 6], [7]]
