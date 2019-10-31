from PIL import Image

# Open the image
image = Image.open("file_name.jpg")

# Convert image to RGB
rgb_image = image.convert('RGB')

# Find the width and height of the image by using .size
width = rgb_image.size[0]
height = rgb_image.size[1]

# Counters for row, column and total pixels
row = 1
col = 1
pix = 0

# Create an empty output row
rowdata = ""

# Find the RGB value for each pixel in each row
while row < height + 1:
    print("")
    print("Row number: " + str(row))
    while col < width + 1:
        # get the RGB values from the current pixel
        r, g, b = rgb_image.getpixel((col - 1, row - 1))
        # append the RGB values to the rowdata variable as (Red, Green, Blue)
        rowdata += "(" + str(r) + "," + str(g) + "," + str(b) + ") "
        # increment the column count
        col = col + 1
        # increment the pixel count
        pix = pix + 1
    # print out all RGB values for the row
    print(rowdata)
    # clear out rowdata variable
    rowdata = ""
    # increment the row
    row = row + 1
    # reset the column count
    col = 1

# Print the result to the console
print("")
print("Width = " + str(width) + " pixels")
print("Height = " + str(height) + " pixels")
print("Total Pixels = " + str(pix) + ".")
