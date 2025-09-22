# app.py

from flask import Flask, jsonify, request, render_template
from models import (
    GameConfig, GameEngine, get_theme_factory,
    LevelBuilder, EnemyFactory
)

app = Flask(__name__)
engine = GameEngine()


def _apply_theme(theme: str) -> None:
    cfg = GameConfig()
    cfg.theme = theme
    factory = get_theme_factory(theme)
    engine.background = factory.create_background()
    engine.skin_palette = factory.create_skin_palette()


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/set-theme")
def set_theme():
    data = request.get_json(silent=True) or {}
    theme = data.get("theme", "fantasy")
    _apply_theme(theme)
    return jsonify(message=f"Tema cambiado a {theme} (Abstract Factory)", state=_state())


@app.post("/reset")
def reset():
    engine.reset()
    return jsonify(message="Juego reiniciado (Singleton mantiene config)", state=_state())


@app.get("/state")
def state():
    return jsonify(_state())


@app.post("/build-level")
def build_level():
    cfg = GameConfig()
    factory = get_theme_factory(cfg.theme)
    builder = (
        LevelBuilder()
        .with_number(cfg.level)
        .with_goal("Elimina la oleada")
        .with_background(factory.create_background())
    )
    if cfg.theme == "fantasy":
        builder.add_enemy("orc").add_enemy("goblin")
    else:
        builder.add_enemy("drone").add_enemy("android")
    level = builder.build()
    engine.background = level.background
    return jsonify(message=f"Nivel {level.number} construido (Builder)", state=_state())


@app.post("/spawn/<kind>")
def spawn(kind: str):
    cfg = GameConfig()
    if len(engine.enemies) >= cfg.max_enemies:
        return jsonify(message="No puedes crear más enemigos, límite alcanzado.", state=_state())
    try:
        enemy = EnemyFactory.create(kind)
    except ValueError as e:
        return jsonify(message=str(e), state=_state())
    engine.enemies.append(enemy)
    return jsonify(message=f"Enemigo '{kind}' creado (Factory Method + Prototype)", state=_state())


def _state():
    cfg = GameConfig()
    return {
        "theme": cfg.theme,
        "level": cfg.level,
        "background": engine.background,
        "enemies": [e.__dict__ for e in engine.enemies],
    }


if __name__ == "__main__":
    _apply_theme(GameConfig().theme)  # Abstract Factory al iniciar
    app.run(debug=True)