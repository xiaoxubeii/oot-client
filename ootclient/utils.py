__author__ = 'tardis'
import subprocess


def patch_subprocess():
    def _check_output(*popenargs, **kwargs):
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            error = subprocess.CalledProcessError(retcode, cmd)
            error.output = output
            raise error
        return output

    if not hasattr(subprocess, 'check_output'):
        subprocess.check_output = _check_output

    return subprocess
