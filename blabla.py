def countsort(arr):
    n = len(arr)

    # find the maximum element
    maxval = max(arr)

    # create and initialize count array
    count = [0] * (maxval + 1)

    # count frequency of each element
    for num in arr:
        count[num] += 1

    # compute prefix sum
    for i in range(1, maxval + 1):
        count[i] += count[i - 1]

    # build output array
    ans = [0] * n
    for i in range(n - 1, -1, -1):
        val = arr[i]
        ans[count[val] - 1] = val
        count[val] -= 1

    return ans


if __name__ == "__main__":
    arr = [2,5,3,0,2,3,0,3]
    sortedArr = countsort(arr)
    print(*sortedArr)