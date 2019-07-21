from contextlib import contextmanager
import os
import shutil
import tempfile


@contextmanager
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


@contextmanager
def TempDirManager(delete, **kwargs):
  """Context manager that creates and deletes a named temporary directory.

  Args:
    delete: Whether to delete the directory out of the context.
    kwargs: Arguments that shares the same meaning as mkdtemp.
  """
  name = tempfile.mkdtemp(**kwargs)
  try:
    yield name
  finally:
    if delete:
      shutil.rmtree(name)
