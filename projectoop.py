import Tkinter as tk
import subprocess
#from code import InteractiveInterpreter
from Tkinter import *
import keyboard
from ScrolledText import *
import win32com.client as wincl
import tkFileDialog
import tkMessageBox
import os
import thread, time
voice = 0
row,col = 0,0

#POPUP WINDOW -- OPEN FILE
class popupWindow(object):
	def __init__(self,master):
		top=self.top=tk.Toplevel(master)
		top.resizable(width=False, height=False)
		self.e=Entry(top)
		self.e.bind('<KeyPress>',self.entryboxkeypress2)
		self.e.pack()
		self.val=""
		self.s = wincl.Dispatch("SAPI.SpVoice")
		self.s.Rate=1
		global voice
		self.s.Voice=self.s.GetVoices().Item(voice)
	
	def speak(self,string):
		thread.start_new_thread(self.s.Speak,(string,0))
	
	def entryboxkeypress2(self,event):
		self.speak(event.keysym)
		if event.keysym == "Return":
			self.val=self.e.get()+".py"
			if str(self.val) in os.listdir("C:\\Python27\\PowerPad"):
				self.top.destroy()
			else:
				self.speak("INVALID NAME PLEASE ENTER AGAIN")
				self.top.bell()
				self.e.delete(0,'end')
				self.val=""
		else:pass

#POPUP WINDOW -- SAVING FILE				
class popupWindow1(object):
	def __init__(self,master):
		top1=self.top1=tk.Toplevel(master)
		top1.resizable(width=False, height=False)
		self.e1=Entry(top1)
		self.e1.bind('<KeyPress>',self.entryboxkeypress1)
		self.e1.pack()
		self.val1=""
		self.s = wincl.Dispatch("SAPI.SpVoice")
		self.s.Rate=1
		global voice
		self.s.Voice=self.s.GetVoices().Item(voice)
	
	def checkname(self,filename):
		flag=0
		s='< > : " / \ | ? *'
		for i in s:
			if i in filename:flag=1
			else:flag=0
		return flag
	
	def speak(self,string):
		thread.start_new_thread(self.s.Speak,(string,0))
	
	def entryboxkeypress1(self,event):
		self.speak(event.keysym)
		if event.keysym == "Return":
			self.val1=self.e1.get()
			if len(self.val1)>244 or self.checkname(self.val1):
				self.speak("INVALID NAME PLEASE ENTER AGAIN")
				self.top1.bell()
				self.e1.delete(0,'end')
				self.val1=""
			else:	
				self.val1=self.e1.get()+".py"
				self.top1.destroy()
		else:pass


#class MAINWINDOW
class mainwindow:
	
	def __init__(self,master):
		self.master = master
		if os.path.exists("C:\Python27") or os.path.exists("C:\Python36-32"):
			
			self.frame2 = tk.LabelFrame(self.master, text = "Editor", width = 800, height =self.master.winfo_screenheight(), bd = 5)
			self.frame3 = tk.LabelFrame(self.master, text = "Output", width = self.master.winfo_screenwidth()-830, height =(self.master.winfo_screenheight())/2, bd = 5)
			self.frame2.grid(row=1, column=0, padx=8)
			self.frame2.pack_propagate(0)
			self.frame3.grid(row=1, column=1, sticky='nw')
			self.frame3.pack_propagate(0)
			self.textPad = ScrolledText(self.frame2,width=800,height=1000)
			self.textPad.focus_set()
			self.textPad.bind('<KeyPress>',self.onKeyPress)
			self.textPad.bind('<Control-Key-a>',self.select_all)
			self.textPad.bind('<Control-Key-A>',self.select_all)
			self.outputpad=Text(self.frame3,width=450,height=400)
			self.textPad.pack()
			self.outputpad.pack()
			self.outputpad.configure(state='disabled')
			self.filename=""
			self.final_data=""
			self.entry=0
			self.s = wincl.Dispatch("SAPI.SpVoice")
			self.s.Rate=1
			global voice
			self.special_char = {'(' : 'Parenthesis L' , ')' : 'Parenthestis R' , '[' : 'Bracket L' , ']' : 'Bracket R' , '{' : 'Curly Braces L' , '}' : 'Curly Braces R' , '<' : 'Angle Bracket L' , '>' : 'Angle Bracket R', ':' : 'Colon' , '!' : 'Exclamation Mark' , '~' : 'Tilde' , '^' : 'Caret' , '-' : 'Hyphen' , ' ' : 'Space' , '|' : 'Pipe' , ';' : 'Semicolon' ,'\'' : 'Single Quote' , '"' : 'Double Quote' , '?' : 'Question Mark' , ',' : 'Comma' , '.' : 'Period'}
			if os.path.exists("C:\Python27\PowerPad"):pass 
			else:os.makedirs("C:\Python27\PowerPad")
			os.chdir("C:\\Python27\\PowerPad")
			os.environ["PATH"] += os.pathsep + "C:\Python27\PowerPad"
		else:
			tkMessageBox.showerror("Python Not Found", "Sorry, no Python available")
			s = wincl.Dispatch("SAPI.SpVoice");s.Rate=1;s.Speak("python is not installed, Please intall python on your Computer")
			self.master.destroy()
			
	
	def speak(self,string):
		self.s.Speak(string)
	
	def select_all(self,event):
		self.textPad.tag_add(SEL, "1.0", END)
		self.textPad.mark_set(INSERT, "1.0")
		self.textPad.see(INSERT)
		return 'break'

	def outputconf(self):
		self.outputpad.configure(state='normal')
		self.outputpad.insert('end','>>> Running Your Code\n')
		self.outputpad.configure(state='disabled')
	
	def alreadysave(self,data,filename):
		self.speak("SAVING " + filename)
		self.saved_file = open(filename,"w+")
		self.saved_file.write(data)
		self.saved_file.close()

	def popup(self):
		self.w=popupWindow(self.master)
		self.w.e.focus_set()
		self.master.wait_window(self.w.top)
		self.filename=self.w.val
		
	def open_file(self):
		try:
			self.speak("ENTER THE FILE NAME WITHOUT EXTENSION AND PRESS ENTER")
			self.master.bell()
			self.popup()
			file=open(self.filename,"r")
			contents = file.read()
			self.textPad.delete('0.0','end')
			self.outputpad.configure(state='normal')
			self.outputpad.delete('0.0','end')
			self.outputpad.configure(state='disabled')
			self.textPad.insert('1.0',contents)
			file.close()
			self.final_data=self.textPad.get('1.0', END+'-1c')
			self.textPad.focus_set()
			self.frame2.configure(text=self.filename)
		except IOError:pass
	
	def SaVe(self,data):
		self.final_data=self.data
		if not self.filename:
			self.speak("ENTER THE FILE NAME WITHOUT EXTENSION AND PRESS ENTER")
			self.master.bell()
			self.popup2()
			if str(self.filename) in os.listdir("C:\\Python27\\PowerPad"):
				if self.onreplace() == "yes":
					self.alreadysave(self.data,self.filename)
					self.textPad.focus_set()
				else:
					self.speak("ENTER THE NAME AGAIN")
					self.popup2()
					self.SaVe(self.data)
			else:
				self.SaVe(self.filename)
		else:
			self.alreadysave(self.data,self.filename)
		self.textPad.focus_set()
		self.frame2.configure(text=self.filename)
	
	def popup2(self):
		self.w1=popupWindow1(self.master)
		self.w1.e1.focus_set()
		self.master.wait_window(self.w1.top1)
		self.filename=self.w1.val1
	
	def outputgen(self,filename):
		process = subprocess.Popen(["python", filename], stdout = subprocess.PIPE,stderr = subprocess.PIPE)
		self.output = process.stdout.readlines()
		self.error = process.stderr.readlines()
		process.wait()
		'''if not 'prompt' in os.environ:
			self.speak("input")
			print("in")'''
		
		if self.error:
			self.speak("Error")
			self.errorsay(self.error)
		else:
			self.speak("Output")
			self.outputsay(self.output)
		
	def errorline(self,error):
		s=""
		for i in error:
			if not "line" in i:
				pass
			else:
				s+=i
		x=s.split(",")
		s=""
		for i in x:
			if not "line" in i:
				pass
			else:
				s+=i
		return s
		
	def errorsay(self,error):
		s=self.errorline(error)
		x=((error[-1].split(":"))[0])+ " ON THE " 
		self.outputpad.configure(state='normal')
		self.outputpad.insert('end',x+s)
		self.outputpad.configure(state='disabled')
		l=s.split(' ')
		errorline=(self.textPad.get('1.0', END+'-1c').split("\n"))[int(l[-1][0])-1]
		self.textPad.mark_set("insert", "%d.%d" % (int(l[-1][0]),len(errorline)))
		self.speak(x)
		self.speak(s)
		for i in errorline:
			if i in self.special_char.keys():self.speak(self.special_char[i])
			else:self.speak(i)
	
		
		
	def outputsay(self,output):
		self.outputpad.configure(state='normal')
		for i in output:
			self.speak(i)
			self.outputpad.insert('end',i)
		self.outputpad.configure(state='disabled')
	
	def onexit(self):
		self.speak("PRESS Y TO EXIT AND N TO CANCEL")
		self.master.bell()
		return tkMessageBox.askquestion("Exit", "Are You Sure?")
	
	def onopen(self):
		self.speak("THERE ARE SOME UNSAVED CHANGES DO YOU WANT TO SAVE THE FILE BEFORE OPEN A FILE?")
		self.speak("PRESS Y TO SAVE AND N TO CANCEL")
		self.master.bell()
		return tkMessageBox.askquestion("Save and Open", "Are You Sure?")
	
	def onsave(self):
		self.speak("THERE ARE SOME UNSAVED CHANGES DO YOU WANT TO SAVE THE FILE BEFORE EXIT?")
		self.speak("PRESS Y TO SAVE AND N TO CANCEL")
		self.master.bell()
		return tkMessageBox.askquestion("Save and Exit", "Are You Sure?")
	
	def onreplace(self):
		self.speak("THERE ALREADY EXIXT FILE WITH THE SAME NAME, DO YOU WANT TO REPLACE IT ?")
		self.speak("PRESS Y TO REPLACE AND N TO CANCEL")
		self.master.bell()
		return tkMessageBox.askquestion("Replace", "Are You Sure?")
	
	
	def pressf1(self):
		if self.final_data != self.data:
			if self.onsave() == "yes" :
				self.SaVe(self.data)
				self.final_data=""
				self.filename=""
				self.textPad.delete('0.0','end')
			else:
				self.final_data=""
				self.filename=""
				self.textPad.delete('0.0','end')
		else:
			self.final_data=""
			self.filename=""
			self.textPad.delete('0.0','end')
		
		self.outputpad.configure(state='normal')
		self.outputpad.delete('0.0','end')
		self.outputpad.configure(state='disabled')
		self.frame2.configure(text="Editor")
		self.speak("Opening a new Tab")
		
	
	def pressf2(self):
		if self.final_data != self.data:
			if self.onopen() == "yes" :
				self.SaVe(self.data)
				self.final_data=""
				self.filename=""
				self.textPad.delete('0.0','end')
				self.open_file()
			else:
				self.alreadysave(self.data,self.filename)
				self.final_data=""
				self.filename=""
				self.textPad.delete('0.0','end')
				self.open_file()
		else:self.open_file()	
	
	def pressf4(self):
		if not self.final_data == self.data:
			if self.onsave() == "yes":
				self.SaVe(self.data)
				self.master.destroy()
			else:self.master.destroy()	
		else:
			if self.onexit() == "yes":self.master.destroy()
			else:pass
	
	def pressf5(self):
		if self.filename:
			self.outputconf()
			self.alreadysave(self.data,self.filename)
			self.outputgen(self.filename)
		else:
			self.SaVe(self.data)
			self.outputconf()
			self.outputgen(self.filename)
	
	def pressf8(self):
		global voice
		if voice==0:
			voice=1
			self.s.Voice=self.s.GetVoices().Item(voice)
		else:
			voice=0
			self.s.Voice=self.s.GetVoices().Item(voice)
	
	def pressf11(self):
		self.speak("INSTRUCTIONS ARE ")
		self.speak("PRESS F1 FOR NEW FILE, F2 TO OPEN FILE, F3 TO SAVE FILE, F4 TO EXIT, F5 TO COMPILE, F6 TO LISTEN ALL CODE, F7 TO CLEAR ALL, F8 TO CHANGE VOICE, F9 TO KNOW ABOUT US, F11 FOR INSTRUCTIONS")
	
	def onKeyPress(self,event):
		#global self.filename
		#self.speak(event.keysym)
		#print(event.keysym)
		global row,col
		row,col=self.textPad.index('insert').split('.')
		self.data=self.textPad.get('1.0', END+'-1c')
		
		if event.keysym == "F1":self.pressf1()
		
		elif event.keysym == "F2":
			self.speak("OPENING")
			if self.data == "":self.open_file()
			else:self.pressf2()
		
		elif event.keysym == "F3":
			self.speak("SAVING")
			if self.data == "":pass
			else:self.SaVe(self.data)
		
		elif event.keysym == "F4":
			self.speak("EXITING")
			if self.data == "":
				if self.onexit() == "yes":self.master.destroy()
				else:pass
			else:self.pressf4()
			
		elif event.keysym == "F5":	
			self.speak("COMPILE")
			if self.data == "":pass
			else:self.pressf5()
		
		elif event.keysym == "F6":
			self.speak("CODE IS")
			self.speak(self.data)
		
		elif event.keysym == "F7":
			self.speak("CLEARING ALL CODE")
			self.textPad.delete("0.0",'end')

		elif event.keysym == "F8":
			self.speak("CHANGING VOICE")
			self.pressf8()
		
		elif event.keysym == "F9":
			#self.speak("ABOUT Us");
			self.speak("CREATED BY NANDISH PATEL")
		
		elif event.keysym == "F11":self.speak("INSTRUCTIONS");self.pressf11()
		
		else:pass		

def main():
	root = tk.Tk(className = " PowerPad")
	root.state('zoomed')
	app=mainwindow(root)
	root.mainloop()

if __name__ == '__main__':
	main()