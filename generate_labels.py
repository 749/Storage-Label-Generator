import os
import shutil
from PIL import Image, ImageDraw, ImageFont

LABEL_WIDTH = 696  # Total width for the image (includes two labels)
LABEL_HEIGHT = 75  # Height of each label
SINGLE_LABEL_WIDTH = LABEL_WIDTH // 2  # Width of a single label
LABEL_FONT = "font/NotoSansMono-VariableFont_wdth,wght.ttf"  # Path to the font file

def clear_labels_folder():
    """Clears the labels folder before generating new labels."""
    labels_dir = "labels"
    if os.path.exists(labels_dir):
        shutil.rmtree(labels_dir)
    os.makedirs(labels_dir)

def generate_labels(storage_letter, width, height, special_rows=None):
    """
    Generates labels for the storage bins.

    :param storage_letter: The rack identifier (e.g., "A").
    :param width: The maximum number of bins per row.
    :param height: The total number of rows.
    :param special_rows: A dictionary specifying the number of bins for specific rows
                         (e.g., {10: 2, 11: 1}).
    """
    labels_dir = "labels"
    if not os.path.exists(labels_dir):
        os.makedirs(labels_dir)
    
    try:
        font = ImageFont.truetype(LABEL_FONT, size=40)  # Use the specified font
    except IOError:
        font = ImageFont.load_default()
        print(f"Warning: Could not load {LABEL_FONT}. Using default font.")

    leftover_label = None  # To store a single leftover label

    for row in range(1, height + 1):
        row_width = special_rows.get(row, width) if special_rows else width  # Handle special rows
        for col in range(1, row_width + 1):
            current_label = f"{storage_letter}{row:02}{col:02}"

            if leftover_label:
                # Combine leftover label with the current label
                img = Image.new("RGB", (LABEL_WIDTH, LABEL_HEIGHT), color="white")
                draw = ImageDraw.Draw(img)

                # Draw the leftover label
                bbox1 = draw.textbbox((0, 0), leftover_label, font=font)
                text_width1 = bbox1[2] - bbox1[0]
                text_height1 = bbox1[3] - bbox1[1]
                text_x1 = (SINGLE_LABEL_WIDTH - text_width1) // 2
                text_y1 = (LABEL_HEIGHT - text_height1) // 2
                draw.text((text_x1, text_y1), leftover_label, fill="black", font=font)

                # Draw the current label
                bbox2 = draw.textbbox((0, 0), current_label, font=font)
                text_width2 = bbox2[2] - bbox2[0]
                text_height2 = bbox2[3] - bbox2[1]
                text_x2 = SINGLE_LABEL_WIDTH + (SINGLE_LABEL_WIDTH - text_width2) // 2
                text_y2 = (LABEL_HEIGHT - text_height2) // 2
                draw.text((text_x2, text_y2), current_label, fill="black", font=font)

                # Draw vertical center line as cutting guide
                draw.line(
                    [(SINGLE_LABEL_WIDTH, 0), (SINGLE_LABEL_WIDTH, LABEL_HEIGHT)],
                    fill="black",
                    width=2,  # Line thickness
                )

                # Save the combined label image
                label_filename = f"labels/{leftover_label}_{current_label}.png"
                img.save(label_filename)
                print(f"Generated label: {label_filename}")

                leftover_label = None  # Reset leftover label
            else:
                # Save the current label as a leftover if no pair is available
                leftover_label = current_label

    # Handle the last leftover label, if any
    if leftover_label:
        img = Image.new("RGB", (LABEL_WIDTH, LABEL_HEIGHT), color="white")
        draw = ImageDraw.Draw(img)

        # Draw the leftover label on the first half
        bbox1 = draw.textbbox((0, 0), leftover_label, font=font)
        text_width1 = bbox1[2] - bbox1[0]
        text_height1 = bbox1[3] - bbox1[1]
        text_x1 = (SINGLE_LABEL_WIDTH - text_width1) // 2
        text_y1 = (LABEL_HEIGHT - text_height1) // 2
        draw.text((text_x1, text_y1), leftover_label, fill="black", font=font)

        # Draw vertical center line as cutting guide
        draw.line(
            [(SINGLE_LABEL_WIDTH, 0), (SINGLE_LABEL_WIDTH, LABEL_HEIGHT)],
            fill="black",
            width=2,  # Line thickness
        )

        # Save the leftover label
        label_filename = f"labels/{leftover_label}_blank.png"
        img.save(label_filename)
        print(f"Generated label: {label_filename}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate storage box labels")
    parser.add_argument("storage_letter", help="The storage rack letter (A-Z)")
    parser.add_argument("width", type=int, help="Number of columns")
    parser.add_argument("height", type=int, help="Number of rows")
    parser.add_argument(
        "--special_rows",
        nargs="+",
        help="Special rows with different numbers of bins (e.g., 10:2 11:1)",
        default=None
    )
    args = parser.parse_args()

    # Parse special rows
    special_rows = {}
    if args.special_rows:
        for entry in args.special_rows:
            row, bins = entry.split(":")
            special_rows[int(row)] = int(bins)

    clear_labels_folder()
    generate_labels(args.storage_letter, args.width, args.height, special_rows)
