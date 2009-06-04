def mask(size):
    '''Mask for `size' bits

    >>> mask(3)
    7
    '''
    return (1L << size) - 1

def num2bits(num, width=32):
    '''String represntation (in bits) of a number

    >>> num2bits(3, 5) 
    '00011'
    '''
    s = ""
    for bit in range(width - 1, -1, -1):
        if num & (1L << bit):
            s += "1"
        else:
            s += "0"
    return s

def get_bit(value, bit):
    '''Get value of bit

    >>> num2bits(5, 5)
    '00101'
    >>> get_bit(5, 0)
    1
    >>> get_bit(5, 1)
    0
    '''
    return (value >> bit) & 1

def get_range(value, start, end):
    '''Get range of bits

    >>> num2bits(5, 5)
    '00101'
    >>> get_range(5, 0, 1)
    1
    >>> get_range(5, 1, 2)
    2
    '''
    return (value >> start) & mask(end - start + 1)

def set_bit(num, bit, value):
    '''Set bit `bit' in num to `value' 

    >>> i = 5
    >>> set_bit(i, 1, 1)
    7
    >>> set_bit(i, 0, 0)
    4
    '''
    if value:
        return num | (1L << bit)
    else:
        return num & (~(1L << bit))

def sign_extend(num, size):
    '''Sign exten number who is `size' bits wide
    
    >>> sign_extend(5, 2)
    1
    >>> sign_extend(5, 3)
    -3
    '''
    m = mask(size - 1)
    res = num & m
    # Positive
    if (num & (1L << (size - 1))) == 0:
        return res

    # Negative, 2's complement
    res = ~res
    res &= m
    res += 1
    return -res
