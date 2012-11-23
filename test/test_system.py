import subprocess
import sys
import re
import os

output = subprocess.check_output(['ls', '-la', '/'], shell=False,  stderr=subprocess.STDOUT, universal_newlines=True).split(os.linesep)
print (output)
