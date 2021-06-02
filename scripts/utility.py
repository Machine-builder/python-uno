def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def point_in_box(pointxy, box):
    left, top, right, bottom = box
    return pointxy[0]>=left and pointxy[0]<right and pointxy[1]>=top and pointxy[1]<bottom