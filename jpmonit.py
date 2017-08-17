import re
import subprocess


class Jpmonit:
  deadlock_pattern = re.compile(".*Found.*deadlock.*")

  def __init__(self, logger):
    self.logger = logger

  def check_all(self, process_name=None):
    """
    Check Java processes whose names match to the specified process_name.
    When process_name is None, check all running processes.
    """
    results = []
    pids = self.get_all_pids(process_name=process_name)
    for pid in pids:
      result = self.check_pid(pid)
      self.logger.debug("PID %d: %s" % (pid, result))
      results.append(result)
    return JpmonitResult.from_collection(results)

  def check_process(self, process_name):
    """
    Check Java processes with the specific process name.
    """
    if not process_name:
      return JpmonitResult.invalid("Invalid process name: " + process_name)
    return self.check_all(process_name=process_name)

  def check_pid(self, pid):
    """
    Check a Java process with the specified pid.
    """
    if not pid:
      return JpmonitResult.invalid("Invalid pid: " + str(id))
    return self.run_checks(pid)

  def check_pidfile(self, pid_file_path):
    """
    Check a Java process whose pid is specified in the pid file.
    """
    if not pid_file_path:
      return JpmonitResult.invalid("Invalid pid file path: " + pid_file_path)

    try:
      pid = self.get_pid_from_pidfile(pid_file_path)
    except IOError:
      return JpmonitResult.invalid("Invalid pid file path: " + pid_file_path)
    return self.run_checks(pid)

  def get_pid_from_pidfile(self, pidfile):
    """
    Get the pid from a pid file. Only one pid is expected per file.
    """
    with open(pidfile, "r") as file:
      return int(file.readline())

  def get_all_pids(self, process_name=None):
    """
    Get pids of running Java processes that match process_name.
    When process_name is None, get all pids.
    """
    p = subprocess.Popen(["jps", "-ml"], stdout=subprocess.PIPE)
    p = subprocess.Popen(["grep", "-v", "sun.tools.jps"], stdin=p.stdout, stdout=subprocess.PIPE)
    if process_name:
      p = subprocess.Popen(["grep", process_name], stdin=p.stdout, stdout=subprocess.PIPE)
    pids = []
    for line in p.stdout.readlines():
      pid = line.split(" ")[0]
      pids.append(int(pid))
    try:
      p.wait()
    except Exception as exception:
      self.logger.error("Failed to run jps: " + exception)
      return pids
    return pids

  def run_checks(self, pid):
    """
    Run all checks for a Java process with the specified pid.
    """
    self.logger.debug("Checking pid " + str(pid))

    int_pid = int(pid)
    pids = self.get_all_pids()
    if int_pid not in pids:
      self.logger.debug("Existing pids: " + ", ".join(map(lambda p: str(p), pids)))
      return JpmonitResult.invalid("No Java process with PID " + str(int_pid) + " can be found")

    if self.check_deadlock(int_pid):
      return JpmonitResult.invalid("Process " + str(int_pid) + " has deadlock")

    return JpmonitResult(True)

  def check_deadlock(self, pid):
    """
    Check deadlock by running jstack.
    """
    has_deadlock = False
    p = subprocess.Popen(["jstack", str(pid)], stdout=subprocess.PIPE)
    for line in p.stdout.readlines():
      if Jpmonit.deadlock_pattern.match(line.strip()):
        has_deadlock = True
        break

    try:
      p.wait()
    except Exception as exception:
      return JpmonitResult.invalid("Failed to check deadlock: " + exception)

    return has_deadlock


class JpmonitResult:
  @staticmethod
  def valid():
    return JpmonitResult(True)

  @staticmethod
  def invalid(message):
    return JpmonitResult(False, message)

  @staticmethod
  def from_collection(results):
    valid = True
    messages = []
    for result in results:
      if not result.is_valid():
        valid = False
        messages << result.get_message()
    return JpmonitResult(valid, "; ".join(messages))

  def __init__(self, valid, message=None):
    self.valid = valid
    self.message = message

  def __str__(self):
    return "JpmonitResult{validity: %s, message: %s}" % (self.valid, self.message)

  def is_valid(self):
    return self.valid

  def get_message(self):
    return self.message
