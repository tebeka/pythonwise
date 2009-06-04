def do_cool_stuff(n):
    print "%s is cool" % n

def positive_logic(x):
    if x > 2:
        y = f(x)
        if y < 10:
            g = f(y)
            if g > 0:
                do_cool_stuff(g)

def negative_logic(x):
    if x <= 2:
        return
    y = f(x)
    if y >= 10:
        return
    g = f(y)
    if g <= 0:
        return
    do_cool_stuff(g)
