HALF_MOORE_COORDINATES = [[-1, -1], [-1, 0], [-1, 1], [0, -1]]


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