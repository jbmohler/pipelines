import conducto as co

def oom_me():
    x = list(range(int(1e8)))


def master() -> co.Parallel:
    image = co.Image(image="alpine", copy_dir='.', reqs_py=['conducto'])

    with co.Parallel(image=image) as output:
        for i in range(40):
            output[f"exec{i:03}"] = t = co.Exec(oom_me)
            t.cpu = 0.5

    return output


if __name__ == '__main__':
    co.Image.register_directory('JOEL_PIPELINES', '.')

    co.main()

