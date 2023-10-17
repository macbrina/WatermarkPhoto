import os
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageChops
from watermark_app import WatermarkApp


class WatermarkLogo(WatermarkApp):
    def __init__(self):
        super().__init__()

        # Docs Menu
        self.button_howto = ttk.Button(self.buttons_frame, text="How to Use", command=self.doc_instructions)
        self.button_howto.grid(row=1, column=4, padx=3)

    def upload_watermark(self):
        if self.img_pref.background_image_tk is None:
            messagebox.showerror("Select an image", f"Please select atleast one image")
        else:
            watermark_path = filedialog.askopenfilename(
                title="Select Logo",
                filetypes=[("Image files", ".jpg *.jpeg *.png *.gif *.bmp *.tiff")]
            )
            if watermark_path:
                self.img_pref.watermark_selected = True
                self.img_pref.watermark_path = watermark_path
                self.img_pref.watermark_pil = Image.open(watermark_path)
                self.img_pref.overlay_image = self.img_pref.watermark_pil.copy()

                # Update the canvas background
                self.update_canvas_background()
                self.open_image_properties()

    def list_images(self):
        photos = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[("Image files", ".jpg *.jpeg *.png *.gif *.bmp *.tiff")]
        )
        if photos:
            for photo in photos:
                clean_photo = photo.split("/")[-1]
                path_parts = photo.split("/")[:-1]
                directory_path = "/".join(path_parts)
                self.img_pref.selected_image_path = directory_path
                self.images_list.insert(END, clean_photo)
            if not self.img_pref.background_image_tk:
                self.images_list.select_set(0)
                self.preview_background_image(None)
            self.get_save_buttons()
            self.get_delete_buttons()
        self.images_list.bind("<<ListboxSelect>>", self.preview_background_image)

    def preview_background_image(self, event):
        selection = self.images_list.curselection()
        if selection:
            selected_img = self.images_list.get(selection)
            if selected_img and self.img_pref.watermark_selected:
                self.img_pref.image_path = f"{self.img_pref.selected_image_path}/{selected_img}"
                self.img_pref.background_pil = Image.open(self.img_pref.image_path)
                self.img_pref.background_image = self.img_pref.background_pil.copy()
                self.update_canvas_background()
            else:
                try:
                    # Show the background image preview
                    self.img_pref.image_path = f"{self.img_pref.selected_image_path}/{selected_img}"
                    self.img_pref.background_pil = Image.open(self.img_pref.image_path)
                    self.img_pref.background_image = self.img_pref.background_pil.copy()
                    self.img_pref.background_image.thumbnail(self.img_pref.preview_size)
                    self.img_pref.background_image_tk = ImageTk.PhotoImage(self.img_pref.background_image)
                    width, height = self.img_pref.background_image.size
                    self.background_canvas.config(width=width, height=height)
                    self.img_pref.image_canvas_id = self.background_canvas.create_image(int(width / 2), int(height / 2),
                                                                                        image=self.img_pref.background_image_tk)
                    self.image_frame.grid()
                    self.delete_frame.grid()
                    # self.open_image_properties()
                except Exception as e:
                    messagebox.showerror("Image Error", f"Error loading image: {str(e)}")

    def get_save_buttons(self):
        if self.images_list.size() == 1 and self.img_pref.watermark_path:
            self.save_current_image.config(text="Save Image")
            self.save_current_image.grid()
            self.save_all_images.grid_remove()
        elif self.images_list.size() > 1 and self.img_pref.watermark_path:
            self.save_current_image.config(text="Save Selected Image")
            self.save_current_image.grid()
            self.save_all_images.grid()
        elif self.images_list.size() < 1:
            self.save_current_image.grid_remove()
            self.save_all_images.grid_remove()
            self.delete_frame.grid_remove()

    def get_delete_buttons(self):
        if self.images_list.size() >= 1:
            self.delete_image.grid()
            if self.images_list.size() > 1:
                self.delete_all_images.grid()
            else:
                self.delete_all_images.grid_remove()
        else:
            self.delete_image.grid_remove()
            self.delete_all_images.grid_remove()

    def on_size_change(self, event):
        if self.img_pref.overlay_image:
            current_size = self.current_size.get()
            self.img_pref.new_size_factor = self.img_pref.default_size_factor * float(current_size)

            current_size = self.get_current_size()
            self.img_pref.display_size = current_size
            self.current_size_label.configure(text=current_size)
            self.update_canvas_background()

    def get_current_size(self):
        return '{:.1f}'.format(self.current_size.get())

    def on_opacity_change(self, opacity):
        if self.img_pref.overlay_image:
            opacity_size = self.get_opacity_size()
            self.img_pref.opacity = int(opacity_size)
            self.current_opacity_label.configure(text=f"{opacity_size}%")
            self.update_canvas_background()

    def get_opacity_size(self):
        return self.opacity_size.get()

    def create_color_grid(self, color_name, color_hex=None):
        if self.img_pref.overlay_image is not None:
            self.img_pref.selected_color.set(color_name)
            selected_color_hex = color_hex if color_hex else self.img_pref.color_names.get(color_name, color_name)
            self.color_display.config(bg=selected_color_hex)

            x = self.img_pref.overlay_image.width
            y = self.img_pref.overlay_image.height

            self.img_pref.overlay_image = self.img_pref.watermark_pil.copy()

            colored_overlay = Image.new("RGBA", (x, y), selected_color_hex)
            self.img_pref.overlay_image = ImageChops.multiply(self.img_pref.overlay_image, colored_overlay)

            self.color_entry.delete(0, END)
            self.color_entry.insert(END, string=self.img_pref.selected_color.get())
            self.img_pref.applied_color = selected_color_hex
            self.img_pref.default_color = selected_color_hex
        else:
            self.img_pref.applied_color = None
        self.update_canvas_background()

    def apply_opacity(self, image, opacity):
        if opacity is not None:
            opacity = float(opacity) / 100
            if image.mode != "RGBA":
                image = image.convert("RGBA")
            if "A" in image.getbands():
                alpha = image.split()[3]
                opacity_level = int(opacity * 255)
                new_alpha = alpha.point(lambda i: opacity_level if i > 0 else 0)
                image.putalpha(new_alpha)
        return image

    def apply_custom_color(self, event):
        custom_color_hex = self.color_entry.get()
        common_colors_hex = self.img_pref.color_names

        if custom_color_hex in common_colors_hex.values():
            self.create_color_grid(custom_color_hex)
        else:
            messagebox.showerror(title="Not Found", message="That color was not found. Try again")
        self.color_entry.delete(0, END)

    def remove_color(self):
        if self.img_pref.overlay_image is not None:
            if self.img_pref.applied_color:
                self.img_pref.overlay_image = self.img_pref.watermark_pil.copy()
                self.color_entry.delete(0, END)
                self.img_pref.applied_color = None
            self.update_canvas_background()

    def delete_current_image(self):
        selected_item = self.images_list.get(self.images_list.curselection())

        if selected_item:
            if messagebox.askokcancel("Confirm Delete", "Do you really want to delete the image?"):
                self.images_list.delete(self.images_list.curselection())
                messagebox.showinfo(title="Success", message="Image has been deleted")
        if self.images_list.size() >= 1:
            self.images_list.select_set(0)
            self.preview_background_image(None)
        else:
            self.images_list.selection_clear(0, END)
            self.background_canvas.delete("all")
            self.img_pref.overlay_image = None
            self.img_pref.watermark_selected = None
            self.image_frame.grid_remove()
            self.img_pref.background_image_tk = None
            if self.open_image_settings and self.img_pref.watermark_path is not None:
                self.settings_window.destroy()
        self.button_image_settings.grid_remove()
        self.get_save_buttons()
        self.get_delete_buttons()

    def clear_all_images(self):
        if messagebox.askokcancel("Confirm Delete", "Do you really want to delete the images?"):
            self.images_list.delete(0, END)
            self.background_canvas.delete("all")
            self.image_frame.grid_remove()
            self.img_pref.background_image_tk = None
            self.img_pref.watermark_selected = None
            self.img_pref.overlay_image = None
            if self.open_image_settings and self.img_pref.watermark_path is not None:
                self.settings_window.destroy()
            self.get_save_buttons()
            self.get_delete_buttons()
            self.button_image_settings.grid_remove()
            messagebox.showinfo(title="Success", message="Images has been deleted")

    def doc_instructions(self):
        self.listbox_frame.grid_remove()
        self.doc_frame.grid()

        for doc in self.img_pref.docs:
            self.doc_list.insert(END, doc)
        self.doc_list.config(state="disabled")
        self.button_howto.config(text="Hide Docs", command=self.hide_docs)

    def hide_docs(self):
        self.listbox_frame.grid()
        self.doc_frame.grid_remove()
        self.doc_list.delete(0, END)
        self.button_howto.config(text="How to Use", command=self.doc_instructions)

    def image_settings_toggle(self):
        if not self.open_image_settings and self.img_pref.background_image_tk is not None and self.img_pref.watermark_path is not None:
            self.open_image_properties()
        else:
            self.settings_window.attributes('-topmost', True)
            self.settings_window.attributes('-topmost', False)

    def on_rotation_change(self):
        """Rotate the watermark within the specified range"""
        if self.img_pref.overlay_image:
            rotation_angle = self.get_rotation_relay()
            if rotation_angle != self.img_pref.overlay_rotation:
                self.img_pref.overlay_rotation = rotation_angle
                self.update_canvas_background()

    def get_rotation_relay(self):
        return self.rotate_var.get()

    def apply_effect(self, effect_type):
        if self.img_pref.overlay_image is not None:
            self.img_pref.overlay_image = self.img_pref.watermark_pil.copy()
            if effect_type in self.img_pref.filters:
                self.img_pref.overlay_image = self.img_pref.overlay_image.filter(self.img_pref.filters[effect_type])
                self.img_pref.applied_filter = self.img_pref.filters[effect_type]
            elif effect_type in self.img_pref.enhance_buttons:
                self.img_pref.overlay_image = self.img_pref.enhance_buttons[effect_type](self.img_pref.overlay_image)
                self.img_pref.overlay_image = self.img_pref.overlay_image.enhance(1.5)
                self.img_pref.applied_enhancement = self.img_pref.enhance_buttons[effect_type]
        else:
            self.img_pref.applied_filter = None
            self.img_pref.applied_enhancement = None
        self.update_canvas_background()

    def on_remove_effect(self):
        """Removes the effect applied"""
        if self.img_pref.overlay_image is not None:
            if self.img_pref.applied_filter or self.img_pref.applied_enhancement:
                self.img_pref.overlay_image = self.img_pref.watermark_pil.copy()
                self.img_pref.applied_enhancement = None
                self.img_pref.applied_filter = None
            self.update_canvas_background()

    def change_watermark_position(self):
        self.img_pref.watermark_edits["position"] = self.current_position.get()
        self.update_canvas_background()

    def get_watermark_position(self, background_img, watermark):
        position = self.img_pref.watermark_edits["position"]
        padding = self.img_pref.watermark_edits["padding"]
        new_padding = int(background_img.width // (1 / padding))
        # Get the position
        if position == "Top Left":
            x_position = new_padding
            y_position = new_padding
        elif position == "Top Right":
            x_position = int(background_img.width - new_padding - watermark.width)
            y_position = new_padding
        elif position == "Bottom Right":
            x_position = int(background_img.width - new_padding - watermark.width)
            y_position = int(background_img.height - new_padding - watermark.height)
        elif position == "Center":
            x_position = int(background_img.width / 2 - watermark.width / 2)
            y_position = int(background_img.height / 2 - watermark.height / 2)
        else:
            x_position = new_padding
            y_position = int(background_img.height - new_padding - watermark.height)
        return x_position, y_position

    def process_image_edits(self, background_img, watermark):
        """Process the images and the edits"""
        # Get the watermark path and default size_factor
        default_size_factor = self.img_pref.new_size_factor

        # Get the width of the watermark relative to the background
        new_watermark_width = int(default_size_factor * background_img.width)

        # Get the height relative to the new width and resize it
        resize = new_watermark_width / watermark.width
        new_watermark_height = int(watermark.height * resize)
        new_watermark = watermark.resize((new_watermark_width, new_watermark_height))

        new_watermark = self.apply_final_edits(new_watermark)

        watermark_pos = self.get_watermark_position(background_img, new_watermark)

        new_background = background_img.copy()
        new_background.paste(new_watermark, watermark_pos, new_watermark)

        return new_background

    def apply_final_edits(self, new_watermark):
        if self.img_pref.applied_filter:
            new_watermark = new_watermark.filter(self.img_pref.applied_filter)

        if self.img_pref.applied_enhancement:
            new_watermark = self.img_pref.applied_enhancement(new_watermark)
            new_watermark = new_watermark.enhance(1.5)

        if hasattr(self.img_pref, 'opacity'):
            new_watermark = self.apply_opacity(new_watermark, self.img_pref.opacity)

        if self.img_pref.applied_color:
            x, y = new_watermark.width, new_watermark.height
            colored_overlay = Image.new("RGBA", (x, y), self.img_pref.applied_color)
            new_watermark = ImageChops.multiply(new_watermark, colored_overlay)

        if self.img_pref.overlay_rotation:
            new_watermark = new_watermark.rotate(self.img_pref.overlay_rotation, resample=Image.BILINEAR, expand=False)

        return new_watermark

    def update_canvas_background(self):
        """Update the watermark and edits on the Background image"""
        # Show the watermark on the canvas
        modified_image = self.process_image_edits(self.img_pref.background_pil, self.img_pref.overlay_image)
        self.img_pref.background_image = modified_image.copy()
        self.img_pref.background_image.thumbnail(self.img_pref.preview_size)
        self.img_pref.background_image_tk = ImageTk.PhotoImage(self.img_pref.background_image)
        width, height = self.img_pref.background_image.size
        self.background_canvas.config(width=width, height=height)
        self.img_pref.image_canvas_id = self.background_canvas.create_image(int(width / 2), int(height / 2),
                                                                            image=self.img_pref.background_image_tk)
        self.get_save_buttons()
        self.get_delete_buttons()
        self.image_frame.grid()
        self.delete_frame.grid()

    def reset_to_original_logo(self):
        if self.img_pref.watermark_pil:
            self.img_pref.overlay_image = self.img_pref.watermark_pil.copy()
        self.update_canvas_background()

    def save_images(self):
        if self.img_pref.background_image and self.img_pref.overlay_image:
            folder_path = filedialog.askdirectory(title="Select Save Folder")

            if folder_path:
                for index in range(self.images_list.size()):
                    image_path = self.images_list.get(index)
                    background_path = f"{self.img_pref.selected_image_path}/{image_path}"

                    image_pil = Image.open(background_path).convert("RGB")

                    modified_image = self.process_image_edits(image_pil, self.img_pref.watermark_pil)

                    image_edit = modified_image.copy()
                    image_name = image_path.split("/")[-1]

                    if image_pil.mode != "RGB":
                        image_edit = image_edit.convert("RGB")

                    file_path = os.path.join(folder_path, f"edited_{image_name}")
                    image_edit.save(file_path)
                messagebox.showerror("Success", f"Your image has been saved successfully")

        else:
            messagebox.showerror("No Folder", f"NO folder selected")

    def save_present_image(self):
        if self.img_pref.overlay_image and self.img_pref.background_image:
            file_path = filedialog.asksaveasfilename(confirmoverwrite=True,
                                                     defaultextension="png",
                                                     filetypes=[("jpeg", ".jpg"),
                                                                ("png", ".png"),
                                                                ("bitmap", "bmp"),
                                                                ("gif", ".gif")])
            if file_path:
                image_path = self.img_pref.image_path

                # Check the file extension and if it is jpg or jpeg, convert to RGB
                image_pil = Image.open(image_path)

                modified_image = self.process_image_edits(image_pil, self.img_pref.watermark_pil)

                image_edit = modified_image.copy()

                if image_pil.mode != "RGB":
                    image_edit = image_edit.convert("RGB")

                image_edit.save(file_path)
                messagebox.showerror("Success", f"Your image has been saved successfully")
