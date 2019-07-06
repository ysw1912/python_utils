import os
import stat
import subprocess

import pytest

from utils.temp_file_manager import TempFileManager


@pytest.mark.parametrize('delete', [True, False])
def test_temp_file_manager(delete):
  with TempFileManager(delete=delete, suffix='.sh') as tmp_file:
    assert os.path.isfile(tmp_file)

    # Use the file as a shell script.
    # with open(tmp_file, 'w') as fp:
    #   fp.write('#!/bin/bash\becho hello')
    # os.chmod(tmp_file, os.stat(tmp_file).st_mode | stat.S_IEXEC)
    # subprocess.check_call([tmp_file])

  assert os.path.exists(tmp_file) == (not delete)
  if not delete:
    os.unlink(tmp_file)
