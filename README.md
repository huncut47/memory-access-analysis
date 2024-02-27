# RP

## Kalkulacia internej fragmentacie v pamati

Toto je repo pre jeden z objektivov rocnikoveho projektu `Program na sledovanie a analyzu adries v pamati`\
Sklada sa z:
- cpp program produkujuci .out subor s vyuzitim pin toolu
- skript na kalkulovanie fragmentacie z logu
- sample pinatrace.out subor
  - tento subor obsahuje: `adresa velkost ip/addr`, kde ip=instrukcia, addr=data (?)

### cpp program

builduje sa z `pinatrace.cpp` (additional info je na [stranke samotneho intel pin-toolu](https://software.intel.com/sites/landingpage/pintool/docs/98830/Pin/doc/html/index.html#BuildingExamples))\
priklad:
```
make obj-intel64/pinatrace.so TARGET=intel64
```
vytvori `pinatrace.so`; tento program sa da nasledne spustit na nejaky iny program prikazom uvedenym nizsie a vytvori subor pinatrace.out, ktoreho spracovanie ma na starosti python script

`
*pin location* -t pinatrace.so -- *target program location*
`

priklad:
```
./pin -t pinatrace.so -- /bin/ls
```

vytvori file `pinatrace.out`

### py - interna fragmentacia

Python verzia: 3.11.6 alebo vyssia

prikaz na spustenie:

`
python *pintool_file_manipulation.py location* *pinatrace.out file location* -arguments
`

argumenty:
- `-b, --both` ku fragmentacii navyse vrati stranky, v ktorych sa pristupovalo aj k datam aj k instrukciam
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

s pouzitim agrumentu both, data, instr:

```
python pintool_file_manipulation.py pinatrace.out -bdi
```

vrati

```
Instr Fragmentacia: 93.11%
Data Fragmentacia: 93.39%
Celkova Fragmentacia: 86.50%
0x561c7b184: v stranke boli aj data aj instrukcie
```

### statistika.py
TODO
required python library: subprocess
