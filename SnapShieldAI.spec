from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

project = Path(SPECPATH)
datas = [
    (str(project / "frontend" / "dist"), "frontend/dist"),
    (str(project / "ml" / "artifacts"), "ml/artifacts"),
    (str(project / "data" / "samples"), "data/samples"),
] + collect_data_files("rapidocr_onnxruntime")
hiddenimports = collect_submodules("rapidocr_onnxruntime") + [
    "sklearn.feature_extraction.text",
    "sklearn.linear_model._logistic",
    "sklearn.preprocessing._label",
]

a = Analysis([str(project / "desktop_launcher.py")], pathex=[str(project)], binaries=[], datas=datas, hiddenimports=hiddenimports, hookspath=[], hooksconfig={}, runtime_hooks=[], excludes=["dask", "IPython", "matplotlib", "pandas", "pyarrow", "pytest", "tensorflow", "torch"], noarchive=False)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name="SnapShieldAI", debug=False, bootloader_ignore_signals=False, strip=False, upx=True, console=True, disable_windowed_traceback=False)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=True, upx_exclude=[], name="SnapShieldAI")
