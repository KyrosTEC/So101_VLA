# Dataset Plan

## Importante
No subir datasets pesados a GitHub.
Los datos van en data/ que esta ignorada por .gitignore.

## IL Track
Situaciones:
- both_bw: blanco y negro visibles -> mover rojo a caja roja
- only_black: solo negro visible -> mover amarillo a caja amarilla
- only_white: solo blanco visible -> mover verde a caja verde

Piloto (10 demos):
```bash
bash scripts/record_il.sh both_bw 10
bash scripts/record_il.sh only_black 10
bash scripts/record_il.sh only_white 10
```

Produccion (100 demos):
```bash
bash scripts/record_il.sh both_bw 100
bash scripts/record_il.sh only_black 100
bash scripts/record_il.sh only_white 100
```

## VLA Track
Produccion (100 demos):
```bash
bash scripts/record_vla.sh red 100
bash scripts/record_vla.sh yellow 100
bash scripts/record_vla.sh green 100
```
