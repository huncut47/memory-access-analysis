#!/usr/bin/env python

from __future__ import annotations
import argparse

PAGE_SIZE = 4096

parser = argparse.ArgumentParser(description='Fragmentation analysis tool')
parser.add_argument('filename')
parser.add_argument('-b', '--both', action='store_true', help='shows pages with data and instructions')
parser.add_argument('-d', '--data', action='store_true', help='data fragmentation')
parser.add_argument('-i', '--instr', action='store_true', help='instruction fragmentation')
parser.add_argument('-a', '--all', action='store_true', help='fragmentation for all pages')

def used_pages(file_location: str, pages_inst: dict, pages_data: dict, pages_total: dict) -> None:
    with open(file_location, 'r') as file:
        for line in file:
            if line == '#eof\n':
                break

            address, size, typ = line.strip().split(' ')

            if typ == 'ip':
                pages = pages_inst
            elif typ == 'addr':
                pages = pages_data

            address = int(address, 16)
            page_number = address // PAGE_SIZE

            if page_number not in pages:
                pages[page_number] = [0] * PAGE_SIZE

            if page_number not in pages_total:
                pages_total[page_number] = [0] * PAGE_SIZE

            for i in range(int(size)):
                offset = address % PAGE_SIZE + i

                while offset >= PAGE_SIZE:
                    page_number += 1
                    if page_number not in pages:
                        pages[page_number] = [0] * PAGE_SIZE
                    if page_number not in pages_total:
                        pages_total[page_number] = [0] * PAGE_SIZE
                    offset -= PAGE_SIZE

                pages[page_number][offset] = 1
                pages_total[page_number][offset] = 1

def fragmentation_calculation(output: list, pages_inst: dict, pages_data: dict, pages_total: dict) -> None:
    pages = pages_inst.keys() | pages_data.keys()
    used_total = 0
    used_data = 0
    used_instr = 0

    for page_number in pages:
        page_used_inst = sum(pages_inst.get(page_number, []))
        page_used_data = sum(pages_data.get(page_number, []))
        page_used_total = sum(pages_total.get(page_number, []))

        used_total += page_used_total
        used_data += page_used_data
        used_instr += page_used_inst

        page_instr_fragm = 100 - page_used_inst / PAGE_SIZE * 100
        page_data_fragm = 100 - page_used_data / PAGE_SIZE * 100
        page_total_fragm = 100 - page_used_total / PAGE_SIZE * 100

        if args.both:
            if page_instr_fragm < 100 and page_data_fragm < 100:
                output.append(f'{page_number:#x}: v stranke boli aj data aj instrukcie')

        if args.all:
            printline = f''

            if args.both:
                if page_instr_fragm < 100 and page_data_fragm < 100:
                    printline += f'! '

            printline += f'{page_number:#x} F: {page_total_fragm:.2f}%'

            if args.data:
                printline += f' DF: {page_data_fragm:.2f}%'
            if args.instr:
                printline += f' IF: {page_instr_fragm:.2f}%'

            print(printline)

    total_fragmentation = 100 - used_total / (len(pages) * PAGE_SIZE) * 100
    data_fragmentation = 100 - used_data / (len(pages) * PAGE_SIZE) * 100
    instr_fragmentation = 100 - used_instr / (len(pages) * PAGE_SIZE) * 100

    output.append(f'Celkova Fragmentacia: {total_fragmentation:.2f}%')
    if args.data:
        output.append(f'Data Fragmentacia: {data_fragmentation:.2f}%')
    if args.instr:
        output.append(f'Instr Fragmentacia: {instr_fragmentation:.2f}%')

if __name__ == '__main__':
    args = parser.parse_args()

    pages_inst = {}
    pages_data = {}
    pages_total = {}
    output = []

    used_pages(args.filename, pages_inst, pages_data, pages_total)
    fragmentation_calculation(output, pages_inst, pages_data, pages_total)

    for line in reversed(output):
        print(line)

# /home/rafael/Desktop/Pinatrace/pinatrace.out

# pridaj -d perhaps na debug
# prida stranky ktore sa citali bez pisania
# fragmentacia pre pamat / pre stranky s prepinacom