import uuid
import conducto as co


def argged() -> co.Serial:
    output = co.Serial()
    output['node1'] = co.Exec("cat /content.txt", image=co.Image(dockerfile="Dockerfile.buildarg", docker_build_args={"my_arg": f"node1 - {uuid.uuid1().hex}"}))
    output['node2'] = co.Exec("cat /content.txt", image=co.Image(dockerfile="Dockerfile.buildarg", docker_build_args={"my_arg": f"node2 - {uuid.uuid1().hex}"}))
    output['node3'] = co.Exec("cat /content.txt", image=co.Image(dockerfile="Dockerfile.buildarg", docker_build_args={"my_arg": f"node3 - {uuid.uuid1().hex}"}))
    output['node4'] = co.Exec("cat /content.txt", image=co.Image(dockerfile="Dockerfile.buildarg", docker_build_args={"my_arg": f"node4 - {uuid.uuid1().hex}"}))
    output['node5'] = co.Exec("cat /content.txt", image=co.Image(dockerfile="Dockerfile.buildarg", docker_build_args={"my_arg": f"node5 - {uuid.uuid1().hex}"}))
    output['node6'] = co.Exec("cat /content.txt", image=co.Image(dockerfile="Dockerfile.buildarg", docker_build_args={"my_arg": f"node6 - {uuid.uuid1().hex}"}))
    return output

if __name__ == '__main__':
    co.main()
