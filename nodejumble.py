import conducto as co


def parallel(max2pow: int) -> co.Parallel:
    image = co.Image(image="alpine")

    def cmd_sleep(i):
        return f"""\
echo "{i+1} iterations of {2**i//(i+1)} seconds"
for i in $(seq 1 {i+1})
do
    echo "Iteration " $i
    sleep {2**i//(i+1)}
done"""


    with co.Parallel(image=image) as output:
        with co.Parallel(name='set1') as set1:
            for i in range(max2pow):
                set1[f'node_{1}_{i:03}'] = co.Exec(cmd_sleep(i), cpu=.25)

        with co.Parallel(name='set2') as set2:
            for i in range(max2pow):
                set2[f'node_{2}_{i:03}'] = co.Exec(cmd_sleep(i), cpu=.25, max_time="13s")

        with co.Parallel(name='set3') as set3:
            for i in range(max2pow):
                set3[f'node_{3}_{i:03}'] = co.Exec(cmd_sleep(i), cpu=.25, max_time="12h")

    return output


if __name__ == '__main__':
    co.Image.register_directory('JOEL_PIPELINES', '.')

    co.main()
