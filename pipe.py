from subprocess import Popen, PIPE, STDOUT

def pipe(*commands, **kw):
    """Run a chain of commands, returns the output of the last one.

    Arguments are a list of command line arguments, an optional keyword "stderr"
    can be used to capture stdandard error as well. Example:

    pipe(["dmesg"], ["grep", "hda"]) is like "dmesg | grep hda"
    """
    stderr = STDOUT if kw.get("stderr", False) else None
    pipe = None
    for cmdline in commands:
        stdin = pipe.stdout if pipe else None
        pipe = Popen(cmdline, stdin=stdin, stdout=PIPE, stderr=stderr)

    return pipe.communicate()[0]
