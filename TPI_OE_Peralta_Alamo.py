import csv

# ============================================
# SIMULADOR DE CHATBOT - RENDICIÓN DE GASTOS
# TPI - Organización Empresarial - UTN TUP 2026
# Alumnos: Peralta - Alamo
# Empresa ficticia: PrimosTech
# ============================================

archivo_empleados = 'empleados.csv'
archivo_historial = 'historial_gastos.csv'

# Límites que determinan el camino del bot (Gateways del BPMN)
limite_auto       = 5000   # Hasta acá se aprueba automáticamente
limite_supervisor = 20000  # Hasta acá requiere supervisor, arriba se rechaza


# ============================================================
# LECTURA Y ESCRITURA CSV
# ============================================================

def cargar_empleados():
    # Cargamos los empleados desde el CSV usando DictReader
    empleados = []
    try:
        with open(archivo_empleados, 'r', encoding='utf-8-sig') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                empleados.append({
                    'id':                     fila['id'].strip().upper(),
                    'nombre':                 fila['nombre'].strip().title(),
                    'departamento':           fila['departamento'].strip().title(),
                    'presupuesto_disponible': int(fila['presupuesto_disponible']),
                    'gastos_acumulados':      int(fila['gastos_acumulados'])
                })
    except FileNotFoundError:
        print(f"ERROR: No se encontro el archivo '{archivo_empleados}'.")
    return empleados


def guardar_empleados(empleados):
    # Guardamos los cambios de presupuesto en el CSV con DictWriter
    columnas = ['id', 'nombre', 'departamento', 'presupuesto_disponible', 'gastos_acumulados']
    with open(archivo_empleados, 'w', newline='', encoding='utf-8') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(empleados)


def registrar_historial(empleado, concepto, monto, resultado):
    # Registramos la rendición en el historial usando modo append
    # para no borrar registros anteriores
    columnas = ['id_empleado', 'nombre', 'concepto', 'monto', 'resultado']

    # Verificamos si el archivo ya existe para no repetir el encabezado
    archivo_existe = False
    try:
        archivo = open(archivo_historial, 'r')
        archivo.close()  # cerramos porque no necesitamos leer nada, solo chequear que existe
        archivo_existe = True
    except FileNotFoundError:
        archivo_existe = False

    with open(archivo_historial, 'a', newline='', encoding='utf-8') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        if not archivo_existe:
            escritor.writeheader()
        escritor.writerow({
            'id_empleado': empleado['id'],
            'nombre':      empleado['nombre'],
            'concepto':    concepto,
            'monto':       monto,
            'resultado':   resultado
        })


# ============================================================
# FLUJO PRINCIPAL DE RENDICIÓN
# ============================================================

def iniciar_rendicion(empleados):
    print('\n--- NUEVA RENDICION DE GASTOS ---')

    # Variable de estado que registra en qué paso del proceso se encuentra el usuario
    # Refleja la Máquina de Estados del diagrama BPMN
    estado = 'esperando_id'

    # PASO 1: Identificacion del empleado
    while True:
        id_ingresado = input('\nBot: Ingrese su ID de empleado (ej: E001): ').strip().upper()

        if id_ingresado == 'SALIR':
            estado = 'cancelado'
            print('Bot: Proceso cancelado.')
            return

        if id_ingresado == '':
            print('Bot: El ID no puede estar vacio. Intente nuevamente.')
            continue

        empleado = None
        for emp in empleados:
            if emp['id'] == id_ingresado:
                empleado = emp
                break

        if empleado is None:
            print(f'Bot: No encontre ningun empleado con el ID "{id_ingresado}". Intente nuevamente.')
            continue

        estado = 'identificado'
        print(f'\nBot: Empleado identificado: {empleado["nombre"]} - {empleado["departamento"]}')
        print(f'Bot: Presupuesto disponible: ${empleado["presupuesto_disponible"]:,}')
        break

    # PASO 2: Concepto del gasto
    estado = 'esperando_categoria'
    print('\nBot: Seleccione la categoria del gasto:')
    print('     1. Viaticos y traslados')
    print('     2. Material de oficina')
    print('     3. Capacitacion y cursos')
    print('     4. Equipamiento tecnologico')
    print('     5. Otro')

    categorias = {
        '1': 'Viaticos y traslados',
        '2': 'Material de oficina',
        '3': 'Capacitacion y cursos',
        '4': 'Equipamiento tecnologico',
        '5': 'Otro'
    }

    while True:
        opcion = input('\nUsuario: ').strip()
        if opcion.lower() == 'salir':
            estado = 'cancelado'
            print('Bot: Proceso cancelado.')
            return
        if opcion not in categorias:
            print('Bot: Opcion invalida. Ingrese un numero del 1 al 5.')
            continue
        categoria = categorias[opcion]
        estado = 'categoria_seleccionada'
        break

    descripcion = input(f'Bot: Describa el gasto ({categoria}): ').strip()
    if descripcion == '':
        descripcion = 'Sin descripcion'
    concepto = f'{categoria} - {descripcion}'

    # PASO 3: Monto del gasto
    estado = 'esperando_monto'
    while True:
        entrada = input('\nBot: Ingrese el monto a rendir en pesos: $').strip()
        if entrada.lower() == 'salir':
            estado = 'cancelado'
            print('Bot: Proceso cancelado.')
            return
        try:
            monto = float(entrada.replace(',', '.'))
            if monto <= 0:
                print('Bot: El monto debe ser mayor a $0.')
                continue
            estado = 'monto_ingresado'
            break
        except ValueError:
            print('Bot: Monto invalido. Ingrese solo numeros (ej: 1500).')

    # PASO 4: Verificacion de comprobante
    estado = 'esperando_comprobante'
    print('\nBot: Tiene comprobante o factura del gasto?')
    print('     1. Si, tengo factura')
    print('     2. Si, tengo ticket/recibo')
    print('     3. No tengo comprobante')

    while True:
        opcion = input('\nUsuario: ').strip()
        if opcion.lower() == 'salir':
            estado = 'cancelado'
            print('Bot: Proceso cancelado.')
            return
        if opcion == '1':
            comprobante = 'Factura'
            estado = 'comprobante_confirmado'
            break
        elif opcion == '2':
            comprobante = 'Ticket/recibo'
            estado = 'comprobante_confirmado'
            break
        elif opcion == '3':
            estado = 'cancelado_sin_comprobante'
            print('Bot: No es posible procesar una rendicion sin comprobante.')
            print('Bot: Proceso cancelado.')
            return
        else:
            print('Bot: Opcion invalida. Ingrese 1, 2 o 3.')

    # PASO 5: Evaluacion y decision (Gateways del BPMN)
    estado = 'evaluando'
    print('\nBot: Procesando solicitud...')

    # Gateway 1: hay presupuesto disponible?
    if monto > empleado['presupuesto_disponible']:
        estado = 'rechazado_sin_presupuesto'
        resultado = 'RECHAZADO - Sin presupuesto'
        print(f'\nBot: SOLICITUD RECHAZADA.')
        print(f'Bot: El monto ${monto:,.2f} supera su presupuesto disponible (${empleado["presupuesto_disponible"]:,}).')
        print('Bot: Contacte a su jefe de area para gestionar una ampliacion.')

    # Gateway 2: aprobacion automatica?
    elif monto <= limite_auto:
        estado = 'aprobado_automaticamente'
        resultado = 'APROBADO AUTOMATICAMENTE'
        for emp in empleados:
            if emp['id'] == empleado['id']:
                emp['presupuesto_disponible'] -= int(monto)
                emp['gastos_acumulados']      += int(monto)
                break
        guardar_empleados(empleados)
        print(f'\nBot: SOLICITUD APROBADA.')
        print(f'Bot: Monto: ${monto:,.2f}')
        print(f'Bot: El reembolso se acreditara en su proximo recibo de sueldo.')

    # Gateway 3: requiere supervisor?
    elif monto <= limite_supervisor:
        estado = 'pendiente_supervisor'
        resultado = 'PENDIENTE - Requiere aprobacion de supervisor'
        print(f'\nBot: SOLICITUD EN REVISION.')
        print(f'Bot: El monto ${monto:,.2f} requiere aprobacion de su supervisor.')
        print('Bot: Recibira una respuesta en 48 horas habiles.')

    # Gateway 4: monto excede el limite maximo
    else:
        estado = 'rechazado_limite_maximo'
        resultado = 'RECHAZADO - Supera limite maximo'
        print(f'\nBot: SOLICITUD RECHAZADA.')
        print(f'Bot: El monto ${monto:,.2f} supera el limite maximo permitido (${limite_supervisor:,}).')
        print('Bot: Gestione esta rendicion directamente en el area de Finanzas.')

    registrar_historial(empleado, concepto, monto, resultado)

    # PASO 6: Resumen final
    estado = 'finalizado'
    print(f'\n--- RESUMEN ---')
    print(f'  Empleado:    {empleado["nombre"]}')
    print(f'  Concepto:    {concepto}')
    print(f'  Monto:       ${monto:,.2f}')
    print(f'  Comprobante: {comprobante}')
    print(f'  Resultado:   {resultado}')


# ============================================================
# CONSULTA DE PRESUPUESTO
# ============================================================

def consultar_presupuesto(empleados):
    print('\n--- CONSULTA DE PRESUPUESTO ---')
    id_ingresado = input('Bot: Ingrese su ID de empleado: ').strip().upper()

    empleado = None
    for emp in empleados:
        if emp['id'] == id_ingresado:
            empleado = emp
            break

    if empleado is None:
        print(f'Bot: No se encontro el empleado con ID "{id_ingresado}".')
        return

    print(f'\n  Nombre:                 {empleado["nombre"]}')
    print(f'  Departamento:           {empleado["departamento"]}')
    print(f'  Presupuesto disponible: ${empleado["presupuesto_disponible"]:,}')
    print(f'  Gastos acumulados:      ${empleado["gastos_acumulados"]:,}')


# ============================================================
# MENÚ PRINCIPAL
# ============================================================

def menu_principal():
    print('''
╔══════════════════════════════════════════════╗
║   PRIMOSTECH — BOT DE RENDICIÓN DE GASTOS    ║
╚══════════════════════════════════════════════╝
Escriba "salir" en cualquier momento para cancelar.
''')

    empleados = cargar_empleados()

    if len(empleados) == 0:
        print('ERROR: No hay empleados cargados. Verifique el archivo CSV.')
        return

    while True:
        print('''
--- MENU PRINCIPAL ---
1. Nueva rendicion de gastos
2. Consultar presupuesto disponible
3. Salir''')

        opcion = input('\nSeleccione una opcion: ').strip()

        if opcion == '1':
            iniciar_rendicion(empleados)
        elif opcion == '2':
            consultar_presupuesto(empleados)
        elif opcion == '3':
            print('\nBot: Hasta luego.')
            break
        else:
            print('Bot: Opcion invalida. Ingrese 1, 2 o 3.')


# Punto de entrada del programa
menu_principal()