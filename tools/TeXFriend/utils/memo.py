def start(window):
	import tkinter as tk
	from tkinter import ttk

	__author__ = 'Administrator'


	def show_msg(event):
	    print(name.get())
	name = tk.StringVar()
	players = ttk.Combobox(window, textvariable=name)
	players["values"] = ("成龙", "刘德华", "周星驰")
	players["state"] = "readonly"

	players.current(2)
	# players.set("演员表")
	# print(players.get())

	players.bind("<<ComboboxSelected>>", show_msg)

	return players
