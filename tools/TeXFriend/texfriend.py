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


#!/bin/python
"""
Hello World, but with more meat.
"""

import wx
from cfg.lang import zh as LANG
from cfg import cfg


class TeXFriend(wx.Frame):
    """
    A Frame that says Hello World
    """

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(TeXFriend, self).__init__(*args, **kw)

        # create a panel in the frame
        pnl = wx.Panel(self)

        # and put some text with a larger bold font on it
        st = wx.StaticText(pnl, label="Hello World!", pos=(25,25))
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)

        # Create an icon
        self.icon = wx.Icon(name=cfg.TEXFRIEND_ICON_PATH)
        self.SetIcon(self.icon)

        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText(cfg.TEXFRIEND_ORGANIZATION)


    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        NewItem = fileMenu.Append(-1, "&%s"%LANG["New"], "")
        OpenItem = fileMenu.Append(-1, "&%s"%LANG["Open"], "")
        SaveItem = fileMenu.Append(-1, "&%s\tCtrl-S"%LANG["Save"], "")
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(-1, LANG["Exit"])

        # Setting Menu
        settingMenu = wx.Menu()
        topLevelItem = settingMenu.Append(-1, LANG["TopLevel"])
        welcomePageItem = settingMenu.Append(-1, LANG["WelcomePage"])
        LanguageItem = settingMenu.Append(-1, LANG["Language"])

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(-1, LANG["About"])

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&%s"%LANG["File"])
        menuBar.Append(settingMenu, "&%s"%LANG["Setting"])
        menuBar.Append(helpMenu, "&%s"%LANG["Help"])

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnNew, NewItem)
        self.Bind(wx.EVT_MENU, self.OnOpen, OpenItem)
        self.Bind(wx.EVT_MENU, self.OnSave, SaveItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)


    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    def OnNew(self, event):
        self.PushStatusText(LANG["New"])
        wx.MessageBox("TODO")
        self.SetStatusText(cfg.TEXFRIEND_ORGANIZATION)

    def OnOpen(self, event):
        self.PushStatusText(LANG["Open"])
        wx.MessageBox("TODO")
        self.SetStatusText(cfg.TEXFRIEND_ORGANIZATION)

    def OnSave(self, event):
        self.PushStatusText(LANG["Save"])
        wx.MessageBox("TODO")
        self.SetStatusText(cfg.TEXFRIEND_ORGANIZATION)

    def OnAbout(self, event):
        """Display an About Dialog"""
        self.PushStatusText(LANG["About"])
        wx.MessageBox(LANG["AboutInformation"],
                      LANG["About"],
                      wx.OK|wx.ICON_INFORMATION)


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = TeXFriend(None, title=cfg.TEXFRIEND_WINDOWN_TITLE)
    frm.Show()
    app.MainLoop()