from font_gen import FontGenerator

x = FontGenerator("font.ttf")
x.export_font("new_font.ttf")

print(x.encode_string("Hello World"))