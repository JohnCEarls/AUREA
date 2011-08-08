##Set-ExecutionPolicy Unrestricted (run on command line in admin mode)
Get-ChildItem Env:
$Aversion = "1.6.2"
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

$from = "C:\Documents and Settings\john\AUREA\dist\AUREA-"+$Aversion+".win32.zip"
$to = "C:\Documents and Settings\john\AUREA\dist\AUREA-"+$Aversion+".win32-py2." + $v + ".zip"
cp $from $to
rm $from
}
$env:Path = $origPath
$env:Path
$from = "C:\Documents and Settings\john\AUREA\dist\*" 
$to = "C:\Documents and Settings\john\My Documents\Dropbox\Price\builds"
cp $from $to