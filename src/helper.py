def update_text(control, value="", color="white"):
    control.value = value
    control.color = color
    control.update()


def update_control(control, visible=True, disabled=False):
    control.visible = visible
    control.disabled = disabled
    control.update()


def load_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()
