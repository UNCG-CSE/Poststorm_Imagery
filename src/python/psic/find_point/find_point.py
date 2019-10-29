import pandas as pd

data = pd.read_csv("catalog.csv")
data.drop(data.columns[0], axis=1, inplace=True)

# Enter point to search for
xp = -77.680374
yp = 34.334811

#function determines if point is inside quad
def inside_quad(xp, yp, x1, y1, x2, y2, x3, y3, x4, y4):

    d1 = (x2 - x1) * (yp - y1) - (xp - x1) * (y2 - y1)

    d2 = (x3 - x2) * (yp - y2) - (xp - x2) * (y3 - y2)

    d3 = (x4 - x3) * (yp - y3) - (xp - x3) * (y4 - y3)

    d4 = (x1 - x4) * (yp - y4) - (xp - x4) * (y1 - y4)
    if d1 >= 0 and d2 >= 0 and d3 >= 0 and d4 >= 0:
        return True
    elif d1 <= 0 and d2 <= 0 and d3 <= 0 and d4 <= 0:
        return True
    else:
        return False

for index, row in data.iterrows():
    x1 = row['ll_lon']
    y1 = row['ll_lat']
    x2 = row['ul_lon']
    y2 = row['ul_lat']
    x3 = row['ur_lon']
    y3 = row['ur_lat']
    x4 = row['lr_lon']
    y4 = row['lr_lat']

    if inside_quad(xp, yp, x1, y1, x2, y2, x3, y3, x4, y4):
        print(row['file'])




