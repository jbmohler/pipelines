import conducto as co

def pipe() -> co.Serial:
   root = co.Serial(image=co.Image(copy_dir='.'))
   root["Deploy"] = co.Exec("echo Deploy service") 
   root["Test"] = co.Lazy("conducto lazy_inner.py test_service --num-tests=5", node_type=co.Parallel)

   return root

