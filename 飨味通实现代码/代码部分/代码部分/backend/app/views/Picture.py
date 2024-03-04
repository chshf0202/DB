

def getId():
    ans = 'p' + str(GetPictureID.PidBase).zfill(7)
    GetPictureID.PidBase += 1
    return ans


class GetPictureID:
    PidBase = 1
