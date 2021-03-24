import tkinter as tk
from aspect_analysis import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()
nlp = stanza.Pipeline()
stop_words = set(stopwords.words('english'))



Font = ("monaco",18,"bold")
c1 = "white"
c2 = "purple"
pad = 8
root = tk.Tk()
root.state('zoomed')
w = root.winfo_screenwidth()
h = root.winfo_screenheight()


def pred():
    lb.delete(0,"end")
    txt = e.get()
    findic = aspect_analysis(txt, stop_words, nlp)
    c = 0
    print(findic)
    for i in findic:
        s = f"{i} {findic[i]}"
        scores = sid.polarity_scores(s)
        print(scores)
        scores.pop("compound")
        scores = sorted(scores.items(),key=lambda x : x[1],reverse=True)[0][0]
        print(i,scores)
        lb.insert(c, f"{i} ==> {scores}")
        c+=1
   

f1 = tk.Frame(root,height=h*0.1,width=w,bg="purple") 
f1.place(x=0,y=0)

l0 = tk.Label(text="Aspect Based Sentiment Analysis",fg=c1,bg=c2,font=Font)
l0.place(x=0,y=0)
root.update_idletasks()
l0.place(x=int((w/2)-(l0.winfo_width()/2)),y=int((f1.winfo_height()/2)-(l0.winfo_height()/2)))

f2 = tk.Frame(root,height=h*0.9,width=w) 
f2.place(x=0,y=h*0.1)
root.update_idletasks()
 
f3 = tk.Frame(f2) 

l1 = tk.Label(f3,text="<INPUT TEXT>",font=Font,fg=c1,bg=c2)
l1.place(x=0,y=0)
root.update_idletasks() 
l1.place(x=int((w/2)-(l1.winfo_width()/2)),y=pad)

e = tk.Entry(f3,font=Font,fg=c2)
e.place(x=0,y=0,width=w*0.6)
root.update_idletasks() 
e.place(x=int(int(w/2)-int(e.winfo_width()/2)),y=l1.winfo_height()+(pad*2))

b = tk.Button(f3,text="Predict",font=Font,bg=c2,fg=c1,border=5,command=pred)
b.place(x=0,y=0)
root.update_idletasks() 
b.place(x=int(int(w/2)-int(b.winfo_width()/2)),y=l1.winfo_height()+e.winfo_height()+(pad*3))

root.update_idletasks() 
f3.place(x=0,y=0,width=w,height=l1.winfo_height()+e.winfo_height()+b.winfo_height()+(pad*4))

f4 = tk.Frame(f2) 

l2 = tk.Label(f4,text="<Result>",font=Font,fg=c1,bg=c2)
l2.place(x=0,y=0)
root.update_idletasks() 
l2.place(x=int((w/2)-(l2.winfo_width()/2)),y=pad)

lb = tk.Listbox(f4,bg=c1,font=Font)
lb.place(x=0,y=0)
root.update_idletasks() 
lb.place(x=int((w/2)-(lb.winfo_width()/2)),y=l2.winfo_height()+pad*2)

root.update_idletasks() 
f4.place(x=0,y=f3.winfo_height(),width=w,height=l2.winfo_height()+lb.winfo_height()+(pad*3))

root.mainloop()
