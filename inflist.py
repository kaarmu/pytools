
def infList(slc: slice):
    value = slc.start
    op = (lambda a, b: a > b) if slc.step > 0 else (lambda a,b: a < b)
    while op(slc.stop, value):
        value += slc.step
        yield value

