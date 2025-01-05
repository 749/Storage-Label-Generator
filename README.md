# Storage Label Generator

## Overview

This project generates and prints storage box labels for a Brother QL-500 label printer. It handles odd numbers of bins per row, minimizes label paper waste, and supports special configurations for rows with fewer bins.

## Features

- **Label Generation**:
  - Generates labels based on the storage rack letter, number of columns, and number of rows.
  - Handles special rows with fewer bins dynamically.
  - Optimizes label usage by pairing leftover labels with the next available one.
  - Clears the existing `labels` folder before generating new labels.

- **Label Printing**:
  - Uses the `brother_ql` CLI to print labels on a Brother QL-500 printer.
  - Supports USB connection with customizable printer settings.
  - Sequential printing with manual cutting prompts.

## Prerequisites

1. **Install Dependencies**:
   - Ensure `pipenv` is installed:
     ```bash
     pip install pipenv
     ```
   - Install project dependencies:
     ```bash
     pipenv install
     ```

2. **Install Brother QL CLI**:
   - Install the `brother_ql` package globally or within the `pipenv` environment:
     ```bash
     pip install brother_ql
     ```

3. **Verify Printer Connection**:
   - Use the following command to discover connected printers:
     ```bash
     brother_ql discover
     ```
   - Confirm the USB ID matches your printer (e.g., `usb://0x04f9:0x2015`).

4. **Ensure Font Availability**:
   - Download and place the font `NotoSansMono-VariableFont_wdth,wght.ttf` in a known location.
   - Update the `LABEL_FONT` variable in `generate_labels.py` with the correct path.

## Usage

### Generate Labels

1. Run the script to generate labels:
   ```bash
   pipenv run python generate_labels.py <STORAGE_LETTER> <WIDTH> <HEIGHT> [--special_rows ROW:BINS ...]
   ```

2. **Arguments**:
   - `STORAGE_LETTER`: The identifier for the storage rack (e.g., `A`).
   - `WIDTH`: The maximum number of bins per row.
   - `HEIGHT`: The total number of rows in the storage.

3. **Optional**:
   - `--special_rows ROW:BINS ...`: Define rows with fewer bins. Example: `--special_rows 10:2 11:1` (row 10 has 2 bins, row 11 has 1 bin).

4. **Example**:
   ```bash
   pipenv run python generate_labels.py A 5 11 --special_rows 10:2 11:1
   ```

   - Clears the `labels` folder.
   - Generates labels for a rack with 5 bins per row, 11 rows, where rows 10 and 11 have 2 and 1 bins, respectively.
   - Optimizes label paper usage by combining leftover labels with the next available one.

### Print Labels

1. Print generated labels:
   ```bash
   pipenv run python print_labels.py
   ```

2. The script will:
   - Print labels sequentially using the `brother_ql` CLI.
   - Prompt for manual cutting after each label is printed.

3. **CLI Options**:
   - Backend: `pyusb`
   - Model: `QL-500`
   - Printer: `usb://0x04f9:0x2015` (update with your printer's USB ID).

## File Structure

```
storage_label_generator/
├── Pipfile
├── Pipfile.lock
├── README.md
├── generate_labels.py
├── print_labels.py
├── labels/  # Contains generated label images
└── fonts/   # (Optional) Place custom fonts here
```

## Customization

- **Font**:
  - Update the `LABEL_FONT` variable in `generate_labels.py` to use a different font file.

- **Printer Settings**:
  - Update `backend`, `model`, and `printer_identifier` in `print_labels.py` to match your printer.

- **Label Size**:
  - Modify `LABEL_WIDTH` and `LABEL_HEIGHT` in `generate_labels.py` to adjust label dimensions.

## Notes

- Ensure the `labels` folder is writable.
- Test the font rendering to ensure compatibility with the label printer.
- The optimization for special rows and leftover labels ensures minimal paper waste.

## Known Issues

- If the specified font is unavailable, the script will fall back to the default system font and issue a warning.

## Contributing

Feel free to submit pull requests or open issues to improve the project.

## License

This project is licensed under the MIT License.
