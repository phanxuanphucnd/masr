"""
Dict convert char2index and index2char
"""

char_map_str = """
<SPACE> 0
a 1
á 2
à 3
ã 4
ả 5
ạ 6
ă 7
ắ 8
ằ 9
ẵ 10
ẳ 11
ặ 12
â 13
ấ 14
ầ 15
ẫ 16
ẩ 17
ậ 18
b 19
c 20
d 21
đ 22
e 23
é 24
è 25
ẽ 26
ẻ 27
ẹ 28
ê 29
ế 30
ề 31
ễ 32
ể 33
ệ 34
f 35
g 36
h 37
i 38
í 39
ì 40
ĩ 41
ỉ 42
ị 43
j 44
k 45
l 46
m 47
n 48
o 49
ó 50
ò 51
õ 52
ỏ 53
ọ 54
ô 55
ố 56
ồ 57
ỗ 58
ổ 59
ộ 60
ơ 61
ớ 62
ờ 63
ỡ 64
ở 65
ợ 66
p 67
q 68
r 69
s 70
t 71
u 72
ú 73
ù 74
ũ 75
ủ 76
ụ 77
ư 78
ứ 79
ừ 80
ữ 81
ử 82
ự 83
v 84
w 85
x 86
y 87
ý 88
ỳ 89
ỹ 90
ỷ 91
ỵ 92
z 93
"""

char_map = {}
index_map = {}
for line in char_map_str.strip().split('\n'):
    ch, index = line.split()
    char_map[ch] = int(index)
    index_map[int(index)+1] = ch
index_map[1] = ' '