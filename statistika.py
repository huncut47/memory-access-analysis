import subprocess

root = '/home/rafael/Desktop/memory_access_analysis/'

# clear pinatrace.out, results.txt
with open(f'{root}pinatrace.out', 'w') as f01, open('results.txt', 'w') as f02:
    f01.write('')
    f02.write('')

with open(f'{root}programs.txt', 'r') as programs:
    programs = programs.read().split('\n')

    # for each program in programs.txt
    for line in programs:
        line = line.strip()

        # run pinatrace on the program, write the output to pinatrace.out (this is done by the actual program)
        print(f'Running {line}...')
        subprocess.run(f"{root}pin -t {root}pinatrace.so -- {line}", shell=True)

        # run pintool_file_manipulation.py on pinatrace.out, write the output to results.txt
        with open(f'{root}results.txt', 'a') as results:
            results.write(line + ": ")
        subprocess.run(f"/bin/python {root}pintool_file_manipulation.py {root}pinatrace.out -b >> results.txt", shell=True)

