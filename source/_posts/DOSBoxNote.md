---
title: DOSBoxNote
date: 2022-12-26 23:00:39
cover: DOSBoxNote.png
tags:
    - DOSBox
    - Construction
description: DOSBox software tutorial
---

## Construction

[DOSBox software download link](https://youareaaron0.lanzoub.com/iVj4t00h3g7e)

[application in DOSBox download link](https://lifesea.org/)

1. open DOSBox.exe
2. Running specific program
   - In CMD:  
   `mount c g:CAI`: `c` means to create virtual C directory and `g:CAI` means where is virtual directory's location
   - In Config:
   loc:`C/User/Administrator/AppData/Local/DOSBox/dosbox-0.74.conf`  
     1. over config file bottom type this:  
        `mount c g:CAI`  
        `g:`  
        `CAI`  
     2. run the exe file
3. modified the **window size**
   1. open config file  
      top of context find `windowresolution=original`  
   2. change to `windowresolution=1920x1080`
   3. then change next line `output=surface` to `output=openg1`