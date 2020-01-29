# -*- mode: python -*-

block_cipher = None


a = Analysis(['launcher.py'],
             pathex=['C:\\Users\\lbbas\\Desktop\\test\\webCourseQT',
             'C:\\Users\\lbbas\\Desktop\\test\\webCourseQT\\api',
             'C:\\Users\\lbbas\\Desktop\\test\\webCourseQT\\resource',
             'C:\\Users\\lbbas\\Desktop\\test\\webCourseQT\\ui'
             ],
             binaries=[],
             datas=[('resource','resource')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
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
          name='launcher',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='launcher')
