import picamera
import io
from PIL import Image


# Captures an image and converts it into a pil image
def getImage(camera):
	stream = io.BytesIO()
	camera.capture(stream, format='jpeg')
	stream.seek(0)
	return Image.open(stream)

# Returns the percentage with that the detect color matches the given color
def matchColors(color, detect):
	redMatch = float(abs(color[0] - detect[0])) / 255
	greenMatch = float(abs(color[1] - detect[1])) / 255
	blueMatch = float(abs(color[2] - detect[2])) / 255
	return 1 - (redMatch + greenMatch + blueMatch) / 3

# Takes a picture with the pi camera and returns the pixel where the detect
# color matched the best
def detectColor(camera, detect):
	# Get the image
	image = getImage(camera)
	width, height = image.size

	# Find the best matching pixel
	bestMatch = 0
	bestMatchPixel = (0, 0)
	bestMatchPixelColor = (0, 0, 0)
	for x in range(width):
		for y in range(height):
			pixel = image.getpixel((x, y))
			match = matchColors(pixel, detect)
			if match > bestMatch:
				bestMatch = match
				bestMatchPixel = (x, y)
				bestMatchPixelColor = pixel

	# Return best match pixel
	return bestMatchPixel


# Takes a picture and returns the bounds (x, y, width, height) where the detect
# color wos found
def getColorBounds(camera, detect):
	# Get the image
	image = getImage(camera)
	width, height = image.size

	# Find the matching pixels
	maxDiff = 50
	for x in range(width):
                for y in range(height):
			pixel = image.getpixel
