# -*- mode: python -*-

block_cipher = None


a = Analysis(['C:\\Users\\nhemingway\\PycharmProjects\\TimeSheet\\src\\main\\python\\main.py'],
             pathex=['C:\\Users\\nhemingway\\PycharmProjects\\TimeSheet\\target\\PyInstaller'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=['c:\\users\\nhemingway\\pycharmprojects\\timesheet\\venv\\lib\\site-packages\\fbs\\freeze\\hooks'],
             runtime_hooks=['C:\\Users\\nhemingway\\PycharmProjects\\TimeSheet\\target\\PyInstaller\\fbs_pyinstaller_hook.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Test',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False , icon='C:\\Users\\nhemingway\\PycharmProjects\\TimeSheet\\src\\main\\icons\\Icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='Test')
