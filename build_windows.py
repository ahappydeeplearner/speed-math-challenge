#!/usr/bin/env python3
"""
Windows 构建脚本
使用 PyInstaller 构建 Windows 可执行文件
"""
import os
import shutil
import subprocess
import sys
import zipfile


def clean_build_dirs():
    """清理之前的构建目录"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已删除: {dir_name}")


def build_exe():
    """使用 PyInstaller 构建可执行文件"""
    pyinstaller_cmd = [
        'pyinstaller',
        '--name=速算闯关',
        '--windowed',
        '--noconsole',
        '--onedir',
        '--add-data=assets;assets',
        '--add-data=config;config',
        '--add-data=storage;storage',
        '--hidden-import=pygame',
        '--hidden-import=numpy',
        'main.py'
    ]
    
    print("正在使用 PyInstaller 构建应用...")
    result = subprocess.run(pyinstaller_cmd)
    if result.returncode != 0:
        print("构建失败！")
        sys.exit(1)
    print("应用构建成功！")


def create_zip():
    """创建 ZIP 压缩包"""
    app_dir = 'dist/速算闯关'
    zip_name = '速算闯关-Windows-Installer.zip'
    zip_path = f'dist/{zip_name}'
    
    if not os.path.exists(app_dir):
        print(f"错误: 找不到应用目录 {app_dir}")
        sys.exit(1)
    
    print("正在创建 ZIP 压缩包...")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(app_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, 'dist')
                zipf.write(file_path, arcname)
    
    print(f"ZIP 压缩包创建成功: {zip_path}")


def main():
    print("=" * 50)
    print("速算闯关 - Windows 构建脚本")
    print("=" * 50)
    
    clean_build_dirs()
    build_exe()
    create_zip()
    
    print("\n" + "=" * 50)
    print("构建完成！")
    print("=" * 50)


if __name__ == '__main__':
    main()
