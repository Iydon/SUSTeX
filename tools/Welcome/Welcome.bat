@echo off
SETLOCAL enabledelayedexpansion
chcp 65001 >nul
title Welcome to TeX World!

goto:start
如何制作批处理文件:
==================
1. 在桌面右键, 选择[新建] - [文本文档].
2. 将本批处理脚本复制粘贴到新建文档中, 再点击[文件] - [另存为].
3. 选择好保存路径, 在下面将[保存类型]改为"所有文件(*.*)", 然后在文件名中输入"SUSTeX.bat", 点击[保存].
4. 点击"SUSTeX.bat"运行批处理程序, 运行完毕删除即可.
:start

rem 变量赋值.
set option=-c
set version=-c
set tmp=-c



rem 介绍
:introductionYesOrNo
echo 请仔细阅读本批处理文件的内容.
set /p option="(Y/N)的意思为: 如果'是', 则输入'Y'并按回车, 否则输入'N'并按回车, 你是否明白(Y/N)"
if /i "!option!"=="Y" (
    echo .
) else (
    if /i "!option!"=="N" (
        echo 如果不明白, 可以在[https://github.com/Iydon/SUSTeX]提出[Issues].
        start https://github.com/Iydon/SUSTeX
        echo .
    ) else (
        goto:introductionYesOrNo
    )
)
set option=-c
set /p tmp="进行下一步(Enter)"

rem 镜像下载
:downloadISO
echo 一个[TeX发行版]是[TeX]排版引擎, 支持排版的软件以及一些辅助工具的集合.
echo 现今的两个主流发行版为[TeX Live]和[MikTeX].
echo 本批处理暂时只说明[TeX Live]安装方法, [MikTeX]请自行搜索.
call:todo
set /p option="你是否下载[TeX]发行版(例如[TeX Live])(Y/N)"
if /i "!option!"=="Y" (
    call:pass
) else (
    if /i "!option!"=="N" (
        echo [https://mirrors.ustc.edu.cn/CTAN/systems/texlive/Images/]
        echo [https://mirrors.tuna.tsinghua.edu.cn/CTAN/systems/texlive/Images/]
        start https://mirrors.ustc.edu.cn/CTAN/systems/texlive/Images/
        start https://mirrors.tuna.tsinghua.edu.cn/CTAN/systems/texlive/Images/
        echo 可以到如上网站下载[texlive2018.iso].
    ) else (
        goto:downloadISO
    )
)
set option=-c
set /p tmp="进行下一步(Enter)"

rem 镜像安装
:installISO
set /p option="你是否安装[TeX]发行版(Y/N)"
if /i "!option!"=="Y" (
    call:pass
) else (
    if /i "!option!"=="N" (
        rem 版本信息
        ver && set /p version="请根据如上信息输入系统版本(7/10)"
        if "!version!"=="7" (
            echo [Windows 7]未自带镜像挂载软件, 请于搜索引擎上搜索[win7镜像挂载].
        ) else (
            if "!version!"=="10" (
                echo [Windows 10]可以自动挂载镜像, 鼠标左键双击镜像文件, 便可自动挂载镜像.
            ) else (
                echo 版本不清楚, 该批处理文件可能无法提供帮助.
            )
        )
    ) else (
        goto:installISO
    )
    echo .
    echo 挂载完镜像请打开[DVD驱动器]运行[install-tl-windows.bat]脚本. 期间不可以待机, 安装时间视电脑而定, 请耐心等待, 大概需要1小时左右.
    echo 发行版安装最后一步需要等待很长时间, 不要随意终止.
)
set option=-c
set /p tmp="进行下一步(Enter)"

rem 编辑器安装
:installEditor
echo 安装编辑器请于发行版安装完后进行, 这样编辑器可以自动配置编译命令.
set /p option="你是否下载[TeX]编辑器(例如[TeX Studio])(Y/N)"
if /i "!option!"=="Y" (
    call:pass
) else (
    if /i "!option!"=="N" (
        set option=-c
        set /p option="你是否希望打开[TeX Live]自带编辑器(TeXWorks)(Y/N)"
        if /i "!option!"=="Y" (
            texworks >nul 2>nul
            if %ERRORLEVEL% LEQ 16 (
                echo 如果觉得不满意, 可以下载[TeX Studio]编辑器.
                echo [https://github.com/texstudio-org/texstudio/releases].
                start https://github.com/texstudio-org/texstudio/releases
            ) else (
                echo [TeX]发行版有可能未正常安装, 请先安装[TeX]发行版.
            )
        ) else (
            echo 如果未安装编辑器, 推荐[TeX Studio]编辑器.
            echo [https://github.com/texstudio-org/texstudio/releases].
            start https://github.com/texstudio-org/texstudio/releases
        )
    ) else (
        goto:installEditor
    )
)
set option=-c
set /p tmp="进行下一步(Enter)"

rem 判断 TeX 命令是否可行, 从而推断是否安装发行版.
tex -v >nul 2>nul
if %ERRORLEVEL% LEQ 16 (
    echo TeX Live 安装没有问题.
    rem 示例文件
    :demoFile
    set /p option="是否生成示例文件(Y/N)"
    if /i "!option!"=="Y" (
        call:writeDemoFile
    ) else (
        if /i "!option!"=="N" ( echo . ) else ( goto:demoFile )
    )
    set option=-c
    set /p tmp="进行下一步(Enter)"
    rem 帮助文档
    :texdocMan
    set /p option="是否查看帮助文档(Y/N)"
    if /i "!option!"=="Y" (
        texdoc lshort-zh >nul 2>nul
        if %ERRORLEVEL% LEQ 16 (
            echo 在命令行输入[texdoc]加你想搜索的宏包名称, 即可查看其帮助文档.
            echo 例如本次命令即[texdoc lshort-zh].
            echo 如果[texdoc]无法查找到相应文档, 可以去[https://ctan.org/]继续查找.
            start https://ctan.org/
        ) else (
            call:todo
        )
    ) else (
        if /i "!option!"=="N" ( echo . ) else ( goto:texdocMan )
    )
    set option=-c
    set /p tmp="进行下一步(Enter)"
) else (
    echo 如果输入时存在异常, 例如未输入即按回车, 则有可能到达此选项, 如果是这样则忽略此条, 重新打开批处理脚本, 确保输入精准.
    call:todo
    echo 如果到达这里请提出[Issues], 再加入新的逻辑.
    start https://github.com/Iydon/SUSTeX
)

rem echo ERROREVEL: %ERRORLEVEL%

pause
goto:end



rem Functions
:writeDemoFile
    echo 写入文件, 编译文件中...
    echo \documentclass{standalone}  > demo.tex
    echo \begin{document}           >> demo.tex
    echo Happy \LaTeX ing.          >> demo.TeX
    echo \end{document}             >> demo.TeX
    PdfLaTeX demo.tex >nul
    del demo.log demo.aux
    echo 示例文件 demo.tex 编译成功.
goto:eof

:pass
rem 类似[Python]的[pass].
echo 好的.
goto:eof

:todo
rem TODO.
goto:eof



:end
