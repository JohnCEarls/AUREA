##Set-ExecutionPolicy Unrestricted (run on command line in admin mode)
Get-ChildItem Env:
$pyVs = @(7)
$origPath = $env:Path
foreach($v in $pyVs){

$env:PYTHON_LIB = "C:\Python2"+$v+"\libs\Python2" + $v +".lib"
$env:PYTHON_INCLUDE = "C:\Python2"+$v+"\include"
$env:Path = $origPath + ";C:\Python2" + $v
Get-ChildItem Env:
$env:Path
$oldpylib = $env:PYTHON_LIB

$env:PYTHON_LIB = $null
$test = $env:PYTHON_LIB
"
Building ...
"
python setup.py build
}
$env:PYTHONPATH = "C:\Users\earls3\AUREA\build\lib.win-amd64-2.7"
