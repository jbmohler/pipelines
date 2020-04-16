import conducto as co


def timed_sleep():
    import time

    for i in range(10):
        print(f"line {i}")
        time.sleep(0.001)


def bigprog(outers=8, inners=4) -> co.Serial:
    pythonImage = "python:3.7-slim"
    image = co.Image(image=pythonImage, copy_dir=".", reqs_py=["conducto"])

    output = co.Serial(image=image)
    for x in range(outers):
        node = "ser{:04}".format(x)
        output[node] = co.Serial()
        for y in range(inners):
            output["{}/node{:03n}".format(node, y)] = co.Exec(timed_sleep)
            # pysleep = "something ..."
            # output['{}/node{:03n}'.format(node, y)] = co.Exec("python -c '{}'".format(pysleep))
    # print(len(output.serialize()))
    return output


if __name__ == "__main__":
    co.main()
