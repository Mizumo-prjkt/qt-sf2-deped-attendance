import os
import tarfile
import zipfile
import subprocess
import datetime

def create_archive(files, archive_format="zip", output_filename=None):
    """
    Bundles a list of files into an archive.
    Supported formats: zip, tar, tar.xz, 7z
    """
    if not files:
        print("No files to archive.")
        return None
        
    valid_files = [f for f in files if os.path.exists(f)]
    if not valid_files:
        print("None of the specified files exist for archiving.")
        return None
        
    if not output_filename:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.dirname(os.path.abspath(valid_files[0]))
        output_filename = os.path.join(output_dir, f"Attendance_Bundle_{timestamp}")
        
    # Append correct extension
    if archive_format == "zip" and not output_filename.endswith(".zip"):
        output_filename += ".zip"
    elif archive_format == "tar" and not output_filename.endswith(".tar"):
        output_filename += ".tar"
    elif archive_format == "tar.xz" and not output_filename.endswith(".tar.xz"):
        output_filename += ".tar.xz"
    elif archive_format == "7z" and not output_filename.endswith(".7z"):
        output_filename += ".7z"
        
    print(f"Creating {archive_format} archive: {output_filename} ...")
    
    try:
        if archive_format == "zip":
            with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as arc:
                for file_path in valid_files:
                    arc.write(file_path, arcname=os.path.basename(file_path))
                    
        elif archive_format == "tar":
            with tarfile.open(output_filename, "w") as arc:
                for file_path in valid_files:
                    arc.add(file_path, arcname=os.path.basename(file_path))
                    
        elif archive_format == "tar.xz":
            with tarfile.open(output_filename, "w:xz") as arc:
                for file_path in valid_files:
                    arc.add(file_path, arcname=os.path.basename(file_path))
                    
        elif archive_format == "7z":
            # Attempt to use py7zr if installed, else fallback to 7z command
            try:
                import py7zr
                with py7zr.SevenZipFile(output_filename, 'w') as arc:
                    for file_path in valid_files:
                        arc.write(file_path, arcname=os.path.basename(file_path))
            except ImportError:
                print("py7zr not installed, attempting to use 7z system command...")
                cmd = ["7z", "a", output_filename] + valid_files
                subprocess.run(cmd, check=True, capture_output=True)
        else:
            print(f"Unsupported archive format: {archive_format}")
            return None
            
        print(f"Successfully created archive at {output_filename}")
        return output_filename
        
    except Exception as e:
        print(f"Error creating archive: {e}")
        return None
