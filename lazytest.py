import os
import conducto as co


def forgot_return() -> co.Serial:
    pass


def validated_lazy(value: int) -> co.Serial:
    if value > 100:
        print(f"nope, {value} too big")
        return

    output = co.Serial()
    output["print"] = co.Exec(f"echo epic value {value}")
    return output


def test_error_generates() -> co.Parallel:
    image = co.Image(image="alpine", copy_dir=".", reqs_py=["conducto"])

    with co.Parallel(image=image) as output:
        output["lazy1"] = co.Lazy(validated_lazy, 85)
        output["lazy2"] = co.Lazy(validated_lazy, 104)
        output["lazy3"] = co.Lazy(forgot_return)

    return output

def register():
    co.Image.share_directory("something", ".")

    print("cloud will error; local will show shares")
    os.system("cat /root/.conducto/{os.environ['CONDUCTO_PROFILE']}/config")

def late_register() -> co.Parallel:
    image = co.Image(image="alpine", copy_dir=".", reqs_py=["conducto"])

    with co.Parallel(image=image) as output:
        output["lazy1"] = co.Exec(register)

    return output


if __name__ == "__main__":
    co.Image.register_directory("JOEL_PIPELINES", ".")

    co.main()
