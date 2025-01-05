import os
import subprocess

def print_labels():
    labels_dir = "labels"
    if not os.path.exists(labels_dir):
        print("No labels found. Generate labels first.")
        return

    # Define your printer settings
    backend = "pyusb"
    model = "QL-500"
    printer_identifier = "usb://0x04f9:0x2015"  # Use the correct USB ID for your printer
    label_type = "62"  # 62mm continuous label

    for label in sorted(os.listdir(labels_dir)):
        label_path = os.path.join(labels_dir, label)
        print(f"Printing label: {label_path}")

        try:
            # Construct the CLI command
            command = [
                "brother_ql",
                "-b", backend,
                "-m", model,
                "-p", printer_identifier,
                "print",
                "-l", label_type,
                label_path
            ]

            # Execute the command
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error printing label: {e}")
            break

        input("Press Enter to print the next label...")

if __name__ == "__main__":
    print_labels()
