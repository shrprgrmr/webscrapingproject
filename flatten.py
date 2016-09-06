def flatten(foo):
    for x in foo:
        if hasattr(x, '__iter__'):
            for y in flatten(x):
                yield y
        else:
            yield x
			
l_strings=["asdf qwer", "oiuw asdf","asdf qwer", "zxcv mcxz"]

print l_strings
print list(flatten([s.split() for s in list(flatten(l_strings))]))