# Feature Specification: Galton Simulator Implementation

**Feature Branch**: `001-galton-sim`  
**Created**: 2025-10-27  
**Status**: Draft  
**Input**: User description: "Nombre del proyecto galton_sim Objetivo funcional Simular la caída de N bolas a través de un tablero tipo Galton con L niveles de clavos y reportar cuántas bolas terminan en cada contenedor de salida, mostrando la distribución resultante numérica y (opcionalmente) gráfica. Requisitos funcionales (qué debe hacer) Simulación básica Entrada: num_bolas (int > 0) num_niveles (int > 0) p_derecha (float entre 0 y 1, default 0.5) seed (int | None) Proceso: Cada bola \"rebota\" num_niveles veces. En cada rebote decide ir derecha con probabilidad p_derecha, izquierda en caso contrario. La posición final de la bola corresponde al número total de \"derechas\". Salida (estructura de datos): Lista/array counts[columna] = cantidad_de_bolas_en_esa_columna. Número de columnas = num_niveles + 1. Métricas estadísticas Calcular y devolver: media empírica (en términos de posición final) varianza empírica proporción relativa por columna (frecuencia / N) Visualización en texto Generar un histograma ASCII/barra textual en consola para ver la forma de campana sin necesidad de entorno gráfico. Visualización gráfica (opcional) Función que use matplotlib para graficar barras counts. Eje X: índice de columna (0 … num_niveles). Eje Y: conteo de bolas. Título con parámetros de simulación. Interfaz de ejecución directa Si se ejecuta python galton_sim.py desde terminal: Leer argumentos por CLI (por ejemplo con argparse). Correr la simulación. Imprimir resumen: parámetros tabla columna → conteo media, varianza Imprimir histograma ASCII. Bandera --plot para mostrar gráfica. Requisitos no funcionales (cómo debe ser) Determinismo controlado Si el usuario pasa --seed 123, la simulación debe ser exactamente reproducible. Performance razonable Debe manejar al menos num_bolas = 100000 y num_niveles = 20 en <1s en un portátil típico actual (orden de magnitud; buscamos eficiencia O(N·L) sin cosas raras). Código legible Nombres claros en inglés (num_balls, num_levels, etc.). Docstrings tipo \"qué hace / qué retorna\". Comentarios explicando la lógica probabilística. Modularidad Núcleo de simulación en una función pura (simulate_galton(...)) sin prints. Renderizadores separados: render_ascii(counts) render_plot(counts, ...) Sin acoplar salida a interfaz La parte matemática no debe depender de matplotlib ni de argparse. Eso permite reusar el motor en otros frontends (por ejemplo, notebook educativo o app web ligera en el futuro). Criterios de aceptación (Definition of Done inicial) Ejecutar python galton_sim.py --balls 5000 --levels 10 produce: Conteo por columna (11 columnas). Histograma ASCII visible con forma aproximadamente \"de campana\". Media empírica cercana a levels * p_derecha. Varianza empírica cercana a levels * p_derecha * (1 - p_derecha). Ejecutar con --plot abre una gráfica de barras sin crashear. Cambiar --p_right 0.7 desplaza la distribución hacia la derecha (asimetría visible en los conteos)."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Run Basic Simulation (Priority: P1)

As a student learning probability, I want to run a Galton board simulation with default parameters to observe the binomial distribution emerging as a normal distribution.

**Why this priority**: This is the core functionality that delivers the primary educational value.

**Independent Test**: Can be fully tested by running the program with default parameters and verifying the output shows counts, mean, variance, and ASCII histogram.

**Acceptance Scenarios**:

1. **Given** the program is executed with default parameters, **When** the simulation runs, **Then** it produces a counts array with num_levels + 1 columns, empirical mean, variance, and an ASCII histogram.
2. **Given** default parameters (num_balls=1000, num_levels=10, p_right=0.5, seed=None), **When** the simulation completes, **Then** the mean is approximately 5.0 and variance approximately 2.5.

---

### User Story 2 - Vary Simulation Parameters (Priority: P2)

As a teacher demonstrating probability concepts, I want to change the number of balls, levels, and bias probability to show how these affect the distribution.

**Why this priority**: Enables interactive exploration of probability parameters, supporting educational use cases.

**Independent Test**: Can be tested by running with different parameter combinations and verifying the distribution changes accordingly.

**Acceptance Scenarios**:

1. **Given** p_right=0.7, **When** the simulation runs, **Then** the mean shifts to approximately levels * 0.7 and the distribution is skewed right.
2. **Given** increased num_levels=20, **When** the simulation runs, **Then** the variance increases and the distribution spreads more.

---

### User Story 3 - Generate Graphical Visualization (Priority: P3)

As a user wanting visual representation, I want to optionally generate a matplotlib plot of the distribution.

**Why this priority**: Provides visual aid for understanding, but not essential for core functionality.

**Independent Test**: Can be tested by running with --plot flag and verifying a plot window appears without errors.

**Acceptance Scenarios**:

1. **Given** --plot flag is used, **When** the program runs, **Then** a matplotlib bar chart displays with correct x-axis (column indices), y-axis (counts), and title including simulation parameters.
2. **Given** --plot flag, **When** the simulation completes, **Then** the plot shows the bell-shaped curve for symmetric parameters.

---

### Edge Cases

- What happens when num_balls = 0? Should reject input with error message.
- How does system handle num_levels = 0? Should produce 1 column with all balls.
- What if p_right = 0.0 or 1.0? Should produce deterministic distributions (all left or all right).
- How to handle invalid seed values? Should accept integers or None.
- Performance with large inputs: num_balls=100000, num_levels=20 should complete in <1 second.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept input parameters: num_balls (int > 0), num_levels (int >= 0), p_right (float 0-1, default 0.5), seed (int or None).
- **FR-002**: System MUST simulate each ball's path through num_levels decisions, each going right with probability p_right.
- **FR-003**: System MUST return a counts array where counts[column] = number of balls in that column (columns = num_levels + 1).
- **FR-004**: System MUST calculate and return empirical mean and variance of final positions.
- **FR-005**: System MUST generate an ASCII histogram displaying the distribution in text form.
- **FR-006**: System MUST optionally generate a matplotlib bar plot when requested.
- **FR-007**: System MUST provide a CLI interface using argparse for parameter input and output display.
- **FR-008**: System MUST ensure reproducible results when a seed is provided.
- **FR-009**: System MUST perform simulation in O(N*L) time for N balls and L levels.
- **FR-010**: Code MUST be modular with pure simulation function, separate rendering functions, and no coupling between math and UI.

### Key Entities *(include if feature involves data)*

- **Simulation Parameters**: Input values (num_balls, num_levels, p_right, seed) that control the simulation.
- **Simulation Results**: Output data (counts array, mean, variance, proportions) derived from the simulation.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Simulation with 100,000 balls and 20 levels completes in under 1 second on typical laptop hardware.
- **SC-002**: For symmetric parameters (p_right=0.5), empirical mean is within 0.1 of expected value (levels * 0.5) and variance within 0.1 of expected (levels * 0.25).
- **SC-003**: ASCII histogram displays correctly with proportional bar heights for all parameter combinations.
- **SC-004**: Graphical plot generates without errors and shows correct bar chart with appropriate labels and title.
- **SC-005**: Identical seeds produce identical results across multiple runs.
- **SC-006**: Code achieves 90%+ test coverage for simulation logic.
