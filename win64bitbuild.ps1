##Set-ExecutionPolicy Unrestricted (run on command line in admin mode)
Get-ChildItem Env:
$pyVs = @(6,7)
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
python setup.py bdist_egg
python setup.py bdist_wininst
python setup.py bdist
cp C:\Users\earls3\AUREA\dist\AUREA-1.6.1.win-amd64.zip C:\Users\earls3\AUREA\dist\AUREA-1.6.1.win-amd64-py2.$v.zip 
rm C:\Users\earls3\AUREA\dist\AUREA-1.6.1.win-amd64.zip
}
$env:Path = $origPath
$env:Path

cp C:\Users\earls3\AUREA\dist\* C:\Users\earls3\Dropbox\Price\builds