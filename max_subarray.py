def max_subarray(A):
    max_ending_here = max_so_far = A[0]
    start = 0
    end = 0
    ts = 0
    te = 0
    for i in range(1, len(A)):
        x = A[i]
        sum = max_ending_here + x
        if sum > x:
            te = i
            max_ending_here = sum
        else:
            ts = te = i
            max_ending_here = x

        if max_so_far < max_ending_here:
            start = ts
            end = te
            max_so_far = max_ending_here

        elif max_so_far == max_ending_here and end - start > te - ts:
            start = ts
            end = te

    return start, end


def get_output(str_in):
    str_in = str_in.strip().split('\n')
    str_out = ''
    for line in str_in:
        line = line.split(' ')
        A = []
        for item in line:
            A.append(int(item))

        start, end = max_subarray(A)
        str_out += str(start) + ',' + str(end) + '\n'

    return str_out


if __name__ == '__main__':
    assert max_subarray([-200, 50, 10, -20, 30, 40, -50, -40, 50, -200]) == \
           (1, 5)
    assert max_subarray([-200, 50, 10, -20, 30, 40, -50, -40, 50, -200, 50,
                         10, -20, 30, 40, -50, -40, 50, -200]) == (1, 5)

    assert max_subarray([1, 1, 1, -10, 3]) == (4, 4)
    assert max_subarray([0, 0, 0, 0, 0]) == (0, 0)
    assert max_subarray([4, 0, 0, 0, 0]) == (0, 0)
    assert max_subarray([-123, -2, -3, -6, -10]) == (1, 1)
    assert max_subarray([1, 3, 4, 7, 9]) == (0, 4)
