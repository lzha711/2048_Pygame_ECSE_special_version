import pygame
# load all the images and resize all to 100*100 to fill in the tile
# 0 is replaced by blank image as default

resize = width, height = 100, 100

blank = pygame.transform.scale(pygame.image.load('images\c1.jpg'),resize) # blank represent 0
image2 = pygame.transform.scale(pygame.image.load('images\c2.png'),resize) # single cell
image3 = pygame.transform.scale(pygame.image.load('images\cwilliam.png'),resize) # william lee
image4 = pygame.transform.scale(pygame.image.load('images\cmark.png'),resize)
image5 = pygame.transform.scale(pygame.image.load('images\ckevin.png'),resize)
image6 = pygame.transform.scale(pygame.image.load('images\cnitish.png'),resize)
image7 = pygame.transform.scale(pygame.image.load('images\cakshya.png'),resize)
image8 = pygame.transform.scale(pygame.image.load('images\cstevan.png'),resize)
image9 = pygame.transform.scale(pygame.image.load('images\cbernard.png'),resize)
image10 = pygame.transform.scale(pygame.image.load('images\cpatrick.png'),resize)
image11 = pygame.transform.scale(pygame.image.load('images\czoran.png'),resize)
image12 = pygame.transform.scale(pygame.image.load('images\csingkiong.png'),resize)

# image dictionary
image_dict = {
    0:blank,
    2:image2,
    4:image3,
    8:image4,
    16:image5,
    32:image6,
    64:image7,
    128:image8,
    256:image9,
    512:image10,
    1024:image11,
    2048:image12
}