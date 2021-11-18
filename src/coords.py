def is_within(rect1, rect2):
    r1tl = rect1[0]
    r1br = rect1[1]
    r2tl = rect2[0]
    r2br = rect2[1]
    return r1tl[0] >= r2tl[0] and \
        r1tl[1] >= r2tl[1] and \
        r1br[0] <= r2br[0] and \
        r1br[1] <= r2br[1]


