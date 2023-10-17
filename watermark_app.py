from tkinter import *
from tkinter import ttk, messagebox
from image_preference import ImagePreference
import tkinter.font as tkFont


class WatermarkApp:
    def __init__(self):
        self.window = Tk()
        self.window.title("Watermark Images")
        self.window.configure(bg="#222222")
        self.window.config(padx=30, pady=50)

        self.style = ttk.Style(self.window)
        self.style.theme_use('alt')
        self.style.configure('.', focuscolor=self.style.lookup('.', 'background'))

        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)
        self.img_pref = ImagePreference()

        self.title = ttk.Label(self.window, background="#333333", foreground="white",
                               text="Add Custom Watermark to Photos in 5 Mins",
                               font=("Arial", 30, "bold"))
        self.title.grid(row=0, column=1, columnspan=5, pady=20)

        self.buttons_frame = Frame(self.window, padx=50, pady=10, background="#222222")
        self.buttons_frame.grid(row=1, column=1, columnspan=3)

        # Images Menu
        self.button_browse = ttk.Button(self.buttons_frame, text="Select Images", command=self.list_images)
        self.button_browse.grid(row=1, column=1, padx=3)

        # Images Menu
        self.button_browse = ttk.Button(self.buttons_frame, text="Select Watermark", command=self.upload_watermark)
        self.button_browse.grid(row=1, column=2, padx=3)

        self.button_image_settings = ttk.Button(self.buttons_frame, text="Open Image Properties",
                                                command=self.image_settings_toggle)
        self.button_image_settings.grid(row=1, column=3, padx=3)
        self.open_image_settings = False
        if not self.open_image_settings:
            self.button_image_settings.grid_remove()

        self.listbox_frame = Frame(self.window, padx=50, pady=50, background="#222222")
        self.listbox_frame.grid(row=2, column=1, columnspan=3)

        self.image_scrollbar = ttk.Scrollbar(self.listbox_frame, orient=VERTICAL)

        self.images_list = Listbox(self.listbox_frame, height=5, width=60, yscrollcommand=self.image_scrollbar.set)
        self.image_scrollbar.config(command=self.images_list.yview)
        self.image_scrollbar.pack(side=RIGHT, fill=Y)
        self.images_list.pack(fill="both", expand=True)

        self.doc_frame = Frame(self.window, padx=50, pady=50, background="#222222")
        self.doc_frame.grid(row=2, column=1, columnspan=3)
        self.doc_frame.grid_remove()

        self.doc_scrollbar = ttk.Scrollbar(self.doc_frame, orient=VERTICAL)

        self.doc_list = Listbox(self.doc_frame, height=15, width=60)
        self.doc_scrollbar.config(command=self.doc_list.yview)
        self.doc_scrollbar.pack(side=RIGHT, fill=Y)
        self.doc_list.pack(fill="both")

        self.save_frame = Frame(self.window, padx=50, pady=10, background="#222222")
        self.save_frame.grid(row=3, column=1, columnspan=3)

        self.save_all_images = ttk.Button(self.save_frame, text="Save All Images", command=self.save_images)
        self.save_all_images.grid(row=3, column=1, padx=10)
        self.save_all_images.grid_remove()

        self.save_current_image = ttk.Button(self.save_frame, text="Save Current Image",
                                             command=self.save_present_image)
        self.save_current_image.grid(row=3, column=2, padx=10)
        self.save_current_image.grid_remove()

        std_font = tkFont.nametofont("TkDefaultFont")
        std_font.config(size=10)
        self.copyright_label = Label(text="Made with ❤️ by Precious", font=std_font)
        self.copyright_label.grid(row=4, column=1, sticky=S + W)

        # Create the frame for the image background_canvas
        self.delete_frame = Frame(self.window, padx=5, pady=5, background="#222222")
        self.delete_frame.grid(row=1, column=5)
        self.delete_frame.grid_remove()

        self.delete_image = ttk.Button(self.delete_frame, text="Delete Selected Image",
                                       command=self.delete_current_image)
        self.delete_image.grid(row=1, column=7, pady=10, padx=3)
        self.delete_image.grid_remove()
        self.delete_all_images = ttk.Button(self.delete_frame, text="Delete All Images", command=self.clear_all_images)
        self.delete_all_images.grid(row=1, column=8, pady=10, padx=3)
        self.delete_all_images.grid_remove()

        self.image_frame = Frame(self.window, padx=5, pady=5, background="#d3d3d3")
        self.image_frame.grid(row=2, column=5, rowspan=5)
        self.image_frame.grid_remove()

        self.background_canvas = Canvas(self.image_frame, highlightthickness=0)
        self.background_canvas.grid(row=2, column=5, rowspan=5, columnspan=3)

        self.current_size = DoubleVar()

    def open_image_properties(self):
        self.open_image_settings = True
        self.button_image_settings.grid()

        self.settings_window = Toplevel(self.window)
        self.settings_window.protocol("WM_DELETE_WINDOW", self.on_closing_image_preference)
        self.settings_window.title("Image Properties")

        # Settings
        settings_frame = Frame(self.settings_window, padx=30, pady=30, background="#2c2c2c")
        settings_frame.grid(row=0, column=0)

        title_frame = Frame(settings_frame, padx=10, pady=10, background="#2c2c2c")
        title_frame.grid(row=1, column=0)

        # Settings Title
        settings_title = ttk.Label(title_frame, text="Properties", background="#2c2c2c",
                                   foreground="white",
                                   font=("Arial", 18, "bold"))
        settings_title.grid(row=1, column=0, padx=30, pady=10)

        # Color chooser
        color_frame = Frame(settings_frame, padx=10, pady=10, background="#212122")
        color_frame.grid(row=2, column=0)

        color_title = ttk.Label(color_frame, text="Color", background="#212122",
                                foreground="white",
                                font=("Arial", 14, "bold"))
        color_title.grid(row=2, column=0)

        row_count = 3
        col_count = 0
        max_count = 17
        displayed_color = 0

        for color_hex, color_name in self.img_pref.color_names.items():
            color_button = ttk.Button(color_frame, text=color_hex, width=13,
                                      command=lambda name=color_name: self.create_color_grid(name))
            color_button.grid(row=row_count, column=col_count)
            col_count += 1
            displayed_color += 1
            if col_count == 5:
                col_count = 0
                row_count += 1
                if displayed_color >= max_count:
                    break

        self.color_display = Label(color_frame, text="", background=f"{self.img_pref.default_color}", width=10, height=1)
        self.color_display.grid(row=2, column=1, pady=10)
        color_label = Label(color_frame, text="HEX: ", background="#212122", foreground="white")
        color_label.grid(row=2, column=2)
        self.color_entry = Entry(color_frame, width=10)
        self.color_entry.insert(END, f"{self.img_pref.default_color}")
        self.color_entry.bind("<Return>", self.apply_custom_color)
        self.color_entry.grid(row=2, column=3)
        color_remove = ttk.Button(color_frame, width=10, text="Do Not Color", command=self.remove_color)
        color_remove.grid(row=2, column=4)

        # PADDING FRAME
        padding_frame = Frame(settings_frame, padx=5, pady=5, background="#2c2c2c")
        padding_frame.grid(row=3, column=0)

        color_pad = ttk.Label(padding_frame, text="", background="#2c2c2c",
                              foreground="white",
                              font=("Arial", 2, "bold"))
        color_pad.grid(row=3, column=0)

        # Image Size
        size_frame = Frame(settings_frame, padx=10, pady=10, background="#212122")
        size_frame.grid(row=4, column=0)

        self.current_size = DoubleVar()
        current_size = self.img_pref.display_size
        self.current_size.set(current_size)
        formatted_size = '{:.1f}'.format(self.current_size.get())
        size_label = ttk.Label(size_frame, text="Size", background="#212122", foreground="white",
                               font=("Arial", 14, "bold"))
        size_label.grid(row=4, column=0, padx=10)
        self.current_size_label = ttk.Label(size_frame, text=f"{formatted_size}", background="#212122", foreground="white")
        self.current_size_label.grid(row=4, column=2, padx=10)

        resize_image = ttk.Scale(size_frame, from_=1.0, to=5.0, orient="horizontal",
                                 command=self.on_size_change, variable=self.current_size)
        resize_image.grid(row=4, column=1)

        self.opacity_size = IntVar()
        opacity = self.img_pref.opacity
        self.opacity_size.set(opacity)
        opacity_label = ttk.Label(size_frame, text="Opacity", background="#212122", foreground="white",
                                  font=("Arial", 14, "bold"))
        opacity_label.grid(row=4, column=3, padx=10)
        self.current_opacity_label = ttk.Label(size_frame, text=f"{opacity}%", background="#212122", foreground="white")
        self.current_opacity_label.grid(row=4, column=5, padx=10)
        reduce_opacity = ttk.Scale(size_frame, from_=1, to=100,
                                   orient="horizontal", command=lambda value: self.on_opacity_change(value),
                                   variable=self.opacity_size)
        reduce_opacity.grid(row=4, column=4)

        # PADDING FRAME
        padding_frame1 = Frame(settings_frame, padx=5, pady=5, background="#2c2c2c")
        padding_frame1.grid(row=5, column=0)

        filter_pad = ttk.Label(padding_frame1, text="", background="#2c2c2c",
                               foreground="white",
                               font=("Arial", 2, "bold"))
        filter_pad.grid(row=5, column=0)

        filter_frame = Frame(settings_frame, padx=10, pady=10, background="#212122")
        filter_frame.grid(row=6, column=0)

        filter_title = ttk.Label(filter_frame, text="Effect", background="#212122",
                                 foreground="white",
                                 font=("Arial", 14, "bold"))
        filter_title.grid(row=6, column=0, pady=5)

        remove_effect = ttk.Button(filter_frame, width=10, text="Remove Effect", command=self.on_remove_effect)
        remove_effect.grid(row=6, column=1, pady=5, columnspan=3, sticky=E)

        filter_row = 7
        filter_col = 0

        for filter_name, filter_type in self.img_pref.filters.items():
            filter_button = ttk.Button(filter_frame, text=filter_name,
                                       command=lambda et=filter_name: self.apply_effect(et))
            filter_button.grid(row=filter_row, column=filter_col)
            filter_col += 1
            if filter_col == 4:
                filter_col = 0
                filter_row += 1
        for enhance_name, enhance_type in self.img_pref.enhance_buttons.items():
            enhance_button = ttk.Button(filter_frame, text=enhance_name,
                                        command=lambda et=enhance_name: self.apply_effect(et))
            enhance_button.grid(row=filter_row, column=filter_col)
            filter_col += 1
            if filter_col == 4:
                filter_col = 0
                filter_row += 1

        # PADDING FRAME
        padding_frame2 = Frame(settings_frame, padx=5, pady=5, background="#2c2c2c")
        padding_frame2.grid(row=8, column=0)
        rotation_pad = ttk.Label(padding_frame2, text="", background="#2c2c2c",
                                 foreground="white",
                                 font=("Arial", 2, "bold"))
        rotation_pad.grid(row=8, column=0)

        rotation_frame = Frame(settings_frame, padx=10, pady=10, background="#212122")
        rotation_frame.grid(row=9, column=0)

        rotation_title = ttk.Label(rotation_frame, text="Rotation", background="#212122", foreground="white",
                                   font=("Arial", 14, "bold"))
        rotation_title.grid(row=9, column=0, pady=5)

        self.rotate_var = IntVar()
        angle = self.img_pref.overlay_rotation
        self.rotate_var.set(angle)

        rotate1 = Radiobutton(rotation_frame, text="180", variable=self.rotate_var, value=180,
                              command=self.on_rotation_change)
        rotate2 = Radiobutton(rotation_frame, text="-90", variable=self.rotate_var, value=-90,
                              command=self.on_rotation_change)
        rotate3 = Radiobutton(rotation_frame, text="0", variable=self.rotate_var, value=0,
                              command=self.on_rotation_change)
        rotate4 = Radiobutton(rotation_frame, text="90", variable=self.rotate_var, value=90,
                              command=self.on_rotation_change)

        rotate1.grid(row=10, column=0, padx=5, sticky="w")
        rotate2.grid(row=10, column=1, padx=5, sticky="w")
        rotate3.grid(row=10, column=2, padx=5, sticky="w")
        rotate4.grid(row=10, column=3, padx=5, sticky="w")

        rotation_title = ttk.Label(rotation_frame, text="Position", background="#212122", foreground="white",
                                   font=("Arial", 14, "bold"))
        rotation_title.grid(row=12, column=0, pady=5)

        self.current_position = StringVar()
        position = self.img_pref.watermark_edits["position"]
        self.current_position.set(position)

        top_left = Radiobutton(rotation_frame, text="Top Left", variable=self.current_position, value="Top Left",
                              command=self.change_watermark_position)
        top_right = Radiobutton(rotation_frame, text="Top Right", variable=self.current_position, value="Top Right",
                              command=self.change_watermark_position)
        center = Radiobutton(rotation_frame, text="Center", variable=self.current_position, value="Center",
                              command=self.change_watermark_position)
        bottom_right = Radiobutton(rotation_frame, text="Bottom Right", variable=self.current_position, value="Bottom Right",
                              command=self.change_watermark_position)
        bottom_left = Radiobutton(rotation_frame, text="Bottom Left", variable=self.current_position, value="Bottom Left",
                              command=self.change_watermark_position)

        top_left.grid(row=12, column=0, padx=5, sticky="w")
        top_right.grid(row=12, column=1, padx=5, sticky="w")
        center.grid(row=12, column=2, padx=5, sticky="w")
        bottom_right.grid(row=12, column=3, padx=5, sticky="w")
        bottom_left.grid(row=12, column=4, padx=5, sticky="w")

        # PADDING FRAME
        padding_frame3 = Frame(settings_frame, padx=5, pady=5, background="#2c2c2c")
        padding_frame3.grid(row=13, column=0)
        close_pad = ttk.Label(padding_frame3, text="", background="#2c2c2c",
                              foreground="white",
                              font=("Arial", 2, "bold"))
        close_pad.grid(row=13, column=0)

        close_frame = Frame(settings_frame, padx=10, pady=10, background="#212122")
        close_frame.grid(row=14, column=0)

        close_image = ttk.Button(close_frame, text="Close", command=self.close_image_properties)
        close_image.grid(row=14, column=2, padx=30)

    def close_image_properties(self):
        self.open_image_settings = False
        self.button_image_settings.grid()
        self.settings_window.destroy()

    def on_closing(self):
        if messagebox.askokcancel("Exit", "Do you really want to quit?"):
            self.window.destroy()

    def on_closing_image_preference(self):
        self.open_image_settings = False
        self.button_image_settings.grid()
        self.settings_window.destroy()
