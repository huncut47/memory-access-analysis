# Tool na kalkulaciu internej fragmentacie v pamati

## Pin tool

building the pin tool from `pinatrace.cpp` (additional info je na [stranke samotneho intel pin-toolu](https://software.intel.com/sites/landingpage/pintool/docs/98830/Pin/doc/html/index.html#BuildingExamples))
```
make obj-intel64/pinatrace.so TARGET=intel64
```
tento pin tool sa da nasledne spustit na dany program prikazom uvedenym nizsie a vytvori subor pinatrace.txt, ktoreho spracovanie ma na starosti python script

`
*pin tool location* -t pinatrace.so -- *target program location*
`

## Interna fragmentacia

prikaz na spustenie:

`
python *pintool_file_manipulation.py location* *pinatrace.out file location* -arguments
`

argumenty:
- `-v, --verbose` ku fragmentacii navyse vrati stranky, v ktorych sa pristupovalo aj k datam aj k instrukciam
- `-d, --data` prida osobitnu fragmentaciu len pre data
- `-i, --instr` prida fragmentaciu pre instrukcie
- `-a, --all` zobrazi fragmentaciu pre vsetky stranky

priklad:

```
python pintool_file_manipulation.py pinatrace.out
```

vrati

```
Celkova Fragmentacia: 86.50%
```

s pouzitim agrumentu verbose, data, instr:

```
python pintool_file_manipulation.py pinatrace.out -vdi
```

vrati

```
Instr Fragmentacia: 93.11%
Data Fragmentacia: 93.39%
Celkova Fragmentacia: 86.50%
0x561c7b184: v stranke boli aj data aj instrukcie
```
