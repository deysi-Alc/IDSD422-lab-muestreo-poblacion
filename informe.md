# Informe — Clasificación de variables y población vs. muestra

**Para:** Gerencia de RetailAndina S.A. · **De:** Equipo de Business Intelligence  
**Fecha:** 23/10/2026 · **Asunto:** Base de fidelización: tipos de variables y estimación por muestreo

---

## Resumen ejecutivo

Se clasificaron las variables de la base de fidelización y se estimó el ingreso mensual promedio de los 400 clientes. Se compararon tres diseños de muestreo con muestras de 20 clientes: conveniencia, aleatorio simple y estratificado. El parámetro poblacional fue de 1330.72 USD. Antes de decidir con una muestra, la gerencia debe considerar el sesgo y la variabilidad, ya que una estimación cercana no garantiza que el diseño sea adecuado.

## Parte A — Clasificación de las variables

| Variable | Tipo | Justificación (criterio) | Verificación en código |
|---|---|---|---|
| `cliente_id` | Identificador (nominal) | Etiqueta única por cliente, no se puede promediar ni se analiza como variable. | Texto: 12 únicos en 12 filas. |
| `edad` | Cuantitativa continua | Se mide: la mitad tiene sentido y existen valores intermedios, aquí está redondeada a años. | `int64`: 12 únicos, rango 22–48. |
| `numero_hijos` | Cuantitativa discreta | Es un conteo: solo enteros, no existe 2,5 hijos. | `int64`: 5 únicos (0 a 4). |
| `genero` | Cualitativa nominal | Categorías sin orden, la mitad no tiene sentido. | Texto: 3 únicos (Femenino, Masculino, Otro). |
| `nivel_educacion` | Cualitativa ordinal | Orden natural para cursar niveles educativos. | Texto: 4 únicos; orden declarado con `Categorical`. |
| `ciudad` | Cualitativa nominal | Lugar de residencia, sin orden entre ciudades. | Texto: 3 únicos (Cuenca, Guayaquil, Quito). |
| `ingresos_mensuales` | Cuantitativa continua | Monto en USD: la mitad tiene sentido y admite centavos, aquí viene en dólares enteros. | `int64`: 12 únicos. |
| `satisfaccion` | Cualitativa ordinal | Escala con orden, pero la distancia entre niveles no es fija. | `int64` (llegó como número): 4 únicos (2 a 5); escala 1–5 declarada. |

**P1.** ¿Qué te dijo el dtype de `satisfaccion` y por qué no basta para clasificarla? ¿Qué pasa si una ordinal queda como texto sin declarar el orden?

`satisfaccion` llegó como `int64`: pandas la leyó como número porque sus valores son 2 a 5, pero el dtype solo dice cómo se almacena, no que es una escala ordinal cuyos niveles no están a igual distancia. Si una ordinal queda como texto sin orden declarado, Python la ordena alfabéticamente: `sorted()` dio Posgrado, Primaria, Secundaria, Universidad. Con el orden declarado, `min()` dio Primaria y `max()`, Posgrado.

## Parte B — Población vs. muestra

### La población y su parámetro

| Concepto | Valor |
|---|---|
| Población (N) | 400 clientes (Quito 200, Guayaquil 120, Cuenca 80). |
| Variable de interés | `ingresos_mensuales` (USD). |
| Parámetro poblacional (media) | 1330.72 USD. |

**¿Por qué se muestrea si aquí el parámetro existe y se calculó?**

Se calculó porque la población es pequeña y completa. Normalmente medir a todos no es posible ni barato.

### Los tres diseños

| Diseño | n | Media estimada | Composición por ciudad | Diferencia vs. parámetro |
|---|---:|---:|---|---:|
| Conveniencia (`head`) | 20 | 1348.50 | Quito 20 | +17.78 |
| Aleatorio simple (`sample`) | 20 | 1336.00 | Quito 8, Guayaquil 4, Cuenca 8 | +5.28 |
| Estratificado (`groupby` + 5 %) | 20 | 1287.50 | Quito 10, Guayaquil 6, Cuenca 4 | −43.22 |

**Medias de 5 sorteos distintos del aleatorio simple (semillas 1 a 5):**

| Semilla | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|
| Media | 1336.00 | 1405.00 | 1235.00 | 1491.50 | 1288.00 |

**P2.** ¿Cuánto vale el parámetro poblacional y cuánto estimó cada diseño? ¿Cuál quedó más cerca y por qué eso no alcanza para declarar un ganador?

El parámetro es 1330.72 USD. Quedaron a +17.78 la conveniencia (1348.50), a +5.28 el aleatorio simple (1336.00) y a −43.22 el estratificado (1287.50). El aleatorio simple quedó más cerca, pero es un solo sorteo: con otras semillas dio entre 1235.00 y 1491.50, y en R el estratificado se alejó +223.28. Una corrida mide la suerte del sorteo, no la calidad del diseño.

**P3.** La muestra por conveniencia también tiene 20 filas. ¿Qué defecto tiene y cómo lo delatas en la composición por ciudad? ¿Se corrige tomando más filas?

La conveniencia tiene sesgo de selección: `head(20)` toma las primeras filas y el archivo está ordenado por ciudad, así que salieron 20 de 20 de Quito (100 %) cuando Quito es el 50 % de la base; Guayaquil (30 %) y Cuenca (20 %) quedaron en 0. Su media quedó cerca (+17.78) por azar: describe solo a Quito (media 1390.50). Más filas no lo corrigen: `head(200)` seguiría siendo solo Quito.

**P4.** El sorteo aleatorio dio un número distinto en cada semilla. ¿Qué implica esa variabilidad para una empresa que va a decidir con un solo estudio?

Las semillas 1 a 5 dieron 1336.00, 1405.00, 1235.00, 1491.50 y 1288.00: un rango de 256.50 USD para el mismo parámetro. Indica que es variabilidad de muestreo (azar, sin dirección), distinta del sesgo de la conveniencia (sistemático).

**P5.** ¿Cuándo usarías cada diseño en la práctica? Relaciona cada uno con un uso real (piloto, subgrupos que deben aparecer, conclusión sobre toda la población).

Conveniencia: pilotos o pruebas rápidas, sin buscar generalizar. Aleatorio simple: concluir sobre toda la población cuando hay lista completa y los subgrupos no son el foco. Estratificado: cuando hay subgrupos que deben aparecer, como las tres ciudades (10, 6 y 4 clientes), o grupos que difieren entre sí, como aquí en ingreso.

## Conclusiones

1. De las 7 variables, 2 son cuantitativas continuas (edad, ingresos_mensuales), 1 discreta (numero_hijos), 2 nominales (genero, ciudad) y 2 ordinales (nivel_educacion, satisfaccion). El dtype no basta.

2. Frente al parámetro de 1330.72 USD, los diseños de n = 20 estimaron 1348.50 (conveniencia), 1336.00 (aleatorio simple) y 1287.50 (estratificado). La conveniencia tomó 20 de 20 clientes de Quito frente al 50 % real: tiene sesgo por diseño, aunque su número quedó cerca.

3. Con cinco semillas, el aleatorio simple varió entre 1235.00 y 1491.50 (rango de 256.50 USD) y el estratificado dio −43.22 en Python y +223.28 en R: una sola corrida no demuestra que un diseño sea mejor. El diseño decide, no el tamaño.

