import os
import sys
import yaml
import pathlib
import packaging.version
import github_action_utils

#获取winget路径
winget_id=sys.argv[1]#winget包名
winget_id=winget_id.split(".")#转为字符串列表形式
rootpath=pathlib.Path(sys.argv[0]).resolve().parent
winget_software_path=rootpath.joinpath("winget-pkgs","manifests",winget_id[0][0].lower(),*winget_id)

#最新版本号
version=str(max([packaging.version.parse(versionpath.name) for versionpath in winget_software_path.iterdir()]))
try:
    github_action_utils.set_env("version",version)
except:
    pass
winget_package_path=winget_software_path.joinpath(version)
print("Winget package is located in",winget_package_path)

#解析winget包
for filepath in winget_package_path.iterdir():
    filename=str(filepath)
    if("installer" in filename):
        installerinfo=yaml.load(filepath.open(encoding="utf8"),Loader=yaml.BaseLoader)
    elif("locale" in filename):
        if("en-US" in filename):
            localeinfo=yaml.load(filepath.open(encoding="utf8"),Loader=yaml.BaseLoader)
    else:
        basicinfo=yaml.load(filepath.open(encoding="utf8"),Loader=yaml.BaseLoader)
#在choco包中需要用到的信息
chocoid=sys.argv[2]#choco包名
chocoinfo={
    "id":chocoid,
    "version":version,
    "title":localeinfo["PackageName"],
    "projectUrl":localeinfo["PackageUrl"],
    "tags":" ".join(localeinfo.get("Tags",[])),
    "summary":localeinfo["ShortDescription"],
    "description":localeinfo["ShortDescription"],
    "installerUrl":installerinfo["Installers"][0]["InstallerUrl"],
    "installerSha256":installerinfo["Installers"][0]["InstallerSha256"],
}
if("Author" in localeinfo):
    chocoinfo["authors"]=localeinfo["Author"]
else:
    chocoinfo["authors"]=winget_id[0]

if("Installers" in installerinfo):
    installer = installerinfo["Installers"][0] | installerinfo
else:
    installer = installerinfo
installertype=installer["InstallerType"]
#import ipdb
#ipdb.set_trace()
if("InstallerSwitches" in installer):
    if("SilentWithProgress" in installer["InstallerSwitches"]):
        chocoinfo["silentArgs"]=installer["InstallerSwitches"]["SilentWithProgress"]
    else:
        chocoinfo["silentArgs"]=installer["InstallerSwitches"]["Silent"]
templatepath=rootpath.joinpath("templates",installertype)
choco_package_path=pathlib.Path.cwd().joinpath(chocoid)
print("Choco package is output to:",choco_package_path)

#递归，把template_current_path的全部文件填入信息后，存入choco_current_path
def folderwalk(template_current_path,choco_current_path):
    choco_current_path.mkdir(exist_ok=True)
    for template_child in template_current_path.iterdir():
        choco_child=choco_current_path.joinpath(template_child.name.format(**chocoinfo))
        if(template_child.is_file()):#文件：
            choco_child.write_text(template_child.read_text(encoding="utf8").format(**chocoinfo),encoding="utf8")
        else:#文件夹
            folderwalk(template_child,choco_child)
folderwalk(templatepath,choco_package_path)

