import conducto as co

with open("Dockerfile.buildarg", "w") as f:
    f.write("""\
FROM alpine
ARG my_arg
RUN echo $my_arg > /content.txt""")


def argged() -> co.Serial:
    output = co.Serial()
    output['node1'] = co.Exec("cat /content.txt", image=co.Image(dockerfile="Dockerfile.buildarg", dockerfile_build_args={"my_arg": "node1"}))
    output['node2'] = co.Exec("cat /content.txt", image=co.Image(dockerfile="Dockerfile.buildarg", dockerfile_build_args={"my_arg": "node2"}))
    return output

if __name__ == '__main__':
    co.main()
