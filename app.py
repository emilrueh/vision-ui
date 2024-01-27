import flet as ft

from src.gpt_vision import view_image
from src.img_convert import image_to_base64str


def main(page: ft.Page):
    page.title = "GPT-Vision UI"

    selected_images = []
    base64_images = []
    image_verification = "Selected images:\n"

    def pick_files_result(e: ft.FilePickerResultEvent):
        nonlocal image_verification

        if e.files:
            for s_img in e.files:
                selected_images.append(s_img)
                image_verification += f"{s_img.name}\n"
            response_output_field.value = image_verification
        else:
            response_output_field.value = "No file selected"

        response_output_field.update()

    def call_vision(event):
        custom_prompt = prompt_input_field.value
        if custom_prompt and selected_images:
            for img in selected_images:
                base64_images.append(image_to_base64str(image_source=img.path, file_type="JPEG"))

            response_output_field.value = "Calling OpenAI Vision API..."
            response_output_field.update()

            gpt_response = view_image(images_in_base64str=base64_images, user_prompt=custom_prompt, max_tokens=300)
            response_output_field.value = gpt_response

        elif not custom_prompt:
            response_output_field.value = "No prompt input"
        elif not selected_images:
            response_output_field.value = "No images selected"

        response_output_field.update()

    # picking files
    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_files_dialog)
    upload_file_button = ft.ElevatedButton(
        text="Select File", on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=True), height=50
    )

    # calling vision
    prompt_input_field = ft.TextField(label="Input Prompt", on_submit=call_vision, width=500)
    response_output_field = ft.TextField(
        value="",
        width=630,
        height=300,
        multiline=True,  # scrollable
        read_only=True,  # only used for output
        border_width=0,
    )

    # aligning elements
    input_row = ft.Row(controls=[upload_file_button, prompt_input_field], spacing=10, alignment="center")
    complete_column = ft.Column(
        controls=[input_row, response_output_field], spacing=10, horizontal_alignment="center"
    )

    page.add(complete_column)


if __name__ == "__main__":
    ft.app(target=main)
