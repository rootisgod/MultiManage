import subprocess
import sys

sub_process = subprocess.Popen("multipass launch", close_fds=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

while sub_process.poll() is None:
    out = sub_process.stdout.read(1)
    sys.stdout.write(str(sub_process.stderr.read(1)))
    # sys.stdout.write(str(out))
    sys.stdout.flush()
