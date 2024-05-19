from taipy.gui import Gui
import taipy.gui.builder as tgb
from math import cos, exp


value = 10


def compute_data(decay: int) -> list:
    return [cos(i / 6) * exp(-i * decay / 600) for i in range(100)]


def on_slider(state):
    state.data = compute_data(state.value)


with tgb.Page() as page:
    tgb.text(value="# Taipy Getting Started", mode="md")
    tgb.text(value="Value: {value}")
    tgb.slider(value="{value}", on_change=on_slider)
    tgb.chart(data="{data}")

data = compute_data(value)

if __name__ == "__main__":
    Gui(page=page).run(title="Dynamic chart")
