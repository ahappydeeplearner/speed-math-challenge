name: Cross-platform Build

on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:

jobs:
  build-macos:
    name: Build macOS Version
    runs-on: macos-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Setup Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pygame pyinstaller pillow
    
    - name: Build macOS app
      run: |
        python3 build_installer.py
    
    - name: Upload macOS installer
      uses: actions/upload-artifact@v4
      with:
        name: SpeedMathChallenge-macOS
        path: dist/SpeedMathChallenge-Installer.dmg
        retention-days: 30

  build-windows:
    name: Build Windows Version
    runs-on: windows-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Setup Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pygame pyinstaller pillow
    
    - name: Build Windows app
      run: |
        python build_windows.py
    
    - name: Upload Windows installer
      uses: actions/upload-artifact@v4
      with:
        name: SpeedMathChallenge-Windows
        path: dist/SpeedMathChallenge-Windows-Installer.zip
        retention-days: 30

  create-release:
    name: Create Release
    needs: [build-macos, build-windows]
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/')
    
    steps:
    - name: Download all artifacts
      uses: actions/download-artifact@v4
    
    - name: Create Release
      uses: softprops/action-gh-release@v2
      with:
        files: |
          SpeedMathChallenge-macOS/SpeedMathChallenge-Installer.dmg
          SpeedMathChallenge-Windows/SpeedMathChallenge-Windows-Installer.zip
        body: |
          ## Speed Math Challenge - Cross-platform Version
          
          ### Download Instructions
          - **macOS Users**: Download `SpeedMathChallenge-Installer.dmg`
          - **Windows Users**: Download `SpeedMathChallenge-Windows-Installer.zip`
          
          ### Installation Instructions
          
          **macOS**:
          1. Open DMG file
          2. Drag app to Applications folder
          3. First run requires authorization in System Settings
          
          **Windows**:
          1. Extract ZIP file
          2. Run SpeedMathChallenge.exe directly (portable mode)
          
          ### System Requirements
          - macOS 10.13 or higher
          - Windows 7/8/10/11
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
