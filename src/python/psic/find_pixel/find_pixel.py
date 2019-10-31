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
row_data = ""

# Find the RGB value for each pixel in each row
while row < height + 1:
    print("")
    print("Row number: " + str(row))
    while col < width + 1:
        # Get the RGB values from the current pixel
        r, g, b = rgb_image.getpixel((col - 1, row - 1))
        # Append the RGB values to the rowdata variable as (Red, Green, Blue)
        row_data += "(" + str(r) + "," + str(g) + "," + str(b) + ") "
        # Increment the column count
        col = col + 1
        # Increment the pixel count
        pix = pix + 1
    # Print out all RGB values for the row
    print(row_data)
    # Clear out row data variable
    row_data = ""
    # Increment the row
    row = row + 1
    # Reset the column count
    col = 1

# Print the result to the console
print("")
print("Width = " + str(width) + " pixels")
print("Height = " + str(height) + " pixels")
print("Total Pixels = " + str(pix) + ".")
