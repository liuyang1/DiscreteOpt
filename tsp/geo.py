def kbline(pt0, pt1):
    if pt1[0] == pt0[0]:
        return None
    k = (pt1[1]-pt0[1]) / (pt1[0] - pt0[0])
    b = - k * pt0[0] + pt0[1]
    return k,b

def isCross(pt0, pt1, pt2, pt3):
    line0 = kbline(pt0, pt1)
    line1 = kbline(pt2, pt3)
    if not line0 or not line1:
        return False
    if line0[0] == line1[0]:
        return False
    dk, db = line1[0] - line0[0], line1[1] - line0[1]
    x = -1.0 * db / dk
    if x < min(pt0[0], pt1[0]) or x > max(pt0[0], pt1[0]):
        return False
    if x < min(pt2[0], pt3[0]) or x > max(pt2[0], pt3[0]):
        return False
    return True
