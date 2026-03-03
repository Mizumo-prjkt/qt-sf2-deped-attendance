import subprocess
import os

def convert_xlsx_to_pdf(xlsx_paths):
    """
    Converts a list of .xlsx file paths to .pdf using LibreOffice headless.
    Returns a list of generated .pdf file paths.
    """
    pdf_paths = []
    for xlsx_path in xlsx_paths:
        if not os.path.exists(xlsx_path):
            print(f"File not found: {xlsx_path}")
            continue
            
        output_dir = os.path.dirname(os.path.abspath(xlsx_path))
        print(f"Converting {xlsx_path} to PDF...")
        
        try:
            # Run libreoffice headless conversion
            # Syntax: libreoffice --headless --convert-to pdf <file> --outdir <dir>
            cmd = [
                "libreoffice",
                "--headless",
                "--convert-to", "pdf",
                xlsx_path,
                "--outdir", output_dir
            ]
            
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            
            # Libreoffice saves the file as .pdf in the output_dir with the same base name
            base_name = os.path.splitext(os.path.basename(xlsx_path))[0]
            expected_pdf_path = os.path.join(output_dir, f"{base_name}.pdf")
            
            if os.path.exists(expected_pdf_path):
                pdf_paths.append(expected_pdf_path)
                print(f"Successfully converted to {expected_pdf_path}")
            else:
                print(f"Error: Conversion succeeded but expected PDF not found at {expected_pdf_path}")
                print(f"LibreOffice Output: {result.stdout}")
                
        except subprocess.CalledProcessError as e:
            print(f"Error converting {xlsx_path} to PDF.")
            print(f"LibreOffice Output: {e.stdout}")
            print(f"LibreOffice Error: {e.stderr}")
        except FileNotFoundError:
            print("Error: 'libreoffice' command not found. Please ensure LibreOffice is installed and in your PATH.")
            break # No point trying others if the command doesn't exist
            
    return pdf_paths
