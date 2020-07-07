import conducto as co

def save_user_data(index: int):
    co.data.pipeline.puts(name="data/chunk", obj=b'asdf '+bytes(str(index), 'utf-8'))
    if index == 2:
        co.data.pipeline.puts(name="data/chunk2", obj=b'asdf '+bytes(str(index), 'utf-8'))

def save_pipeline_data(index: int):
    co.data.user.puts(name="data/chunk", obj=b'asdf '+bytes(str(index), 'utf-8'))
    if index == 2:
        co.data.user.puts(name="data/chunk2", obj=b'asdf '+bytes(str(index), 'utf-8'))

def read_user_data():
    print("data list")
    print(co.data.user.list("data"))
    data = co.data.pipeline.gets(name="data/chunk")
    print(data)

def read_pipeline_data():
    print("data list")
    print(co.data.pipeline.list("data"))
    data = co.data.user.gets(name="data/chunk")
    print(data)

def run() -> co.Serial:
    co.Image.register_directory("JOEL_PIPELINES", ".")

    output = co.Serial(image=co.Image(copy_dir='.'))
    output["save_user_data1"] = co.Exec(save_user_data, 1)
    output["save_pipeline_data1"] = co.Exec(save_pipeline_data, 1)
    output["save_user_data2"] = co.Exec(save_user_data, 2)
    output["save_pipeline_data2"] = co.Exec(save_pipeline_data, 2)
    output["read_user_data"] = co.Exec(read_user_data)
    output["read_pipeline_data"] = co.Exec(read_pipeline_data)

    return output

if __name__ == "__main__":
    co.main()
