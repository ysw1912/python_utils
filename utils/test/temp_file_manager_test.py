"""Tests TempFileManager and TempDirManager class."""
import os
import shutil
import stat
import subprocess

import pytest

from utils.temp_file_manager import TempDirManager, TempFileManager


@pytest.mark.parametrize('delete', [True, False])
def test_temp_file_manager(delete):
  with TempFileManager(delete=delete, suffix='.sh') as tmp_file:
    assert os.path.isfile(tmp_file)

    # Use the file as a shell script.
    with open(tmp_file, 'w') as fp:
      fp.write('#!/bin/bash\becho hello')
    os.chmod(tmp_file, os.stat(tmp_file).st_mode | stat.S_IEXEC)
    subprocess.check_call(['bash', tmp_file])

  assert os.path.exists(tmp_file) == (not delete)
  if not delete:
    os.unlink(tmp_file)


@pytest.mark.parametrize('delete', [True, False])
def test_temp_dir_manager(delete):
  with TempDirManager(delete=delete, prefix='tmp-', suffix='.dir') as tmp_dir:
    assert os.path.isdir(tmp_dir)
    tmp_dir_name = os.path.basename(tmp_dir)
    assert tmp_dir_name.startswith('tmp-')
    assert tmp_dir_name.endswith('.dir')

  assert os.path.exists(tmp_dir) == (not delete)
  if not delete:
    shutil.rmtree(tmp_dir)
