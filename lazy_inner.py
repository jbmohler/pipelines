import conducto as co

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
