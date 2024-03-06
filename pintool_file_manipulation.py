import argparse

parser = argparse.ArgumentParser(description='Fragmentation analysis tool')
parser.add_argument('filename')
parser.add_argument('-b', '--both', action='store_true', help='shows pages with data and instructions')
parser.add_argument('-d', '--data', action='store_true', help='data fragmentation')
parser.add_argument('-i', '--instr', action='store_true', help='instruction fragmentation')
parser.add_argument('-a', '--all', action='store_true', help='fragmentation for all pages')
parser.add_argument('-v', '--verbose', action='store_true', help='shows number of read/write operations for data/instructions')

PAGE_SIZE = 4096

def used_pages(file_location: str, pages_inst: dict[int, list[int]], pages_data: dict[int, list[int]], pages_total: dict[int, list[int]]) -> None:
    with open(file_location, 'r') as file:
        if args.verbose:
            net = {'R': {'addr': 0, 'ip': 0},
                   'W': {'addr': 0, 'ip': 0}}

        for line in file:
            if line == '#eof\n':
                break

            line = line.strip().split(' ')
            if len(line) == 3:
                addr, size, typ = line
            elif len(line) == 4:
                addr, size, typ, operation = line

                if args.verbose:
                    net[operation][typ] += 1

            if typ == 'ip':
                pages = pages_inst
            elif typ == 'addr':
                pages = pages_data

            address = int(addr, 16)
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

    if args.verbose:
        for key, value in net.items():
            print(key)
            for k, v in value.items():
                print(f'{k}: {v}')
            print()

def fragmentation_calculation(output: list[str], pages_inst: dict[int, list[int]], pages_data: dict[int, list[int]], pages_total: dict[int, list[int]]) -> None:
    pages = pages_inst.keys() | pages_data.keys()
    used_total = 0
    used_data = 0
    used_instr = 0

    if args.all:
        min = [None]
        max = [None]
        count = 0
        suma = 0

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
            printline = ''

            if args.both:
                if page_instr_fragm < 100 and page_data_fragm < 100:
                    printline += '! '

            printline += f'{page_number:#x} F: {page_total_fragm:.2f}%'

            nevyuzite_bajty = PAGE_SIZE - page_used_total
            printline += f' NB: {nevyuzite_bajty}'

            count += 1
            suma += nevyuzite_bajty
            if min[0] is None or nevyuzite_bajty < min[0]:
                min[0] = nevyuzite_bajty
                min.append(page_number)
            if max[0] is None or nevyuzite_bajty > max[0]:
                max[0] = nevyuzite_bajty
                max.append(page_number)

            if args.data:
                printline += f' DF: {page_data_fragm:.2f}%'
            if args.instr:
                printline += f' IF: {page_instr_fragm:.2f}%'

            print(printline)

    if args.all:
        print('-----------')
        print(f'Pocet stranok: {count}')
        print(f'Priemerne nevyuzite bajty: {round(suma / count, 2)}')
        print(f'Minimalna velkost: {min[0]} na strankach:')
        for i in range(1, len(min)):
            print(hex(min[i]))
        print(f'Maximalna velkost: {max[0]} na strankach:')
        for i in range(1, len(max)):
            print(hex(max[i]))

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

    pages_inst: dict[int, list[int]] = {}
    pages_data: dict[int, list[int]] = {}
    pages_total: dict[int, list[int]] = {}
    output: list[str] = []

    used_pages(args.filename, pages_inst, pages_data, pages_total)
    fragmentation_calculation(output, pages_inst, pages_data, pages_total)

    for line in reversed(output):
        print(line)
