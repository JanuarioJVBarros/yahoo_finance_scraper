from openpyxl import Workbook
import os

def write_to_excel(file_name, header_list, data, file_path='analysis_results'):
    os.makedirs(file_path, exist_ok=True)

    # Create a new workbook and a sheet
    wb = Workbook()
    sheet = wb.active

    # Write the headers to the first row
    sheet.append(header_list)

    # Write the data to subsequent rows
    for row in data:
        sheet.append(row)

    # Ensure the directory exists
    os.makedirs(file_path, exist_ok=True)

    # Combine file path and file name
    full_file_path = os.path.join(file_path, f"{file_name}.xlsx")

    # Save the workbook to the specified file
    wb.save(full_file_path)

    print(f"File '{file_name}' saved at: {full_file_path}")

