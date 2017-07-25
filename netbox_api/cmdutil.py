import subprocess

import io
import re
import time

_GREEDY_WS_RE = re.compile('[\s]+')


class CommandResult(object):
    def __init__(self, return_code, stdout, stderr):
        self.return_code = return_code
        self.stdout = stdout
        self.stderr = stderr


def do_exec(cmd):
    args = _GREEDY_WS_RE.split(cmd)

    # Buffers to hold output
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()

    # Start the process
    process = subprocess.Popen(
        args=args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    # Poll the process for its status and output while it runs
    poll_result = process.poll()
    while poll_result is None:
        # Read STDOUT and STDERR
        stdout_buffer.write(
            process.stdout.read().decode('utf-8'))
        stderr_buffer.write(
            process.stderr.read().decode('utf-8'))

        # Sleep for 10ms
        time.sleep(0.01)

        # Poll the process again
        poll_result = process.poll()

    try:
        # Flush and read the rest of the stdout buffer
        process.stdout.flush()
        stdout_buffer.write(
            process.stdout.read().decode('utf-8'))
    except OSError:
        # We ignore this exception and simply close the fd
        pass
    finally:
        process.stdout.close()

    try:
        # Flush and read the rest of the stderr buffer
        process.stderr.flush()
        stderr_buffer.write(
            process.stderr.read().decode('utf-8'))
    except OSError:
        # We ignore this exception and simply close the fd
        pass
    finally:
        process.stderr.close()

    return CommandResult(
        return_code=process.returncode,
        stdout=stdout_buffer.getvalue().strip(),
        stderr=stderr_buffer.getvalue().strip())
