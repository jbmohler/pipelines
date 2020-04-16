import conducto as co
import typing

## BUG: This doesn't parse L correctly when called from command line:
## python listbug.py f --i=3
def f(i: int, L: typing.List[str] = ["a","b","c,d"]):
    print(i, L)

## This parses correctly when called from command line, but it feels
## wrong, doesn't result in a list L when called directly from python,
## and gives (probably correctly) gives a TypeError when used in the
## pipeline call below.
## python listbug.py g --i=4
def g(i: int, L: typing.List[str] = "d,e,f"):
    print(i, L)

## python listbug.py pipeline --func=f ## works as expected
## python listbug.py pipeline --func=g ## TypeError (correctly?)
def pipeline(func: str = "f") -> co.Serial:
    output = co.Serial()
    if func == "f":
        for i in range(5,7):
            output[str(i)] = co.asnode(f, i=i)
    else:
        for i in range(7,9):
            output[str(i)] = co.asnode(g, i=i)
    return output

if __name__ == "__main__":
    ## f works fine when conducto is not involved
    f(1)
    ## g doesn't error, but L is not a list
    g(2)
    co.main()
