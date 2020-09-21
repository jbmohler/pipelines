import conducto as co


def sleepy(length=9, count=600) -> co.Parallel:
    image = co.Image(image="bash")

    output = co.Parallel(image=image, cpu=.5)
    for index in range(count):
        output[f"node{index:05n}"] = co.Exec(f"sleep {length}")
    return output


if __name__ == '__main__':
    co.Image.register_directory('JOEL_PIPELINES', '.')

    co.main(default=sleepy)
