import pandas as pd

data = pd.read_csv("catalog.csv")
data.drop(data.columns[0], axis=1, inplace=True)
print(data.head())


# Enter user's point
xp = -79.074886
yp = 34.674011


def inside_quad(xp, yp, x1, y1, x2, y2, x3, y3, x4, y4):

    d = (x2 - x1) * (yp - y1) - (xp - x1) * (y2 - y1)
    if d < 0:
        return False
    d = (x3 - x2) * (yp - y2) - (xp - x2) * (y3 - y2)
    if d < 0:
        return False
    d = (x4 - x3) * (yp - y3) - (xp - x3) * (y4 - y3)
    if d < 0:
        return False
    d = (x1 - x4) * (yp - y4) - (xp - x4) * (y1 - y4)
    if d >= 0:
        return True


for index, row in data.head().iterrows():
    x1 = row['ll_lon']
    y1 = row['ll_lat']
    x2 = row['ul_lon']
    y2 = row['ul_lat']
    x3 = row['ur_lon']
    y3 = row['ur_lat']
    x4 = row['lr_lon']
    y4 = row['lr_lat']

    if inside_quad(xp, yp, x1, y1, x2, y2, x3, y3, x4, y4):
        # print(row['file'])
        print(True)
