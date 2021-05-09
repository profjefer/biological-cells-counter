import sys
import os
import cv2

sys.path.append('../')
from segmentation_dip import segmentation
from shared.counter import count_cells, change_cells_to_rgb


def main():
    save = False
    path_to_file = sys.argv[1] if len(sys.argv) > 1 else exit("Missing argument: path_to_file")
    if len(sys.argv) > 2:
        output = sys.argv[2]
        save = True
    if os.path.exists(path_to_file) is False:
        exit("File not found: " + path_to_file)

    image = cv2.imread(path_to_file, cv2.CV_8UC1)
    prepared_image = segmentation(image)

    try:
        prepared_image = prepared_image.tolist()
    except AttributeError:
        exit("Wrong file format: " + path_to_file)

    image, cells = count_cells(prepared_image)
    print('The image contains ', len(cells), ' cells.')

    if save is True:
        output_image = change_cells_to_rgb(image, cells)
        try:
            cv2.imwrite(output, output_image)
            print('File was saved.')
        except Exception:
            exit('Path not found: ' + output)


if __name__ == "__main__":
    main()
