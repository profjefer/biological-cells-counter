def add_buffer(image):
    image.insert(0, [0] * len(image[0]))
    image.append([0] * len(image[0]))
    for r in range(len(image)):
        image[r].insert(0, 0)
        image[r].append(0)
    return image