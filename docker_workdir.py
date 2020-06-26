import conducto as co

def test_docker_auto_workdir() -> co.Parallel:
    with co.Parallel() as output:
        output["docker_auto_workdir=True"] = n1 = co.Exec(test_docker_auto_workdir)
        output["docker_auto_workdir=False"] = n2 = co.Exec(test_docker_auto_workdir)
        n1.image = co.Image(copy_dir=".", docker_auto_workdir=True)
        n2.image = co.Image(copy_dir=".", docker_auto_workdir=False)
    return output
