#!/usr/bin/env python
# -*- coding: utf-8 -*-
##########################################################
#   A clever person solves a problem. A wise person avoids it
#   Please call Me programming devil.
#
#   提供C/C++代码的开源项目，生成一个可以供Microsoft Visual Studio 2010 正常打开的
#   工程文件
#   注意：此方法生成的工程文件，仅供使用vs2010打开看代码，不要妄想可以直接编译的。
#           因为使用vs系列看c++代码，真是爽。
######################################################## #
import os
import uuid
import sys
reload(sys)
sys.setdefaultencoding('utf-8') #允许打印unicode字符


#被认为invalid的文件，将不被包含在工程目录里
def is_invalid_file(f=""):
    f=f.lower()
    suffixs=[".gitignore",".gitmodules",".travis.yml",".dat",".patch",".png","log","zip",".rc",".ico",".bmp","doc",".pyc"]
    for s in suffixs:
        if f.endswith(s):
            return True
    return False



#遍历rootDir，将得到的dir放在dirList里，将file放在fileList
def tsearch1(rootDir,dirList=[],fileList=[]):
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        if os.path.basename(path).startswith('.'):
            continue

        if is_invalid_file(path):
            continue

        if os.path.isdir(path):

            dirList.append(path.decode("gbk"))
            tsearch1(path,dirList,fileList)
        else:
            fileList.append(path.decode("gbk"))




def makesln(rootDir):
    parentdir = os.path.split(rootDir)[0]
    slndir=os.path.join(parentdir,"sln")
    if not  os.path.exists(slndir):
        os.mkdir(slndir)

    dirList =[]
    fileList = []
    tsearch1(rootDir,dirList,fileList)

    namespace=os.path.split(rootDir)[1]
    dirs=";\n".join(dirList)
    # print dirs
    files="\n".join([ '<ClInclude Include="{0}"/>'.format( f ) for f in fileList])
    param={"namespace":namespace,"dirs":dirs,"files":files}
    txt='''
    <?xml version="1.0" encoding="utf-8"?>
<Project DefaultTargets="Build" ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">

  <ItemGroup Label="ProjectConfigurations">
    <ProjectConfiguration Include="Debug|Win32">
      <Configuration>Debug</Configuration>
      <Platform>Win32</Platform>
    </ProjectConfiguration>
    <ProjectConfiguration Include="Release|Win32">
      <Configuration>Release</Configuration>
      <Platform>Win32</Platform>
    </ProjectConfiguration>
  </ItemGroup>

    <ItemGroup>
          %(files)s
    </ItemGroup>


  <PropertyGroup Label="Globals">
    <ProjectGuid>{ECB32C21-BB38-4352-9FB0-1E25F23DE8C6}</ProjectGuid>
    <Keyword>Win32Proj</Keyword>
    <RootNamespace>%(namespace)s</RootNamespace>
  </PropertyGroup>
  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.Default.props" />
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Debug|Win32'" Label="Configuration">
    <ConfigurationType>Application</ConfigurationType>
    <UseDebugLibraries>true</UseDebugLibraries>
    <CharacterSet>MultiByte</CharacterSet>
  </PropertyGroup>
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Release|Win32'" Label="Configuration">
    <ConfigurationType>Application</ConfigurationType>
    <UseDebugLibraries>false</UseDebugLibraries>
    <WholeProgramOptimization>true</WholeProgramOptimization>
    <CharacterSet>Unicode</CharacterSet>
  </PropertyGroup>
  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.props" />
  <ImportGroup Label="ExtensionSettings">
  </ImportGroup>

  <ImportGroup Label="PropertySheets" Condition="'$(Configuration)|$(Platform)'=='Debug|Win32'">
    <Import Project="$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
  </ImportGroup>
  <ImportGroup Label="PropertySheets" Condition="'$(Configuration)|$(Platform)'=='Release|Win32'">
    <Import Project="$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
  </ImportGroup>
  <PropertyGroup Label="UserMacros" />
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Debug|Win32'">
    <LinkIncremental>true</LinkIncremental>
  </PropertyGroup>
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Release|Win32'">
    <LinkIncremental>false</LinkIncremental>
  </PropertyGroup>

  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Debug|Win32'">
    <ClCompile>
      <PrecompiledHeader>
      </PrecompiledHeader>
      <WarningLevel>Level3</WarningLevel>
      <Optimization>Disabled</Optimization>
      <PreprocessorDefinitions>WIN32;_DEBUG;_CONSOLE;%%(PreprocessorDefinitions)</PreprocessorDefinitions>
      <AdditionalIncludeDirectories>
                    %(dirs)s
      </AdditionalIncludeDirectories>
    </ClCompile>

    <Link>
      <SubSystem>Console</SubSystem>
      <GenerateDebugInformation>true</GenerateDebugInformation>
    </Link>
  </ItemDefinitionGroup>

  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Release|Win32'">
    <ClCompile>
      <WarningLevel>Level3</WarningLevel>
      <PrecompiledHeader>
      </PrecompiledHeader>
      <Optimization>MaxSpeed</Optimization>
      <FunctionLevelLinking>true</FunctionLevelLinking>
      <IntrinsicFunctions>true</IntrinsicFunctions>
      <PreprocessorDefinitions>WIN32;NDEBUG;_CONSOLE;%%(PreprocessorDefinitions)</PreprocessorDefinitions>
    </ClCompile>
    <Link>
      <SubSystem>Console</SubSystem>
      <GenerateDebugInformation>true</GenerateDebugInformation>
      <EnableCOMDATFolding>true</EnableCOMDATFolding>
      <OptimizeReferences>true</OptimizeReferences>
    </Link>
  </ItemDefinitionGroup>
  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.targets" />
  <ImportGroup Label="ExtensionTargets">
  </ImportGroup>

</Project>'''%param

    outfile = os.path.join(slndir, "{0}.vcxproj".format(param['namespace']))
    with open(outfile, 'w'  ) as f:
        f.write( txt.strip())
    print(outfile)


    txt='''
    <?xml version="1.0" encoding="utf-8"?>
<Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <ItemGroup>
    '''
    p=len(rootDir)
    for dt in dirList:
        dt=dt[p+1:]
        txt += '''<Filter Include="%s"><UniqueIdentifier>{%s}</UniqueIdentifier></Filter>\n'''%(dt, uuid.uuid1())
    txt +="</ItemGroup>\n"


    def get_parent_dir(fn=""):
        fn1=fn[p+1:]
        fn2=os.path.split(fn1)[0]
        return fn2

    for fn in fileList:
        pn=get_parent_dir(fn)
        if not pn:
            continue
        txt +='''<ItemGroup>
        <ClInclude Include="%s">
          <Filter>%s</Filter>
        </ClInclude>
      </ItemGroup>'''%(fn,pn)


    txt +="\n</Project>"

    outfile = os.path.join( slndir, "{0}.vcxproj.filters".format(param['namespace']  ) )
    with open(outfile, 'w') as f:
        f.write(txt.strip())
    print(outfile)





def main():
    rootDir = r'D:\work\zhangtao\codeyun\ztlmq\shimy_src'
    makesln(rootDir)
    print "DONE"

main()