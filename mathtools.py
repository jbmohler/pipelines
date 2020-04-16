import conducto as co


def domath_in_images() -> co.Parallel:
    def mathimage(base):
        return co.Image(image=base, reqs_py=["sympy"])

    cmd = "from sympy.ntheory.factor_ import factorint; print(factorint(298374981946161828218))"

    output = co.Parallel()
    output["node1"] = co.Exec("python -c '{}'".format(cmd), image=mathimage("alpine"))
    output["node1"] = co.Exec(
        "python -c '{}'".format(cmd), image=mathimage("debian:buster")
    )
    output["node1"] = co.Exec(
        "python -c '{}'".format(cmd), image=mathimage("debian:stretch")
    )
    output["node1"] = co.Exec(
        "python -c '{}'".format(cmd), image=mathimage("python:3.6")
    )
    output["node1"] = co.Exec(
        "python -c '{}'".format(cmd), image=mathimage("python:3.8")
    )
    output["node1"] = co.Exec(
        "python -c '{}'".format(cmd), image=mathimage("python:3.7")
    )
    return output


def domath() -> co.Serial:
    image = co.Image(image="python:3.7-alpine", copy_dir=".", reqs_py=["sympy"])

    cmd = "from sympy.ntheory.factor_ import factorint; print(factorint(298374981946161828218))"

    output = co.Serial(image=image)
    output["node1"] = co.Exec("python -c '{}'".format(cmd))
    return output


if __name__ == "__main__":
    output = co.main()
