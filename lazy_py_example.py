import conducto as co

def sam(i):
    print(i)

def pipe() -> co.Serial:
    root = co.Serial()#image=co.Image(copy_dir="."))
    root["Pre-test"] = co.Exec(sam, 34)
    root["Deploy"] = co.Exec("echo Deploy service")
    root["Test-site"] = co.Lazy(test_service, url="http://testsite", num_tests=5)
    root["Test-x"] = co.Lazy(test_service, url="http://testx", num_tests=4)

    print(root.pretty())
    # /
    # ├─0 Deploy   echo Deploy service
    # └─1 Test
    #   ├─0 Generate   conducto test.py test_service --num_tests=5
    #   └─1 Execute

    return root

def test_service(url:str=None, num_tests=1) -> co.Parallel:
    if url is None:
        # Some deployment strategies will create a new service. In these cases you may
        # not know the URL ahead of time but it can be determined on-the-fly. We mock
        # such an example here.
        url = "https://example.com/look_up_url_at_runtime"
    output = co.Parallel()
    for i in range(num_tests):
        output[f"RunTest_{i}"] = co.Exec(f"Testing deployment at {url}")
    return output

if __name__ == "__main__":
    co.main()
