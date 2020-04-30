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

def hugeprog(l1=10, l2=10, l3=10, l4=10) -> co.Serial:
    image = co.Image(image="alpine")

    output = co.Serial(image=image, cpu=.25)
    for x in range(l1):
        p1 = f"ser{x:04}"
        output[p1] = co.Parallel()
        for y in range(l2):
            p2 = f"{p1}/l2-{y:04}"
            output[p2] = co.Parallel()
            for z in range(l3):
                p3 = f"{p2}/l3-{z:04}"
                output[p3] = co.Parallel()
                for w in range(l4):
                    output[f"{p3}/node{w:03n}"] = co.Exec(f"echo I am {x} {y} {z} {w}")
    # print(len(output.serialize()))
    return output


if __name__ == "__main__":
    co.main()
