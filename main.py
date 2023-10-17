from watermark import WatermarkLogo

app = WatermarkLogo()

app.window.protocol("WM_DELETE_WINDOW", app.on_closing)
app.window.mainloop()
