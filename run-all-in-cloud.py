import subprocess


def run_one_shell(pyfile, pipeline):
    print(
        f"""
Running pipeline {pipeline} in python file {pyfile}
"""
    )

    cmdline = [
        "python",
        "-m",
        "conducto",
        pyfile,
        pipeline,
        "--cloud",
        "--run",
        "--sleep-when-done",
        "--shell",
        "--no-app",
    ]

    subprocess.run(cmdline)


def run_all():
    to_run = [
        ("bigprog.py", "bigprog"),
        ("bigprog.py", "hugeprog"),
        ("docker_build_arg.py", "argged"),
        ("lazy_outer.py", "pipe"),
        ("docker_workdir.py", "test_docker_auto_workdir"),
        ("lazy_py_example.py", "pipe"),
        ("listbug.py", "pipeline"),
        ("multisleep.py", "sleepy"),
        ("series_sc.py", "series_sc"),
        ("mathtools.py", "domath_in_images"),
        ("mathtools.py", "domath"),
        ("slowdocker.py", "sc_slow"),
        ("treereset.py", "tree_reset_skip_test"),
        ("tempdatatest.py", "run"),
        ("test_exec_env.py", "print_exec_env"),
    ]
    for pyfile, pipeline, *args in to_run:
        run_one_shell(pyfile, pipeline)


if __name__ == "__main__":
    run_all()
