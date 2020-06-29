import conducto as co


def sleepy(length=9) -> co.Serial:
    co.Image.register_directory('JOEL_PIPELINES', '.')

    image = co.Image(image="python:3.8-alpine")#, copy_dir='.')
    image1 = co.Image(image="python:3.7-alpine", copy_dir='.')

    pysleep = "import time; time.sleep({}); print(\"done\")".format(length)

    output = co.Serial(image=image)
    output['node1'] = co.Exec("python -c '{}'".format(pysleep))#, cpu=.25)
    output['node2'] = co.Exec("python -c '{}'".format(pysleep))#, cpu=.25)
    output['node3'] = co.Exec("python -c '{}'".format(pysleep), image=image1)
    output['node4'] = co.Exec("python -c '{}'".format(pysleep))
    return output


if __name__ == '__main__':
    co.main()
