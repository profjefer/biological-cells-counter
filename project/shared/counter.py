import sys
import os
import cv2
import random
import numpy as np

HALF_MOORE_COORDINATES = [[-1, -1], [-1, 0], [-1, 1], [0, -1]]
MIN_SIZE = 40


def add_buffer(image):
    image.insert(0, [0] * len(image[0]))
    image.append([0] * len(image[0]))
    for r in range(len(image)):
        image[r].insert(0, 0)
        image[r].append(0)
    return image


def reduce_third_dimension(image):
    for i in range(len(image)):
        for j in range(len(image[i])):
            image[i][j] = image[i][j][0]
    return image


def get_cell_index(pixel, cells):
    for cell in cells:
        try:
            cell.index(pixel)
            return cells.index(cell)
        except ValueError:
            pass
    return -1


def add_pixel_to_cells(pixel, cells, neighbours):
    if len(neighbours) < 1:
        cells.append([])
        cells[-1].append(pixel)
    elif len(neighbours) > 1:
        cells[neighbours[0]].append(pixel)
        for i in range(1, len(neighbours)):
            cells[neighbours[0]].extend(cells[neighbours[i]])
            cells.remove(cells[neighbours[i]])
    else:
        cells[neighbours[0]].append(pixel)

    return cells


def check_neighbours(submatrix, pixel, cells):
    center_row, center_col = pixel
    neighbours = []

    for coord in HALF_MOORE_COORDINATES:
        neighbour = (center_row + coord[0], center_col + coord[1])
        if submatrix[coord[0] + 1][coord[1] + 1] == 255:
            cell_index = get_cell_index(neighbour, cells)
            if cell_index > -1:
                neighbours.append(cell_index)
    neighbours = list(set(neighbours))

    return neighbours


def count_cells(image):
    cells = []
    for r in range(1, int(len(image[0]) - 1)):
        for c in range(1, int(len(image[1]) - 1)):
            if image[r][c] == 255:
                matrix = [row[c-1:c+2] for row in image[r-1:r+2]]
                neighbours = check_neighbours(matrix, (r, c), cells)
                cells = add_pixel_to_cells((r, c), cells, neighbours)
    return cells


def reduce_cells(cells):
    reduced_cells = []
    for cell in cells:
        if len(cell) > MIN_SIZE:
            reduced_cells.append(cell)
    return reduced_cells


def random_rgb(colour_list):
    value = 0
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    while value < 3:
        value = 0
        if (r, 'r') in colour_list:
            r = random.randint(0, 255)
        else:
            value += 1
        if (g, 'g') in colour_list:
            g = random.randint(0, 255)
        else:
            value += 1
        if (b, 'b') in colour_list:
            b = random.randint(0, 255)
        else:
            value += 1
    colour_list.append((r, 'r'))
    colour_list.append((g, 'g'))
    colour_list.append((b, 'b'))
    return colour_list, [r, g, b]


def segmentation(image, cells):
    colour_list = []
    for cell in cells:
        colour_list, rgb = random_rgb(colour_list)
        for pixel in cell:
            image[pixel[0]][pixel[1]] = rgb
            
    return image


def expand_image(image):
    for i in range(len(image)):
        for j in range(len(image[i])):
            val = image[i][j]
            image[i][j] = [val, val, val]
    return image


def main():
    save = False
    path_to_file = sys.argv[1] if len(sys.argv) > 1 else exit("Missing argument: path_to_file")
    if len(sys.argv) > 2:
        output = sys.argv[2]
        save = True
    if os.path.exists(path_to_file) is False:
        exit("File not found: " + path_to_file)
    image = cv2.imread(path_to_file)
    try:
        image = image.tolist()
    except AttributeError:
        exit("Wrong file format: " + path_to_file)

    reduced_image = reduce_third_dimension(image)
    buffered_image = add_buffer(reduced_image)
    cells = count_cells(buffered_image)
    reduced_cells = reduce_cells(cells)
    print('The image contains ', len(reduced_cells), ' cells.')
    if save is True:
        expanded_image = expand_image(image)
        output_image = segmentation(expanded_image, reduced_cells)
        output_image = np.array(output_image)
        try:
            cv2.imwrite(output, output_image)
        except Exception:
            exit('Path not found: ' + output)


if __name__ == "__main__":
    main()
