import subprocess
import conducto as co


def read_requirements() -> co.Parallel:
    proc = subprocess.run(
        "find . -name requirements.txt", shell=True, capture_output=True, check=True
    )

    lines = proc.stdout.decode("utf8").split("\n")
    lines = [ll for ll in lines if ll != ""]

    make_env = """\
python -m venv venv
. ./venv/bin/activate
pip install --upgrade pip
pip install -r {fullpath} > pip-install-requirements-stdout.txt 2> pip-install-requirements-stderr.txt

pip freeze
deactivate

cat pip-install-requirements-stderr.txt >&2
[ ! -s pip-install-requirements-stderr.txt ]
"""

    upgraded = """\
python -m venv venv
. ./venv/bin/activate
pip install --upgrade pip

cat {fullpath} | sed -e "s/==.*//g" > {xfullpath}

pip install -r {xfullpath} > pip-install-requirements-stdout.txt 2> pip-install-requirements-stderr.txt

deactivate

cat pip-install-requirements-stderr.txt >&2
[ ! -s pip-install-requirements-stderr.txt ]
"""

    compare_upgrade = """\
. ./venv/bin/activate

pip freeze | diff {fullpath} -
"""

    builder = co.Image(dockerfile="Dockerfile.venv_build", copy_dir=".")

    with co.Parallel() as output:
        for ll in lines:
            path, reqtxt = ll.rsplit("/", 1)

            path = path.replace("./", "").replace("/", "-")

            with co.Parallel(name=f"{path}") as sub:
                sub["cat"] = co.Exec(f"cat {ll}")
                sub["literal"] = co.Exec(make_env.format(fullpath=ll), image=builder)
                with co.Serial(
                    same_container="new",
                    name="unpinned",
                    stop_on_error=False,
                    image=builder,
                ) as sub2:
                    sub2["upgraded"] = co.Exec(
                        upgraded.format(
                            fullpath=ll,
                            xfullpath=ll.replace(
                                "requirements.txt", "x-requirements.txt"
                            ),
                        )
                    )
                    sub2["compare"] = co.Exec(
                        compare_upgrade.format(
                            fullpath=ll,
                            xfullpath=ll.replace(
                                "requirements.txt", "x-requirements.txt"
                            ),
                        )
                    )
    return output


def checkreqs() -> co.Serial:
    """
    This sets up a venv for every requirements.txt and installs it and does
    various sanity checks.
    """

    root = co.Serial(
        image=co.Image(copy_dir=".", reqs_py=["conducto"]), doc=co.util.magic_doc()
    )
    root["enumerate"] = co.Lazy(read_requirements)

    return root


if __name__ == "__main__":
    co.Image.register_directory("MYDIR", ".")

    co.main()
