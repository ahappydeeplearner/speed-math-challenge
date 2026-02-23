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
    """清理之前的构建目录"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已删除: {dir_name}")


def build_app():
    """使用 PyInstaller 构建应用"""
    pyinstaller_cmd = [
        'pyinstaller',
        '--name=速算闯关',
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
    
    print("正在使用 PyInstaller 构建应用...")
    result = subprocess.run(pyinstaller_cmd)
    if result.returncode != 0:
        print("构建失败！")
        sys.exit(1)
    print("应用构建成功！")


def create_dmg():
    """创建 DMG 安装包"""
    app_path = 'dist/速算闯关.app'
    dmg_name = '速算闯关-Installer.dmg'
    dmg_path = f'dist/{dmg_name}'
    
    if not os.path.exists(app_path):
        print(f"错误: 找不到应用 {app_path}")
        sys.exit(1)
    
    print("正在创建 DMG 安装包...")
    
    temp_dir = 'temp_dmg'
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    shutil.copytree(app_path, os.path.join(temp_dir, '速算闯关.app'))
    
    applications_link = os.path.join(temp_dir, 'Applications')
    if not os.path.exists(applications_link):
        os.symlink('/Applications', applications_link)
    
    if os.path.exists(dmg_path):
        os.remove(dmg_path)
    
    hdiutil_cmd = [
        'hdiutil', 'create',
        '-volname', '速算闯关',
        '-srcfolder', temp_dir,
        '-ov',
        '-format', 'UDZO',
        dmg_path
    ]
    
    result = subprocess.run(hdiutil_cmd)
    if result.returncode != 0:
        print("DMG 创建失败！")
        sys.exit(1)
    
    shutil.rmtree(temp_dir)
    print(f"DMG 安装包创建成功: {dmg_path}")


def main():
    print("=" * 50)
    print("速算闯关 - macOS 构建脚本")
    print("=" * 50)
    
    clean_build_dirs()
    build_app()
    create_dmg()
    
    print("\n" + "=" * 50)
    print("构建完成！")
    print("=" * 50)


if __name__ == '__main__':
    main()
