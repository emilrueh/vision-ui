import flet as ft

from src.gpt_vision import view_image
from src.img_convert import image_to_base64str
from src.helper import update_text, update_control, load_text


# MAIN APP
def main(page: ft.Page):
    # APP LOGIC
    # ---------

    CUSTOM_PROMPT = ""
    system_prompt = load_text("default_system_prompt.txt")
    SELECTED_IMAGES = []
    SELECTED_IMAGES_MSG = ""

    def pick_files_result(event: ft.FilePickerResultEvent):
        nonlocal SELECTED_IMAGES_MSG

        if event.files:
            for s_img in event.files:
                SELECTED_IMAGES.append(s_img)
                SELECTED_IMAGES_MSG += f"{s_img.name}\n"

            update_text(notification_field, SELECTED_IMAGES_MSG)
            update_control(notification_field, visible=True, disabled=False)

        if not SELECTED_IMAGES:
            handle_missing_input()

    def call_vision(event):
        nonlocal CUSTOM_PROMPT
        nonlocal system_prompt

        CUSTOM_PROMPT = prompt_input_field.value

        if CUSTOM_PROMPT and SELECTED_IMAGES:
            base64_images = []

            for img in SELECTED_IMAGES:
                base64_images.append(image_to_base64str(image_source=img.path, file_type="JPEG"))

            prepare_for_vision()

            gpt_response = view_image(
                images_in_base64str=base64_images, user_prompt=CUSTOM_PROMPT, system_prompt=system_prompt, max_tokens=300
            )
            update_text(output_field, gpt_response)

            unprepare_from_vision()

        else:
            handle_missing_input()

    # EVENT HANDLERS
    # --------------

    def prepare_for_vision():
        # disble input
        update_control(upload_file_button, disabled=True)
        update_control(prompt_input_field, disabled=True)
        # hide output
        update_control(output_field, visible=False, disabled=True)
        # display progress
        update_text(notification_field, "Calling OpenAI Vision API...", "green")
        update_control(progress_bar, visible=True)

    def unprepare_from_vision():
        # hide progress
        update_control(notification_field, visible=False)
        update_control(progress_bar, visible=False)
        # display output
        update_control(output_field, visible=True, disabled=False)
        # enable input
        update_control(upload_file_button, disabled=False)
        update_control(prompt_input_field, disabled=False)

    def handle_missing_input():
        warning = []
        if not CUSTOM_PROMPT:
            warning.append("No prompt input")
        if not SELECTED_IMAGES:
            warning.append("No images selected")
        warning_msg = "\n".join(warning) if len(warning) > 1 else warning[0]

        update_text(notification_field, warning_msg, "yellow")
        update_control(notification_field, visible=True, disabled=False)

    # UI ELEMENTS
    # -----------

    page.title = "GPT-Vision UI"

    notification_field = ft.Text(value="", width=630)
    # file picker
    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_files_dialog)
    upload_file_button = ft.ElevatedButton(
        text="Select File", on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=True), height=50
    )
    # vision call
    prompt_input_field = ft.TextField(label="Input Prompt", on_submit=call_vision, width=500)
    output_field = ft.TextField(
        value="",
        width=630,
        height=300,
        multiline=True,  # scrollable
        read_only=True,  # only output
        border_width=0,
    )
    progress_bar = ft.ProgressBar(visible=False, color="green", width=630)

    # structure
    input_row = ft.Row(controls=[upload_file_button, prompt_input_field], spacing=10, alignment="center")
    complete_column = ft.Column(
        controls=[input_row, notification_field, progress_bar, output_field],
        spacing=10,
        horizontal_alignment="center",
    )

    page.add(complete_column)


if __name__ == "__main__":
    ft.app(target=main)
