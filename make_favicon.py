from PIL import Image

img = Image.open("static/images/logo.png")
img.save("static/favicon.ico", format="ICO", sizes=[(32, 32), (64, 64), (128, 128)])

print("favicon.ico created in /static folder!")
