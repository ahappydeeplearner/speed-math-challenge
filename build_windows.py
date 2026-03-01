#!/usr/bin/env python3
"""
Windows build script
Build Windows executable using PyInstaller
"""
import os
import shutil
import subprocess
import sys
import zipfile


def clean_build_dirs():
    """Clean previous build directories"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Deleted: {dir_name}")


def build_exe():
    """Build executable using PyInstaller"""
    pyinstaller_cmd = [
        'pyinstaller',
        '--name=SpeedMathChallenge',
        '--windowed',
        '--onedir',
        '--clean',
        '--noconfirm',
        '--add-data=assets;assets',
        '--add-data=config;config',
        '--add-data=storage;storage',
        '--collect-all=pygame',
        '--collect-all=numpy',
        '--hidden-import=pygame',
        '--hidden-import=numpy',
        '--hidden-import=numpy.core',
        '--hidden-import=numpy.core.multiarray',
        'main.py'
    ]
    
    print("Building app with PyInstaller...")
    result = subprocess.run(pyinstaller_cmd)
    if result.returncode != 0:
        print("Build failed!")
        sys.exit(1)
    print("App built successfully!")


def create_zip():
    """Create ZIP archive"""
    app_dir = 'dist/SpeedMathChallenge'
    zip_name = 'SpeedMathChallenge-Windows-Installer.zip'
    zip_path = f'dist/{zip_name}'
    
    if not os.path.exists(app_dir):
        print(f"Error: App directory not found {app_dir}")
        sys.exit(1)
    
    print("Creating ZIP archive...")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(app_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, 'dist')
                zipf.write(file_path, arcname)
    
    print(f"ZIP archive created: {zip_path}")


def main():
    print("=" * 50)
    print("Speed Math Challenge - Windows Build Script")
    print("=" * 50)
    
    clean_build_dirs()
    build_exe()
    create_zip()
    
    print("\n" + "=" * 50)
    print("Build complete!")
    print("=" * 50)


if __name__ == '__main__':
    main()
