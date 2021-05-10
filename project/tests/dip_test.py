import sys
import os
import cv2
from colorama import init
from termcolor import colored

sys.path.append('../')
from dip.segmentation_dip import segmentation
from shared.counter import count_cells, change_cells_to_rgb


def read_file(path_to_file):
    f = open(path_to_file, 'r')
    files = f.read()
    f.close()
    return files.split('\n')


def main():
    init()
    effectiveness = []
    number_of_tests = 0

    path_to_file = sys.argv[1] if len(sys.argv) > 1 else exit("Missing argument: path_to_file")
    if os.path.exists(path_to_file) is False:
        exit("File not found: " + path_to_file)

    files = read_file(path_to_file)

    for file in files:
        path_to_image = '../../train_set/' + file + '/images/' + file + '.png'
        print(f'Path to file: {path_to_image}')
        try:
            image = cv2.imread(path_to_image, cv2.CV_8UC1)
            prepared_image = segmentation(image)
            prepared_image = prepared_image.tolist()
            image, cells = count_cells(prepared_image)
            number_of_cells = len(cells)
            path_to_mask = '../../train_set/' + file + '/masks/'
            number_of_masks = len(os.listdir(path_to_mask))
            indicator = number_of_cells/number_of_masks
            effectiveness.append(indicator) if indicator <= 1 else 1
            print(colored(f'Effectiveness = {indicator}', 'green'))
            print(colored('TEST PASS', 'green'))
            number_of_tests += 1
        except Exception as e:
            print(colored(e, 'red'))
            print(colored('TEST FAIL', 'red'))

    avg = sum(effectiveness)/len(effectiveness)
    print()
    print('SUMMARY')
    print(f'Succeeded tests: {number_of_tests/len(files)}')
    print(f'Algorithm average: {avg}')


if __name__ == "__main__":
    main()
