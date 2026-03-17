# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('delete_duplicates', 'delete_duplicates'),
        ('artist_extractor', 'artist_extractor'),
        ('reorder_tracks', 'reorder_tracks'),
        ('separate_artists', 'separate_artists'),
        ('separate_genres', 'separate_genres'),
        ('smart_shuffle', 'smart_shuffle'),
        ('playlist_time', 'playlist_time'),
        ('top_tracks_generator', 'top_tracks_generator'),
        ('mood_mixer', 'mood_mixer'),
        ('metadata_export', 'metadata_export'),
        ('utils', 'utils')
    ],
    hiddenimports=['spotipy', 'customtkinter', 'difflib'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='SpotifyToolkit_GUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
