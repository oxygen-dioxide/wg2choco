$ErrorActionPreference = 'Stop'; # stop on all errors
$toolsDir   = "$(Split-Path -parent $MyInvocation.MyCommand.Definition)"
 
$url        = 'https://download.wondershare.com/cbs_down/filmora_64bit_12.0.21_full846.exe'
$packageArgs = @{
  packageName   = 'filmora'
  url           = $url
  fileType      = 'EXE' #only one of these: exe, msi, msu
  softwareName  = 'filmora*'
  checksum      = '396BE3C4C84EF39A79FEA630A1EEA02BE14C0A3DE8576C52D0B2217A53C60692'
  checksumType  = 'sha256'
  silentArgs    = "/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-"
  validExitCodes= @(0, 3010, 1641)
}

Install-ChocolateyPackage @packageArgs