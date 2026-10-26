%%R

# clasificacion_variables.R — Parte A: clasificación de las variables de clientes.csv.
#
# El archivo data/clientes.csv tiene 12 clientes y 7 variables (más el id).
# El objetivo: clasificar cada variable (numérica continua/discreta, categórica
# binaria/ordinal/nominal) y verificar la clasificación en código.
#
# Regla del capítulo 3: el tipo de dato es una pista, no la clasificación.
# El criterio decide: ¿tiene sentido la mitad del valor?
# ¿Hay orden entre las categorías?
#
# Uso: ejecutar desde la raíz del repositorio con:
# source("scripts/clasificacion_variables.R")

# Cargar archivo CSV
clientes <- read.csv("data/clientes.csv",stringsAsFactors = FALSE)

# ---------------------------------------------------------------------------
# 1. Estructura del archivo
# ---------------------------------------------------------------------------

cat("Dimensiones:", nrow(clientes), "filas x",ncol(clientes), "columnas\n\n")
cat("Primeras filas:\n")
print(clientes)
cat("\n")

# ---------------------------------------------------------------------------
# 2. Tipos inferidos — la pista que da el lenguaje
# ---------------------------------------------------------------------------

cat("Tipos inferidos:\n")
print(sapply(clientes, class))
cat("\n")

# TODO 1: ¿qué columnas llegan como número y cuáles como texto?

columnas_numericas <- names(clientes)[sapply(clientes, is.numeric)]

columnas_texto <- names(clientes)[sapply(clientes, is.character)]

cat("Columnas numéricas:\n")
print(columnas_numericas)

cat("\nColumnas de texto:\n")
print(columnas_texto)

# ---------------------------------------------------------------------------
# 3. Valores únicos — ¿cuántas categorías hay y cuáles son?
# ---------------------------------------------------------------------------

# TODO 2: imprimir los valores únicos de cada columna.

cat("\nValores únicos por columna:\n")

for (columna in names(clientes)) {
  valores <- unique(clientes[[columna]])

  cat("\n", columna, ": ",
      length(valores), " valores únicos\n", sep = "")

  cat("  Valores: ")
  print(valores)
}

# ---------------------------------------------------------------------------
# 4. Declarar el orden de las variables ordinales
# ---------------------------------------------------------------------------

# TODO 3: convertir nivel_educacion a factor ordenado.

orden_educacion <- c(
  "Primaria",
  "Secundaria",
  "Tercer nivel",
  "Posgrado"
)

clientes$nivel_educacion <- factor(
  clientes$nivel_educacion,
  levels = orden_educacion,
  ordered = TRUE
)

cat("\nNivel educativo mínimo:\n")
print(min(clientes$nivel_educacion, na.rm = TRUE))

# TODO 4: convertir satisfaccion a factor ordenado.

orden_satisfaccion <- c("1", "2", "3", "4", "5")

clientes$satisfaccion <- factor(
  as.character(clientes$satisfaccion),
  levels = orden_satisfaccion,
  ordered = TRUE
)

cat("\nSatisfacción mínima:\n")
print(min(clientes$satisfaccion, na.rm = TRUE))

# Prueba extra: escribir incorrectamente "Postgrado".

orden_incorrecto <- c(
  "Primaria",
  "Secundaria",
  "Tercer nivel",
  "Postgrado"
)

prueba <- factor(
  as.character(clientes$nivel_educacion),
  levels = orden_incorrecto,
  ordered = TRUE
)

cat("\nValores faltantes por el error tipográfico:\n")
print(sum(is.na(prueba)))

# ---------------------------------------------------------------------------
# 5. Resumen de la clasificación
# ---------------------------------------------------------------------------

# TODO 5: clasificar cada variable según su naturaleza estadística.

clasificacion <- c(
  cliente_id = "Identificador",
  edad = "Numérica discreta",
  numero_hijos = "Numérica discreta",
  genero = "Categórica nominal",
  nivel_educacion = "Categórica ordinal",
  ciudad = "Categórica nominal",
  ingresos_mensuales = "Numérica continua",
  satisfaccion = "Categórica ordinal"
)

cat("\nResumen de la clasificación (para el informe):\n")

for (variable in names(clasificacion)) {
  cat(sprintf(
    "  %-20s %s\n",
    variable,
    clasificacion[variable]
  ))
}
