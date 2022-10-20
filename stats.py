
# mag = 4
# min = 1084005635.0
# max = 2135986984.0

mag = 8
min = 0.446526174 * 1000000
max = 0.889635157 * 1000000

total = 0
under = 0
within = 0
over = 0

with open(f'/maps/mwd24/res_{mag}.csv') as f:
    while True:
        try:
            line = f.readline()
            val = float(line.split(',')[1].strip())

            total += 1
            if val < min:
                under += 1
            elif val > max:
                over += 1
            else:
                within += 1
        except:
            break


print(f"""
 total: {total}
 under: {under} ({(float(under)/float(total)) * 100}%)
 within: {within} ({(float(within)/float(total)) * 100}%)
 over: {over} ({(float(over)/float(total)) * 100}%)
""")