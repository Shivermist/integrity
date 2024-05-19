from taipy.gui import Gui, notify
import taipy.gui.builder as tgb
import re

devposturl = ""


def on_change(state, var_name, var_value):
    print(f"Variable {var_name} changed to {var_value}")
    return state


def on_submit_button_clicked(state):
    print(state.devposturl, type(state.devposturl))

    url = state.devposturl
    print("URL is", url)

    if not re.match(r"https://devpost.com/.*", url):
        notify("Invalid URL", "Please enter a valid Devpost URL")
        return state

    return state


with tgb.Page() as page:
    with tgb.layout(columns="1 2"):
        with tgb.part():
            tgb.text(value="# Taipy Getting Started", mode="md")
            tgb.text(value="Devpost URL:")
            with tgb.layout(columns="1 1", class_name="button_thing"):
                tgb.input(
                    "{devposturl}",
                )
                tgb.button("Investigate!", on_action=on_submit_button_clicked)

        with tgb.part():
            # tgb.text("lkdsajflak {devposturl}")
            pass


if __name__ == "__main__":
    g = Gui(page)
    g.run(title="Dynamic chart", debug=True, port=8000, use_reloader=True)
