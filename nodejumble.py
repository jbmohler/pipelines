import conducto as co


def parallel(max2pow: int) -> co.Parallel:
    co.Image.register_directory('JOEL_PIPELINES', '.')

    image = co.Image(image="alpine")

    output = co.Parallel(image=image)
    for j in range(3):
        for i in range(max2pow):
            sleep = f"sleep {2**i}"
            output[f'node_{j+1}_{i:03}'] = co.Exec(sleep, cpu=.25)
    return output


if __name__ == '__main__':
    co.main()
