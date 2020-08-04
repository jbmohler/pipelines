import conducto as co

MAX_BITS = 6


def bits(n: int):
    # perhaps not the fastest, but all integer
    return len(bin(n))-2


def investigate(beta: int, bitlocked: int) -> co.Parallel:
    """
    Compute the collatz glide - the sequence of multiplies and divides until the
    collatz sequence for beta is less than beta.  Let divides be the number of
    divides in this glide.

    Set up a recursive investigation for all numbers with:

    - the same right-most `bitlocked` bits as beta
    - less than 2^`divides`
    """

    if beta >= 2**20:
        print(f"beta={beta} beyond 2**20; snub off", flush=True)
        return

    print(f"Computing the collatz glide for {beta}", flush=True)

    divides = 0
    value = beta
    # per conjecture, this ends sometime
    while value > beta or divides == 0:
        if value % 2 == 0:
            value //= 2
            divides += 1
        else:
            value = 3 * value + 1

    print(f"The number of divides in the collatz glide is {divides}", flush=True)

    x = 2**(divides)
    print(f"The collatz glide for all N*{x}+{beta} is identical for all N \in ZZ with N>=1.", flush=True)

    output = co.Parallel()

    tail = "0"*bitlocked+bin(beta)[2:]
    # consistent action on subscript even when bitlocked == 0
    tail = tail[len(tail)-bitlocked:]

    if divides > bitlocked:
        search = divides - bitlocked
        if search > MAX_BITS:
            print(f"Capped further investigation at patterns of {MAX_BITS} more bits", flush=True)
            search = min(MAX_BITS, divides)

        for i in range(1, 2**search):
            prefix = ("0"*search+bin(i)[2:])[-search:]
            newbeta = i*2**bitlocked + beta
            output[f"{prefix}-{tail}"] = co.Lazy(investigate, newbeta, divides)

    print("\n"*2, flush=True)

    return output


def collatz() -> co.Serial:
    """
    The Collatz conjecture states an intriguing property of all positive
    integers.   The pattern appears chaotic, but this pipeline shows a way to
    structure the computation by families of final bit patterns in the initial
    term of Collatz sequences.  Read more about the general problem at
    https://en.wikipedia.org/wiki/Collatz_conjecture .

    Consider pairs $$(3^x, 2^y)$$ with $$x,y \in ZZ$$ and $$2^y>3^x$$.  This
    pipeline is premised on a more fundamental conjecture that there is no such
    pair that is too close together.  The exact minimal distance depends on the
    noise introduced by the "+1" in the Collatz conjecture definition, but it
    can be readily bounded.  One can use that bound to easily verify this
    more fundamental conjecture for numbers far larger than any value of `beta`
    in the `investigate` function that this pipeline ever hopes to compute.
    """
    image = co.Image(image="python:3.8-alpine", name="base", copy_dir='.', reqs_py=['conducto'])

    output = co.Serial(image=image, cpu=.25)
    output['0'] = co.Lazy(investigate, 0, 0)
    return output


if __name__ == '__main__':
    co.Image.register_directory('JOEL_PIPELINES', '.')

    co.main()
