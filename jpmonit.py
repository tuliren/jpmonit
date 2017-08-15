import subprocess
import re

class Jpmonit:
  deadlock_pattern = re.compile(".*Found.*deadlock.*")

  def __init__(self, logger):
    self.logger = logger

  def check_process(self, path):
    self.logger.debug("Check process in %s" % path)

    if not path:
      return JpmonitResult(False, "Missing parameter pidfile")

    try:
      pid = self.get_process_id(path)
    except IOError:
      return JpmonitResult(False, "Invalid pid file path: %s" % path)

    return self.check_process(pid)

  def get_process_id(self, path):
    with open(path, 'r') as file:
      return int(file.readline())

  def check_process(self, pid):
    if self.check_deadlock(pid):
      return JpmonitResult(false, "Process %d has deadlock" % pid)
    return JpmonitResult(True)

  def check_deadlock(self, pid):
    has_deadlock = False
    args = ['jstack', str(pid)]
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in p.stdout.readlines():
      if Jpmonit.deadlock_pattern.match(line.strip()):
        has_deadlock = True
        break
    p.wait()
    return has_deadlock

class JpmonitResult:
  def __init__(self, valid, message = None):
    self.valid = valid
    self.message = message

  def is_valid(self):
    return self.valid

  def get_message(self):
    return self.message
