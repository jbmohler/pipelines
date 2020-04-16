import conducto as co

def sc_test() -> co.Serial:
    output = co.Serial(same_container="new")
    output['make_file'] = co.Exec("ls > myfile.txt")
    output['read_file'] = co.Exec("cat myfile.txt")
    output['error'] = co.Exec("cat does_not_exist.txt")
    return output

if __name__ == '__main__':
    co.main()
