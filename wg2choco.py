import sys
import yaml
import pathlib
import packaging.version

#获取winget路径
winget_id=sys.argv[1]#winget包名
#winget_id="listen1.listen1"
winget_id=winget_id.split(".")#转为字符串列表形式
rootpath=pathlib.Path(sys.argv[0]).resolve().parent
winget_software_path=rootpath.joinpath("winget-pkgs","manifests",winget_id[0][0].lower(),*winget_id)
#最新版本号
version=str(max([packaging.version.parse(versionpath.name) for versionpath in winget_software_path.iterdir()]))
winget_package_path=winget_software_path.joinpath(version)
print("Winget软件包路径：",winget_package_path)
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
chocoid=winget_id[1]
chocoinfo={
    "id":chocoid,
    "version":version,
    "title":localeinfo["PackageName"],
    "authors":localeinfo["Author"],
    "projectUrl":localeinfo["PackageUrl"],
    "tags":" ".join(localeinfo["Tags"]),
    "summary":localeinfo["ShortDescription"],
    "description":localeinfo["ShortDescription"],
    "installerUrl":installerinfo["Installers"][0]["InstallerUrl"],
    "installerSha256":installerinfo["Installers"][0]["InstallerSha256"],
}
installertype=installerinfo["InstallerType"]
templatepath=rootpath.joinpath("templates",installertype)
choco_package_path=pathlib.Path.cwd().joinpath(chocoid)
print("输出choco软件包路径：",choco_package_path)
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
#import ipdb
#ipdb.set_trace()
