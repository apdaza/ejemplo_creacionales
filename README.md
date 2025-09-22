# Ejemplo de logs de creación de juego

Patrones creacionales cubiertos:
- Singleton: GameConfig, GameEngine
- Abstract Factory: ThemeFactory (Fantasy/SciFi)
- Factory Method: EnemyFactory
- Prototype: EnemyPrototypeRegistry
- Builder: LevelBuilder

# 1) Clases y responsabilidades

## `Singleton` (metaclase)

* **Qué es:** utilería para garantizar **una sola instancia** por clase que la use.
* **Cómo funciona:** sobreescribe `__call__` y guarda la instancia en `_instances`. Si ya existe, la reutiliza.

## `GameConfig` *(Singleton)*

* **Rol:** configuración global del juego.
* **Campos:** `theme` (fantasy/scifi), `max_enemies`, `level`.
* **Por qué Singleton:** toda la app debe leer/escribir la **misma** configuración.

## `GameEngine` *(Singleton)*

* **Rol:** estado vivo del juego.
* **Campos:** `enemies` (lista de `Enemy`), `background`, `skin_palette` (mapa tipo→skin).
* **Métodos:** `reset()` limpia enemigos.
* **Por qué Singleton:** centraliza el **estado compartido** entre peticiones.

## `ThemeFactory` (Protocolo) + `FantasyThemeFactory` / `SciFiThemeFactory`

* **Rol:** **Abstract Factory** para producir “familias” de elementos de tema.
* **Métodos:**

  * `create_background()` → string del fondo.
  * `create_skin_palette()` → diccionario tipo→skin.
* **get\_theme\_factory(theme):** selector de la factory concreta (fantasy/scifi).

## `Enemy` (dataclass) + `clone()`

* **Rol:** entidad enemigo.
* **Campos:** `kind`, `hp`, `atk`, `skin`.
* **Prototype:** `clone()` devuelve una **copia profunda** (deepcopy) del enemigo base.

## `EnemyPrototypeRegistry` *(Singleton)*

* **Rol:** **catálogo de prototipos** de enemigos.
* **Campos:** `_protos` con plantillas base (`orc`, `dragon`, `goblin`, `drone`, etc.).
* **Métodos:** `get(kind)` → clona el prototipo (o error si no existe).
* **Por qué Singleton:** un único catálogo consistente.

## `EnemyFactory` (Factory Method)

* **Rol:** **punto único** de creación de enemigos.
* **Flujo:**

  1. Pide un clon al `EnemyPrototypeRegistry` (Prototype).
  2. Lee `GameEngine().skin_palette` y aplica la **skin** según el tema.
  3. Devuelve el enemigo listo.

## `Level` (dataclass)

* **Rol:** producto final de la construcción de niveles.
* **Campos:** `number`, `goal`, `background`, `enemy_wave`.

## `LevelBuilder` (Builder)

* **Rol:** construir un `Level` paso a paso (fluent API).
* **Pasos típicos:** `with_number()`, `with_goal()`, `with_background()`, `add_enemy()`, `build()`.
* **Valor:** evita “constructores telescópicos” y mantiene **invariantes** (fondo por defecto si falta).
