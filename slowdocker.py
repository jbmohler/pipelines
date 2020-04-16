import conducto as co
import uuid

with open("long_running_docker", "w") as f:
    f.write(f"""\
FROM alpine
# cache smash
RUN echo {uuid.uuid1().hex}
RUN sleep 10""")


def sc_slow() -> co.Serial:
    output = co.Serial()
    output['p1'] = co.Serial(same_container="new", image=co.Image(dockerfile="long_running_docker"))
    output['p1/make_file'] = co.Exec("ls > myfile.txt")
    output['p1/read_file'] = co.Exec("cat myfile.txt")
    output['p1/error'] = co.Exec("cat does_not_exist.txt")
    return output

if __name__ == '__main__':
    co.main()
