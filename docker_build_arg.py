import uuid
import conducto as co


def argged() -> co.Serial:
    output = co.Serial()
    for i in range(100):
        output[f"node{i:03n}"] = co.Exec(
            "cat /content.txt",
            image=co.Image(
                dockerfile="Dockerfile.buildarg",
                docker_build_args={"my_arg": f"node{i:03n} - {uuid.uuid1().hex}"},
            ),
        )
    return output


if __name__ == "__main__":
    co.Image.share_directory("JOEL_PIPELINES", ".")

    co.main()
