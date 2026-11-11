"""Measured contiguous column bands: preserve order, never shrink or split items."""
def column_chunk(heights,available,gap=10):
    """Largest prefix fitting two columns; choose its shortest balanced band.

    Return (count, left_count, left_height, right_height), or None. All questions
    remain consecutive; the reader finishes left before moving to the right.
    """
    if not heights or available<=0:
        return None
    sums=[0]
    for height in heights:
        sums.append(sums[-1]+height)
    best=None
    for count in range(1,len(heights)+1):
        choices=[]
        for split in range(1,count+1):
            left=sums[split]+gap*(split-1)
            right=sums[count]-sums[split]+gap*max(0,count-split-1)
            if max(left,right)<=available:
                choices.append((max(left,right),abs(left-right),-split,split,left,right))
        if not choices:
            # With positive heights an overfull prefix cannot become shorter.
            break
        _,_,_,split,left,right=min(choices)
        best=(count,split,left,right)
    return best
