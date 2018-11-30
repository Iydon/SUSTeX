def start(window):
	import tkinter as tk
	def print_item(event):
	    print (lb.get(lb.curselection()))
	var = tk.StringVar()
	lb = tk.Listbox(window, height=5, selectmode=tk.BROWSE, listvariable = var)
	lb.bind('<ButtonRelease-1>', print_item)
	list_item = list(range(10))
	for item in list_item:
	    lb.insert(tk.END,item)
	scrl = tk.Scrollbar(lb)
	scrl.pack(side=tk.RIGHT,fill=tk.Y)
	lb.configure(yscrollcommand=scrl.set)

	scrl['command'] = lb.yview  # 指定Scrollbar的command的回调函数是Listbar的yview
	return lb
