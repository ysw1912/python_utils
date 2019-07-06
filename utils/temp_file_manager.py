import contextlib
import os
import tempfile


@contextlib.contextmanager
def TempFileManager(delete, **kwargs):
  """Context manager that creates and deletes a named temporary file.

  Args:
    delete: Whether to delete the file out of the context.
    kwargs: Arguments that shares the same meaning as NamedTemporaryFile.
  """
  assert 'delete' not in kwargs
  tmp_file = tempfile.NamedTemporaryFile(delete=False, **kwargs)
  # Close the file so that it may be used in shell.
  tmp_file.close()
  try:
    yield tmp_file.name
  finally:
    if delete:
      os.unlink(tmp_file.name)
