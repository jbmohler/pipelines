import conducto as co

def tree_reset_skip_test() -> co.Serial:
    output = co.Serial()
    output['gpar'] = co.Serial()
    output['gpar/sib'] = co.Exec("echo why me")
    output['gpar/p1'] = co.Serial(same_container="new")
    output['gpar/p1/make_file'] = co.Exec("ls > myfile.txt")
    output['gpar/p1/read_file'] = co.Exec("cat myfile.txt")
    output['gpar/p1/error'] = co.Exec("cat does_not_exist.txt")
    output['p2'] = co.Serial()
    output['p2/greeting'] = co.Exec("echo hello world")
    return output

if __name__ == '__main__':
    co.main()
