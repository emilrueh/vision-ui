import flet as ft

from src.gpt_vision import view_image
from src.img_convert import image_to_base64str


def update_text(control, value="", color="white", visible=True):
    control.value = value
    control.color = color
    control.visible = visible
    control.update()


def update_control(control, visible=True, disabled=False):
    control.visible = visible
    control.disabled = disabled
    control.update()


def main(page: ft.Page):
    page.title = "GPT-Vision UI"

    selected_images = []
    base64_images = []
    image_verification = "Selected images:\n"

    def pick_files_result(event: ft.FilePickerResultEvent):
        nonlocal image_verification

        update_text(output_field, visible=False)

        if event.files:
            for s_img in event.files:
                selected_images.append(s_img)
                image_verification += f"{s_img.name}\n"
            update_text(notification_field, image_verification)

        if not selected_images:
            update_text(notification_field, "No file selected", "yellow")

    def call_vision(event):
        custom_prompt = prompt_input_field.value
        if custom_prompt and selected_images:
            for img in selected_images:
                base64_images.append(image_to_base64str(image_source=img.path, file_type="JPEG"))

            # preparing for output
            # disabling input for duration of api call
            update_control(upload_file_button, disabled=True)
            update_control(prompt_input_field, disabled=True)

            # displaying progress
            update_text(notification_field, "Calling OpenAI Vision API...", "green")

            update_control(progress_bar, visible=True)

            # receiving output
            gpt_response = view_image(images_in_base64str=base64_images, user_prompt=custom_prompt, max_tokens=300)

            update_text(output_field, gpt_response)
            update_text(notification_field, visible=False)
            update_control(progress_bar, visible=False)

            # enabling input fields on api response
            update_control(upload_file_button, disabled=False)
            update_control(prompt_input_field, disabled=False)

        else:
            if not custom_prompt:
                update_text(notification_field, "No prompt input", "yellow")
            elif not selected_images:
                update_text(notification_field, "No images selected", "yellow")

    # UI ELEMENTS

    # notifications
    notification_field = ft.Text(value="", width=630)

    # picking files
    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_files_dialog)
    upload_file_button = ft.ElevatedButton(
        text="Select File", on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=True), height=50
    )

    # calling vision
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

    # aligning elements
    input_row = ft.Row(controls=[upload_file_button, prompt_input_field], spacing=10, alignment="center")
    complete_column = ft.Column(
        controls=[input_row, notification_field, progress_bar, output_field],
        spacing=10,
        horizontal_alignment="center",
    )

    page.add(complete_column)


if __name__ == "__main__":
    ft.app(target=main)
