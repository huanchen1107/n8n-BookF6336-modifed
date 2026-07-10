import os
import sys
import win32com.client

def convert_to_pdf(input_path):
    input_path = os.path.abspath(input_path)
    output_path = os.path.splitext(input_path)[0] + ".pdf"

    excel = None
    try:
        excel = win32com.client.DispatchEx("Excel.Application")
        excel.Visible = False
        excel.DisplayAlerts = False

        wb = excel.Workbooks.Open(input_path)

        for sheet in wb.Sheets:
            sheet.PageSetup.Zoom = False
            sheet.PageSetup.FitToPagesWide = 1
            sheet.PageSetup.FitToPagesTall = False

        wb.ExportAsFixedFormat(0, output_path)
        wb.Close(False)
        print(output_path)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    finally:
        if excel:
            excel.Quit()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        convert_to_pdf(sys.argv[1])