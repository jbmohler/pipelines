import conducto as co

def save_temp_data(index):
    co.temp_data.puts(name="data_chunk", obj=b'asdf '+bytes(str(index), 'utf-8'))

def save_perm_data(index):
    co.perm_data.puts(name="data_chunk", obj=b'asdf '+bytes(str(index), 'utf-8'))

def run() -> co.Serial:
    output = co.Serial(image=co.Image(copy_dir='.'))
    output["save_temp_data1"] = co.Exec(save_temp_data, 1) 
    output["save_perm_data1"] = co.Exec(save_perm_data, 1) 
    output["save_temp_data2"] = co.Exec(save_temp_data, 2) 
    output["save_perm_data2"] = co.Exec(save_perm_data, 2) 

    return output

if __name__ == "__main__":
    co.main()
