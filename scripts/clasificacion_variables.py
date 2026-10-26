# clasificacion_variables.py — Parte A: clasificación de las variables de clientes.csv.
#
# El archivo data/clientes.csv tiene 12 clientes y 7 variables (más el id).
# El objetivo: clasificar cada variable (numérica continua/discreta, categórica
# binaria/ordinal/nominal) y verificar la clasificación en código.
#
# Regla del capítulo 3: el dtype es una pista, no la clasificación — el criterio
# (¿tiene sentido la mitad del valor? ¿hay orden entre las categorías?) decide.
#
# Uso (desde la raíz del repositorio):  python scripts/clasificacion_variables.py

import pandas as pd

clientes = pd.read_csv("data/clientes.csv")

# ---------------------------------------------------------------------------
# 1. Estructura del archivo
# ---------------------------------------------------------------------------
print(f"Dimensiones: {clientes.shape[0]} filas × {clientes.shape[1]} columnas")
print()
print("Primeras filas:")
print(clientes.to_string(index=False))
print()

# ---------------------------------------------------------------------------
# 2. Tipos inferidos (dtype) — la pista que da el lenguaje
# ---------------------------------------------------------------------------
print("Tipos inferidos (dtype):")
print(clientes.dtypes)
print()
# TODO 1: ¿qué columnas llegan como número y cuáles como texto? Anótalo para el
#         informe. Ojo con satisfaccion: llega como número y es ordinal
#         ("4 no es el doble de 2") — la justificación va en el informe.
print("Columnas numéricas:")
print(clientes.select_dtypes(include="number").columns.tolist())

print("\nColumnas de texto:")
print(clientes.select_dtypes(include="object").columns.tolist())
# ---------------------------------------------------------------------------
# 3. Valores únicos — ¿cuántas categorías hay y cuáles son?
# ---------------------------------------------------------------------------
# TODO 2: completa el bucle para imprimir, por columna, cuántos valores únicos
#         hay y cuáles son. Pista: for columna in clientes.columns: ...  con
#         clientes[columna].unique() y len(). ¿Cuántas categorías tiene genero?
# for columna in clientes.columns:
#     ...

print()
for columna in clientes.columns:
    valores = clientes[columna].unique()
    print(f"{columna}: {len(valores)} valores únicos")
    print(f"  Valores: {valores}")
# ---------------------------------------------------------------------------
# 4. Declarar el orden de las variables ordinales
# ---------------------------------------------------------------------------
# Una ordinal se guarda como texto (o como número) y su orden natural se pierde:
# alfabéticamente "Posgrado" iría antes que "Primaria", que no tiene sentido.
#
# TODO 3: convierte nivel_educacion a categoría ordenada.
#         Pista: astype(pd.CategoricalDtype(categories=[...], ordered=True)).
#         Comprueba con .min(): debe devolver "Primaria".
# TODO 4: haz lo mismo con satisfaccion (escala 1–5 como etiquetas ordenadas).
#         Prueba extra: ¿qué pasa si en la lista de categorías escribes
#         "Postgrado" (con t) para nivel_educacion? Cuenta los faltantes con
#         .isna().sum() — la trampa del typo es silenciosa.
print()

# TODO 3: nivel_educacion
orden_educacion = pd.CategoricalDtype(categories=["Primaria","Secundaria","Tercer nivel","Posgrado"],ordered=True)

clientes["nivel_educacion"] = clientes["nivel_educacion"].astype(orden_educacion)

print("Nivel educativo mínimo:", clientes["nivel_educacion"].min())


# TODO 4: satisfaccion
orden_satisfaccion = pd.CategoricalDtype(categories=["1", "2", "3", "4", "5"],ordered=True)

clientes["satisfaccion"] = clientes["satisfaccion"].astype(str).astype(orden_satisfaccion)

print("Satisfacción mínima:", clientes["satisfaccion"].min())

# Prueba extra: error por escribir incorrectamente "Postgrado"
orden_incorrecto = pd.CategoricalDtype(
    categories=["Primaria","Secundaria","Tercer nivel","Postgrado"],ordered=True)

prueba = clientes["nivel_educacion"].astype(str).astype(orden_incorrecto)

print("Valores faltantes por el error tipográfico:", prueba.isna().sum())
# ---------------------------------------------------------------------------
# 5. Resumen de la clasificación (para el informe)
# ---------------------------------------------------------------------------
# TODO 5: completa el resumen con el tipo de cada variable (el criterio que
#         justifica cada clasificación va en el informe).
clasificacion = {
    "cliente_id": "Identificador",
    "edad": "Numérica discreta",
    "numero_hijos": "Numérica discreta",
    "genero": "Categórica nominal",
    "nivel_educacion": "Categórica ordinal",
    "ciudad": "Categórica nominal",
    "ingresos_mensuales": "Numérica continua",
    "satisfaccion": "Categórica ordinal",
}

print("Resumen de la clasificación (para el informe):")
for variable, tipo in clasificacion.items():
    print(f"  {variable:20s} {tipo}")
