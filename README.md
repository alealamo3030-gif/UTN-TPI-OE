# TPI ORGANIZACIÓN EMPRESARIAL

## Integrantes
- Santiago Peralta
- Alejandro Alamo

## Materia
Organización Empresarial

## Empresa Simulada
PrimosTech

## Proceso Administrativo Seleccionado
Rendición de Gastos

---

# Descripción del Proyecto

Se desarrolló un chatbot simulador que automatiza el proceso de rendición de gastos dentro de una organización.

El objetivo es reemplazar un proceso manual por uno automatizado, permitiendo a los empleados registrar gastos, consultar presupuestos disponibles y recibir una respuesta automática según las reglas definidas por la empresa.

El sistema fue diseñado tomando como base un modelo BPMN 2.0 y posteriormente implementado en Python utilizando archivos CSV como base de datos simulada.

---

# Funcionalidades

- Identificación de empleados mediante ID.
- Consulta de presupuesto disponible.
- Registro de rendiciones de gastos.
- Validación de comprobantes.
- Aprobación automática de gastos menores.
- Derivación a supervisor para gastos intermedios.
- Rechazo de gastos que exceden los límites establecidos.
- Registro automático de todas las operaciones realizadas.
- Manejo de errores y validación de entradas del usuario.

---

# Ejecución del Programa

Ejecutar desde una terminal:

```
python TPI_OE_Peralta_Alamo.py
```

---

## Menú Principal

Al iniciar el programa se mostrará el siguiente menú:

```
1. Nueva rendición de gastos
2. Consultar presupuesto disponible
3. Salir
```

---

## Opción 1: Nueva Rendición de Gastos

### Paso 1: Identificación del Empleado

El sistema solicitará el ID del empleado.

Ejemplo:

```
E001
```

Si el ID no existe, se solicitará nuevamente.

---

### Paso 2: Selección de Categoría

El usuario deberá seleccionar una categoría:

```
1. Viáticos y traslados
2. Material de oficina
3. Capacitación y cursos
4. Equipamiento tecnológico
5. Otro
```

---

### Paso 3: Descripción del Gasto

El sistema solicitará una breve descripción.

Ejemplo:

```
Taxi al aeropuerto
```

---

### Paso 4: Ingreso del Monto

Se deberá ingresar el importe a rendir.

Ejemplo:

```
3500
```

Validaciones:

- Debe ser numérico.
- Debe ser mayor que cero.

---

### Paso 5: Comprobante

El usuario deberá indicar si posee comprobante.

```
1. Factura
2. Ticket o recibo
3. No tengo comprobante
```

Si selecciona la opción 3, el proceso será cancelado.

---

### Paso 6: Evaluación de la Solicitud

El sistema evalúa automáticamente la rendición.

#### Aprobación Automática

Montos menores o iguales a $5.000.

```
APROBADO AUTOMÁTICAMENTE
```

#### Revisión por Supervisor

Montos mayores a $5.000 y menores o iguales a $20.000.

```
PENDIENTE DE APROBACIÓN DEL SUPERVISOR
```

#### Rechazo

La solicitud será rechazada cuando:

- Supere el presupuesto disponible.
- Supere el límite máximo permitido.

---

### Paso 7: Resumen Final

Se muestra:

- Nombre del empleado
- Concepto
- Monto
- Comprobante
- Resultado

Además, la operación queda registrada en el historial.

---

## Opción 2: Consultar Presupuesto

Permite consultar:

- Nombre
- Departamento
- Presupuesto disponible
- Gastos acumulados

Ingresando el ID del empleado.

---

## Opción 3: Salir

Finaliza la ejecución del sistema.

---

# Base de Datos Simulada

## empleados.csv

Contiene:

| Campo | Descripción |
|---------|---------|
| id | Identificador único |
| nombre | Nombre del empleado |
| departamento | Área de trabajo |
| presupuesto_disponible | Saldo disponible |
| gastos_acumulados | Total histórico de gastos |

---

# Reglas de Negocio

### Aprobación Automática

```
Monto ≤ $5.000
```

### Revisión de Supervisor

```
$5.001 ≤ Monto ≤ $20.000
```

### Rechazo

```
Monto > Presupuesto Disponible
```

o

```
Monto > $20.000
```
