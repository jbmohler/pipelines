import conducto as co

def print_exec_env() -> co.Serial:
    output = co.Serial()
    output['print'] = co.Exec("echo $CONDUCTO_EXECUTION_ENV")
    return output

if __name__ == '__main__':
    co.main()
