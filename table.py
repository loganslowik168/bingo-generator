from PIL import Image, ImageDraw, ImageFont
import textwrap

# Define the function to create the table image
def create_table_image(table, cell_size=100, font_size=20, output_file="bingoCard.png"):
    # Calculate the size of the image
    rows = len(table)
    cols = max(len(row) for row in table)
    img_width = cols * cell_size
    img_height = rows * cell_size

    # Create a blank image with white background
    img = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(img)

    # Load a font
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Draw the table
    for row_idx, row in enumerate(table):
        for col_idx, cell_text in enumerate(row):
            # Calculate cell position
            x1 = col_idx * cell_size
            y1 = row_idx * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            # Draw the rectangle for the cell
            draw.rectangle([x1, y1, x2, y2], outline="black")

            # Wrap the text to fit inside the cell
            max_characters_per_line = cell_size // (font_size // 2)  # Estimate based on font size
            wrapped_text = textwrap.fill(cell_text, width=max_characters_per_line)

            # Calculate the text bounding box to center the text
            bbox = draw.textbbox((0, 0), wrapped_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = x1 + (cell_size - text_width) // 2
            text_y = y1 + (cell_size - text_height) // 2

            # Draw the text
            draw.text((text_x, text_y), wrapped_text, fill="black", font=font)

    # Save the image
    img.save(output_file)
    print(f"Bingo card saved as {output_file}")

