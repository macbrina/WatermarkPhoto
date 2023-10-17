from tkinter import StringVar
from effects import common_colors_hex, filter_buttons, enhance_buttons


class ImagePreference:
    def __init__(self):
        self.background_image_tk = None
        self.image_canvas_id = None
        self.preview_size = (650, 650)
        self.image_path = ""
        self.overlay_rotation = 0
        self.opacity = 100
        self.background_pil = None
        self.background_image = None
        self.overlay_image = None
        self.selected_image_path = None
        self.watermark_selected = False
        self.watermark_path = None
        self.watermark_pil = None
        self.selected_color = StringVar()
        self.filters = filter_buttons
        self.color_names = common_colors_hex
        self.enhance_buttons = enhance_buttons
        self.applied_filter = None
        self.applied_color = None
        self.default_color = "#ffffff"
        self.applied_enhancement = None
        self.drag_data = {"x": 0, "y": 0}
        self.saved_overlay_image = None
        self.default_size_factor = 1 / 6
        self.new_size_factor = self.default_size_factor
        self.display_size = 1.0
        self.watermark_edits = {
            "position": "Bottom Right",
            "padding": 1 / 40
        }

        self.docs = [
            "Welcome to the Watermark App! This guide will help you understand how to use the app to add watermarks "
            "to your photos effectively.",
            "Uploading Images:",
            "1. Background Image:",
            "- Click the 'Select Images' button.",
            "- Select the image you want to use as the background and click 'Open.'",
            "- The selected background image will be displayed on the canvas.",
            "2. Watermark Image:",
            "- Click the 'Select Watermark' button.",
            "- Choose the image you want to use as a watermark and click 'Open.'",
            "Editing Watermarks:",
            "3. Edit Watermark:",
            "- You can edit the watermark by adjusting various properties:",
            "- Rotation: Enter the rotation angle in degrees.",
            "- Opacity: Set the opacity level (0-255).",
            "- Colors: Apply color changes to the watermark if needed.(You can also enter the HEX code of the color "
            "in the entry box)",
            "- Size: Increase or decrease the size as desired.",
            "- Filters: Apply filters to the watermark for artistic effects.",
            "- Position: Change the position by dragging the watermark on the canvas.",
            "4. Edit Multiple Images:",
            "- To edit multiple images with the same watermark, follow the same steps for each image.",
            "- Make sure you upload the background image and watermark for each photo separately.",
            "Saving Images:",
            "5. Save Edited Images:",
            "- To save a single edited image, click the 'Save Current Image' button after making your desired "
            "adjustments.",
            "- Choose a location on your computer to save the image.",
            "6. Save Multiple Images:",
            "- To save multiple edited images, make sure you've edited and saved each image individually.",
            "- Click the 'Save All Images' button to save all the edited images in the same directory.",
            "Managing Images:",
            "7. Manage Images:",
            "- You can add, delete, or edit multiple photos.",
            "- To delete a photo, select the photo and click the 'Delete' button.",
            "- To edit a photo, make sure it's loaded in the canvas, and follow the steps to edit the watermark.",
            "User-Friendly Layout:",
            "8. User-Friendly GUI:",
            "- The app is designed with user-friendliness in mind.",
            "- Labels and input fields are provided to guide you through the watermark editing process.",
            "Enjoy Watermarking!",
            "With the Watermark App, you can easily add watermarks to your photos, customize them to your liking, "
            "and save them effortlessly. Have fun watermarking your images and protecting your work!",
            "If you encounter any issues or need assistance, feel free to refer to "
            "the app's help section or contact "
            "the support team for further guidance."
        ]
