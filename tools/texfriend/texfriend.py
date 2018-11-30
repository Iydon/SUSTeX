"""
     -*$$$$*~  -=                            .,,,.     ,---------------------                 .~~~----~~,    -~----~~~
   .!#;,..,~!!,*$                          .;=*****~  ;@@@#$====#@@#=====$#@@-                ,!*$@@@@#=-    :$@@@@$*!
   !@~       ;#@#                         ,#$-    -$*-@@@*,     ;@@$.    .~#@:                   .*@@@~       .$@#~.
  -@*         !@#                        ,$$,       !#@@!       :@@=       -#;                    ,#@@!        *$,
  =@~         .$#                        !@:        .=@#,       :@@=        =*                     ~@@@~      -@~
 .#@~          ;$                       .#@.         ~@$.       :@@=        ;=                      !@@#.    .=*
 ,#@:          ~$                       ,@@           #*        :@@=        -$                      .$@@!    ;=
 .#@=          ,$!!!!!!!!!;.    -*!!!!!!=@@,          !*        :@@=        ,#                       ~@@@~  ,$-
  =@@;         .;!!=@@@#*!;.    -*=#@@#**@@!          ~*        :@@=      ~**@****************;       *@@#..$;
  :@@@*~.           #@@!           ~#$, .#@@:         .-        :@@=      -::!@@@=:::::::;!$@@#       .$@@*!=.
   =@@@@@$!-.       $@@:            $:   !@@@*-.                :@@=          =@@:          :@@.       -@@@#.
   ,=@@@@@@@#*-     $@@:            $~   ,$@@@@#=;~,            :@@=          =@@:           ;@,        !@@#.
    .;#@@@@@@@#;    $@@:            $~    -$@@@@@@@#*,          :@@=          =@@:           .#~        ,#@@*
      .~*$@@@@@@~   $@@:            $~     .*@@@@@@@@#-         :@@=          =@@:            *:        ~#@@@:
          ,~!#@@$.  $@@:            $~       ,~!=#@@@@#-        :@@=          =@@:            :!       .=:;@@$,
             -#@@:  $@@:            $~           .-!@@@*        :@@=          =@@:      :~    ,*       *! .=@@*
  ,           -@@$  $@@:            $~              ~#@#,       :@@=          =@@:      *:     ,      :#,  -@@@~
 ,=            *@#  $@@:            $~  .,           ;@@~       :@@=          =@@:      $:           -$~    ;@@#-
 ,$            :@@  $@@:            $~  -!           .@@;       :@@=          =@@:     :@:           *!      =@@=.
 ,#-           :@$  $@@:            $~  -*            #@;       :@@=          =@@=!!!*$@@:          :=.      -#@@:
 ,#*           ;@!  $@@:            $~  -$.           $@~       :@@=          =@@*::::!#@:         -#~        ;@@#,
 ,#@~          $@.  $@@:            $~  -@~           @#,       :@@=          =@@:     ,@:        .$=          #@@=
 ,#@$~        ;@;   $@@:            $~  -@#,         ~@*        ;@@$.         =@@:      =:       ,*@=          :@@@;
 ,#$:$*-    .!@!    $@@:            $~  -@@$-       .$@-   ~;;;*#@@@=!;;:.    =@@:      !:    :!$#@@@=~      -!#@@@@=;;.
 ,$- .!$$=**$$:     =@@;           .$-  -@;:$;-.  .-=#~    ;************!.    =@@:      ~-    *$$*****;      ~*********,
  -    .-~::-.      ;@@!           ,$.  -=. -;=====$!-                        =@@:             ;~
                    ,@@$           ~=    .     .--,.                          =@@:             *,
                     *@#,          *:                                         =@@:            ,$.
                     -#@!         :=.                                         =@@:            *=.
                      ~@@~       :#-                                          =@@:           :@*
                       ~=@!-..,~*=-                                         .,#@@;.      .,-!@@!
                        .:=##$$$;.                                        :$$#@@@#$$$$$$$$#@@@@:
"""


# Function
counter = 0
def do_job():
    global counter
    title.config(text='do '+ str(counter))
    counter+=1

# Setting -> TopLevel
top_level_flag = False
def top_level():
    global top_level_flag
    top_level_flag = not top_level_flag
    window.wm_attributes('-topmost',top_level_flag)

# Setting -> Language
def change_language():
    global lang_choice, LANG
    idx  = lang_choice.get()
    code = cfg.TEXFRIEND_LANGUAGE_LIST[idx]
    language("w")

def language(action:str):
    with open(file=cfg.TEXFRIEND_LANGUAGE_FILE, mode=action, encoding=cfg.TEXFRIEND_ENCODING) as f:
        if action is "r":
            return f.read()
        elif action is "w":
            global lang_choice
            f.write(str(lang_choice.get()))


# Import
import tkinter as tk
from cfg import cfg, lang


# CONSTANE
CURRENT_LANGUAGE = int(language("r"))
LANG = lang.__getattribute__(cfg.TEXFRIEND_LANGUAGE_LIST[CURRENT_LANGUAGE])

window = tk.Tk()
window.title(cfg.TEXFRIEND_WINDOWN_TITLE)
window.iconbitmap(cfg.TEXFRIEND_ICON_PATH)
window.geometry(cfg.TEXFRIEND_GEOMETRY)


title = tk.Label(window, text='', bg='yellow')
title.pack()


# Menu bar
menubar  = tk.Menu(window)

# File
menu_file = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label=LANG['File'], menu=menu_file)
menu_file.add_command(label=LANG['Open'], command=do_job)
menu_file.add_command(label=LANG['Save'], command=do_job)
menu_file.add_command(label=LANG['New'], command=do_job)
menu_file.add_separator()
menu_file.add_command(label=LANG['Exit'], command=window.quit)

# Setting
menu_setting = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label=LANG['Setting'], menu=menu_setting)
menu_setting.add_checkbutton(label=LANG['TopLevel'], command=top_level)

# Setting -> lang
lang_choice = tk.IntVar()
lang_choice.set(CURRENT_LANGUAGE)
menu_setting_lang = tk.Menu(menubar)
menu_setting.add_cascade(label=LANG['Language'], menu=menu_setting_lang, underline=0)
menu_setting_lang.add_radiobutton(label="中文", variable=lang_choice, value=0, command=change_language)
menu_setting_lang.add_radiobutton(label="English", variable=lang_choice, value=1, command=change_language)
menu_setting_lang.add_radiobutton(label="Le Français", variable=lang_choice, value=2, command=change_language)

# Pack
window.config(menu=menubar)

window.mainloop()
