import tkinter
import requests
from tkinter import font
from tkinter import messagebox
import urllib.parse as urlparse
from urllib.parse import urlencode
import json
import sys

def sendRequestButtonClicked():
	url=URLTextfeild.get()
	if(url==""):
		messagebox.showerror("Error", "URL Field should not be empty!")
		return
	print(url)
	try:
		methodValue=currvalue.get()
		#sending Request
		if methodValue=="GET":
			response=requests.get(url)			
		elif methodValue=="POST":
			body=bodyText.get("1.0","end-1c")
			response=requests.post(url=url,data=body)
		else:
			pass
		#response evaluation
		if response.status_code==200:
			responseTextLabel.config(text=response.status_code,bg="green",fg="black")
			responseHeaderText.config(state="normal",fg='green')
			responseHeaderText.insert(1.0,json.dumps(dict(response.headers),indent=1))
			responseHeaderText.config(state="disabled")
			responseBodyText.config(state="normal",fg='green')
			responseBodyText.insert(1.0,response.text)
			responseBodyText.config(state="disabled")
		else:
			responseTextLabel.config(text=response.status_code,bg="red",fg="black")			
			responseHeaderText.config(state="normal",fg='red')
			responseHeaderText.insert(1.0,json.dumps(dict(response.headers),indent=1))
			responseHeaderText.config(state="disabled")
			responseBodyText.config(state="normal",fg='red')
			responseBodyText.insert(1.0,response.text)
			responseBodyText.config(state="disabled")		
	except requests.exceptions.RequestException as e:
		messagebox.showerror("Error",str(e))
	except requests.exceptions.HTTPError as e:
		messagebox.showerror("Error",str(e))
	except Exception as e: 
		messagebox.showerror("Error",str(e))
			

def AddQueryString():
	url=URLTextfeild.get()
	if(url==""):
		messagebox.showerror("Error", "URL Field should not be empty!")
		return
	name=queryParameterNameLabelfeild.get()
	value=queryParameterValueLabelfeild.get()
	if name=="" or value=="":
		messagebox.showerror("Error", "Query Paramter Name and Query Paramter Value both are required!")
		return
	params = {name:value}
	url_parts = list(urlparse.urlparse(url))
	query = dict(urlparse.parse_qsl(url_parts[4]))
	query.update(params)
	url_parts[4] = urlencode(query)
	url=urlparse.urlunparse(url_parts)
	print(url)
	URLTextfeild.delete(0,"end")
	URLTextfeild.insert(0,url)
	



if __name__=="__main__":
	top=tkinter.Tk()
	top.geometry("%dx%d+%d+%d" %(1000,600,160,50))
	top.title("RestletServices Checker")
	top.resizable(0,0)
	canvas=tkinter.Canvas(top,bg="white",height=600,width=1000)
	canvas.pack()



#METHOD AND OPTIONS	
	methodLabel=tkinter.Label(canvas,text="METHOD",bg="white" ,fg="Black" ,font=font.Font( family="{Times}", size=12, weight='bold'))
	methodLabel.place(x=10,y=10)
	optionsfont =font.Font(family="{Times}",size=11,weight="bold")
	OPTIONS=["GET","POST"]
	currvalue=tkinter.StringVar(canvas)
	currvalue.set(OPTIONS[0])
	optionmenu=tkinter.OptionMenu(canvas,currvalue,*OPTIONS)
	optionmenu.config(font=optionsfont,bg="lemon chiffon",activebackground="navajo white",width=8)
	optionmenu['menu'].config(font=font.Font(family="{Times}",size=10),bg='navajo white',activebackground="lemon chiffon")
	optionmenu.place(x=12,y=32)


#URL LABEL AND SEND BUTTON
	URLLabel=tkinter.Label(canvas,text="URL",bg="white",fg="black",font=font.Font(family="{Times}",size=12,weight='bold'))
	URLLabel.place(x=150,y=10)
	URLTextfeild=tkinter.Entry(canvas,bg="white",bd=1,font=font.Font(family="{Times}",size=15),justify="left",width=66)
	URLTextfeild.place(x=150,y=32,height=34,width=700)
	sendbutton=tkinter.Button(bg="lemon chiffon",activebackground="navajo white",bd=4,fg="black",font=font.Font(family="{Times}",size=12,weight="bold",slant="italic"),text="SEND",command=sendRequestButtonClicked)
	sendbutton.place(x=868,y=31,height=36,width=120)

#SENDING QUERY PART
	queryParameterLabel=tkinter.Label(canvas,text="QUERY PARAMETERS",bg="white",fg="black",font=font.Font(family="{Times}",size=12,weight='bold'))
	queryParameterLabel.place(x=10,y=90)
	queryParameterNameLabel=tkinter.Label(canvas,text="Name:",bg="white",fg="black",font=font.Font(family="{Times}",size=10,weight='bold'))
	queryParameterNameLabel.place(x=15,y=118)
	queryParameterNameLabelfeild=tkinter.Entry(canvas,bg="white",bd=1,font=font.Font(family="{Times}",size=11),justify="left",width=30)
	queryParameterNameLabelfeild.place(x=68,y=118,height=20,width=128)
	queryParameterValueLabel=tkinter.Label(canvas,text="Value:",bg="white",fg="black",font=font.Font(family="{Times}",size=10,weight='bold'))
	queryParameterValueLabel.place(x=205,y=118)
	queryParameterValueLabelfeild=tkinter.Entry(canvas,bg="white",bd=1,font=font.Font(family="{Times}",size=11),justify="left",width=30)
	queryParameterValueLabelfeild.place(x=258,y=118,height=20,width=128)
	addQuerybutton=tkinter.Button(bg="lemon chiffon",activebackground="navajo white",bd=4,fg="black",font=font.Font(family="{Times}",size=11,weight="bold",slant="italic"),text="+",command=AddQueryString)
	addQuerybutton.place(x=398,y=115,height=26,width=30)


#SENDING BODY PART
	bodyLabel=tkinter.Label(canvas,text="BODY REQUEST",bg="white",fg="black",font=font.Font(family="{Times}",size=12,weight='bold'))
	bodyLabel.place(x=10,y=158)
	bodyTextYScrollbar=tkinter.Scrollbar(canvas,orient="vertical")
	bodyTextYScrollbar.place(x=413,y=183,height=387,width=18)
	bodyTextXScrollbar=tkinter.Scrollbar(canvas,orient="horizontal")
	bodyTextXScrollbar.place(x=21,y=553,height=18,width=392)
	bodyText=tkinter.Text(canvas,bg="white",wrap="none",font=font.Font(family="{Times}",size=11),width=43,yscrollcommand=bodyTextYScrollbar.set,xscrollcommand=bodyTextXScrollbar.set)
	bodyTextYScrollbar.config(command=bodyText.yview,activebackground="navajo white",bg="lemon chiffon",bd=4)
	bodyTextXScrollbar.config(command=bodyText.xview,activebackground="navajo white",bg="lemon chiffon",bd=4)
	bodyText.place(x=20,y=183,height=370)


#DRAWING LINE BETWEEN RESPONSE AND REQUEST
	canvas.create_line(452,90,452,570,width=2,fill="gray25")


#RESPONSE PART
	responseLabel=tkinter.Label(canvas,text="RESPONSE",bg="white",fg="black",font=font.Font(family="{Times}",size=12,weight='bold'))	
	responseLabel.place(x=470,y=90)
	responseTextLabel=tkinter.Label(canvas,anchor="nw",bg="white",fg="black",font=font.Font(family="{Times}",size=11,weight='bold'),bd=1,justify="left",borderwidth=2,relief='ridge')
	responseTextLabel.place(x=477,y=115,width=500,height=25)


#RESPONSE HEADER PART
	responseHeaderLabel=tkinter.Label(canvas,text="RESPONSE HEADERS",bg="white",fg="black",font=font.Font(family="{Times}",size=12,weight='bold'))
	responseHeaderLabel.place(x=470,y=158)
	responseHeaderYScrollbar=tkinter.Scrollbar(canvas,orient="vertical")
	responseHeaderYScrollbar.place(x=960,y=185,height=96,width=18)
	responseHeaderXScrollbar=tkinter.Scrollbar(canvas,orient="horizontal")
	responseHeaderXScrollbar.place(x=478,y=263,height=18,width=482)
	responseHeaderText=tkinter.Text(canvas,bg="white",wrap='none',font=font.Font(family="{Times}",size=11),width=43,yscrollcommand=responseHeaderYScrollbar.set,xscrollcommand=responseHeaderXScrollbar.set)
	responseHeaderText.config(state="disabled")
	responseHeaderYScrollbar.config(command=responseHeaderText.yview,activebackground="navajo white",bg="lemon chiffon",bd=4)
	responseHeaderXScrollbar.config(command=responseHeaderText.xview,activebackground="navajo white",bg="lemon chiffon",bd=4)
	responseHeaderText.place(x=478,y=185,width=482,height=78)


#RESPONSE BODY PART
	responseBodyHeaderLabel=tkinter.Label(canvas,text="RESPONSE BODY",bg="white",fg="black",font=font.Font(family="{Times}",size=12,weight='bold'))
	responseBodyHeaderLabel.place(x=470,y=296)
	responseBodyYScrollbar=tkinter.Scrollbar(canvas,orient="vertical")
	responseBodyYScrollbar.place(x=957,y=316,height=255,width=18)
	responseBodyXScrollbar=tkinter.Scrollbar(canvas,orient="horizontal")
	responseBodyXScrollbar.place(x=475,y=553,height=18,width=482)
	responseBodyText=tkinter.Text(canvas,bg="white",wrap='none',font=font.Font(family="{Times}",size=11),width=43,yscrollcommand=responseBodyYScrollbar.set,xscrollcommand=responseBodyXScrollbar.set)
	responseBodyText.config(state="disabled")
	responseBodyYScrollbar.config(command=responseBodyText.yview,activebackground="navajo white",bg="lemon chiffon",bd=4)
	responseBodyXScrollbar.config(command=responseBodyText.xview,activebackground="navajo white",bg="lemon chiffon",bd=4)
	responseBodyText.place(x=475,y=316,height=237,width=482)


	top.mainloop()
