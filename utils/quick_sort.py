def quick_sort(arr, key = lambda x: x):
    sorted_arr = arr.copy()

    def median_of_three(arr, l, m, r, key = lambda x: x):
        if key(arr[m]) > key(arr[r]):
            arr[m], arr[r] = arr[r], arr[m]
        if key(arr[l]) > key(arr[r]):
            arr[l], arr[r] = arr[r], arr[l]
        if key(arr[l]) > key(arr[m]):
            arr[l], arr[m] = arr[m], arr[l]


    def partition(arr, l, r, key = lambda x: x):
        m = (l + r) // 2
        median_of_three(arr, l, m, r, key)
        arr[m], arr[r] = arr[r], arr[m]

        pivot = l - 1

        for i in range(l, r):
            if key(arr[i]) <= key(arr[r]):
                pivot += 1
                arr[i], arr[pivot] = arr[pivot], arr[i]

        pivot += 1
        arr[r], arr[pivot] = arr[pivot], arr[r]
        return pivot

    def _sort(arr, l, r, key = lambda x: x):
        if l >= r:
            return arr

        while l < r:
            pivot = partition(arr, l, r, key)

            if pivot - l < r - pivot:
                _sort(arr, l, pivot - 1, key)
                l = pivot + 1
            else:
                _sort(arr, pivot + 1, r, key)
                r = pivot - 1
        
        return arr

    _sort(sorted_arr, 0, len(sorted_arr) - 1, key)
    return sorted_arr