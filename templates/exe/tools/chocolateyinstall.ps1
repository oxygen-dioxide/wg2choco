$ErrorActionPreference = 'Stop'; # stop on all errors
$toolsDir   = "$(Split-Path -parent $MyInvocation.MyCommand.Definition)"
 
$url        = '{installerUrl}'
$packageArgs = @{{
  packageName   = '{id}'
  url           = $url
  fileType      = 'EXE' #only one of these: exe, msi, msu
  softwareName  = '{id}*'
  checksum      = '{installerSha256}'
  checksumType  = 'sha256'
  silentArgs    = "{silentArgs}"
  validExitCodes= @(0, 3010, 1641)
}}

Install-ChocolateyPackage @packageArgs