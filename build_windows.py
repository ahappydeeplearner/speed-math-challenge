#!/usr/bin/env python3
"""
macOS 构建脚本
使用 PyInstaller 构建 macOS 应用并创建 DMG 安装包
"""
import os
import shutil
import subprocess
import sys


def clean_build_dirs():
    """Clean previous build directories"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Deleted: {dir_name}")


def build_app():
    """Build app using PyInstaller"""
    pyinstaller_cmd = [
        'pyinstaller',
        '--name=速算闯关之外星入侵',
        '--windowed',
        '--noconsole',
        '--onedir',
        '--add-data=assets:assets',
        '--add-data=config:config',
        '--add-data=storage:storage',
        '--hidden-import=pygame',
        '--hidden-import=numpy',
        'main.py'
    ]
    
    print("Building app with PyInstaller...")
    result = subprocess.run(pyinstaller_cmd)
    if result.returncode != 0:
        print("Build failed!")
        sys.exit(1)
    print("App built successfully!")


def create_dmg():
    """Create DMG installer"""
    app_path = 'dist/速算闯关之外星入侵.app'
    dmg_name = 'SpeedMathChallenge-Installer.dmg'
    dmg_path = f'dist/{dmg_name}'
    
    if not os.path.exists(app_path):
        print("Error: App not found")
        sys.exit(1)
    
    print("Creating DMG installer...")
    
    temp_dir = 'temp_dmg'
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    shutil.copytree(app_path, os.path.join(temp_dir, '速算闯关之外星入侵.app'))
    
    applications_link = os.path.join(temp_dir, 'Applications')
    if not os.path.exists(applications_link):
        os.symlink('/Applications', applications_link)
    
    if os.path.exists(dmg_path):
        os.remove(dmg_path)
    
    hdiutil_cmd = [
        'hdiutil', 'create',
        '-volname', 'SpeedMathChallenge',
        '-srcfolder', temp_dir,
        '-ov',
        '-format', 'UDZO',
        dmg_path
    ]
    
    result = subprocess.run(hdiutil_cmd)
    if result.returncode != 0:
        print("DMG creation failed!")
        sys.exit(1)
    
    shutil.rmtree(temp_dir)
    print("DMG installer created successfully")


def main():
    print("=" * 50)
    print("Speed Math Challenge - macOS Build Script")
    print("=" * 50)
    
    clean_build_dirs()
    build_app()
    create_dmg()
    
    print("\n" + "=" * 50)
    print("Build complete!")
    print("=" * 50)


if __name__ == '__main__':
    main()
