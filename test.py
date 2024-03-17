import flet as ft

from src.helper import update_text, update_control, load_text

from src.gpt_vision import view_image
from src.img_convert import image_to_base64str


def main(page: ft.Page):
    files_raw_list = []
    files_controls_list = []
    system_prompt = load_text("default_system_prompt.txt")

    def highlight_img(event):
        event.control.bgcolor = "red" if event.data == "true" else "grey"
        event.control.update()

    def remove_img(event):
        this_container = event.control

        for f in files_raw_list:
            if f.path == this_container.content.src:
                files_raw_list.remove(f)
                break

        files_controls_list.remove(this_container)
        file_col.controls = files_controls_list
        file_col.update()

        img_count = len(files_controls_list)
        uploaded_files_counter.value = img_count
        uploaded_files_counter.update()

    def pick_files_result(event: ft.FilePickerResultEvent):
        if event.files:
            for f in event.files:
                files_raw_list.append(f)
                image_container = ft.Container(
                    content=ft.Image(src=f.path),
                    width=150,
                    height=150,
                    padding=10,
                    bgcolor="blue",
                    on_hover=highlight_img,
                    on_click=remove_img,
                )
                files_controls_list.append(image_container)

            file_col.controls = files_controls_list
            update_control(file_col)

            img_count = len(files_controls_list)
            uploaded_files_counter.value = img_count
            update_control(uploaded_files_counter, visible=True)

            upload_file_button.bgcolor = "blue"
            upload_file_button.update()

    def call_vision(event):
        prompt = input_field.value

        if prompt:
            input_field.border_color = "blue"
            input_field.update()

        if prompt and files_raw_list:
            b64_images = [image_to_base64str(image_source=img.path, file_type="JPEG") for img in files_raw_list]

            gpt_response = view_image(
                images_in_base64str=b64_images, user_prompt=prompt, system_prompt=system_prompt, max_tokens=300
            )
            if output_field.value:
                output_field.value += "\n\n\n"
            output_field.value += f"VISION:\n------\n\n{gpt_response}"
            update_control(output_field)
        if not prompt.strip():
            input_field.border_color = "red"
            input_field.update()
        if not files_raw_list:
            upload_file_button.bgcolor = "red"
            upload_file_button.update()

    def open_settings(event):
        update_control(full_row, visible=False, disabled=True)
        update_control(system_prompt_view, visible=True, disabled=False)

    def close_settings(event):
        nonlocal system_prompt
        system_prompt = system_prompt_field.value
        update_control(system_prompt_view, visible=False, disabled=True)
        update_control(full_row, visible=True, disabled=False)

    # page.theme_mode = ft.ThemeMode.LIGHT

    # file picker
    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_files_dialog)
    upload_file_button = ft.FilledButton(
        text="Pick Files",
        icon=ft.icons.UPLOAD_ROUNDED,
        on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=True),
        height=42,
    )
    upload_file_button.bgcolor = "blue"
    uploaded_files_counter = ft.Text(visible=False)

    # text input
    input_field = ft.TextField(label="Input prompt", on_submit=call_vision, width=500, border_width=1)

    # text output
    output_field = ft.TextField(
        value="",
        width=600,
        height=300,
        multiline=True,  # scrollable
        read_only=True,  # only output
        border_width=1,
    )

    # system prompt edit
    system_prompt_field = ft.TextField(
        value=system_prompt,
        multiline=True,
        height=600,
    )
    submit_button = ft.IconButton(icon=ft.icons.CHECK_BOX_ROUNDED, on_click=close_settings)
    system_prompt_view = ft.Column(controls=[system_prompt_field, submit_button], visible=False, disabled=True)
    settings_button = ft.IconButton(icon=ft.icons.SETTINGS, on_click=open_settings)

    # structure
    upload_row = ft.Row(controls=[upload_file_button, uploaded_files_counter])
    file_col = ft.Column()

    input_row = ft.Row(controls=[settings_button, input_field])

    left_col = ft.Column(controls=[upload_row, file_col])
    right_col = ft.Column(controls=[output_field, input_row])

    full_row = ft.Row(controls=[left_col, right_col])

    page.add(full_row)
    page.add(system_prompt_view)


if __name__ == "__main__":
    ft.app(target=main)
