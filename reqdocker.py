import conducto as co

def echo() -> co.Serial:
    co.Image.register_directory('JOEL_PIPELINES', '.')

    image = co.Image(dockerfile="Dockerfile.reqdocker")

    output = co.Serial(image=image)
    output['node0'] = co.Exec("echo 'from a shell'")
    output['node1'] = co.Exec("docker run --rm alpine echo 'from docker'", requires_docker=True)
    return output


if __name__ == '__main__':
    co.main()

