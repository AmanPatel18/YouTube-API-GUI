from tkinter import *
from YouTube import YouTube
from PIL import ImageTk
import PIL.Image
import os

win=Tk()
win.config(bg='black')
win.title('YouTube')
win.iconbitmap("C:\\Users\\patel\\Documents\\System Icons\\YT.ico")
win_x = 820
win_y = 500
centre_x = 683
centre_y = 384
x = centre_x-int(win_x/2)
y = centre_y-int(win_y/2)
win.geometry(f'820x500+{x}+{y}')
win.resizable(0,0)

yt=YouTube()

# function to fetch title and subscribers from the channel
def get_channel(reference):
    text_field.delete(0,END)
    try:
        title,subs=yt.channel_info(ch_id=reference)
    except:
        title,subs=yt.channel_info(username=reference)

    text_box.delete(1.0,END)
    text_box.insert(END,f'Channel Title: {title}\n')
    text_box.insert(END,f'Total Subscribers: {subs}')

# function to get the total duration of all the videos in the playlist
def get_play_dur(reference):
    text_field.delete(0,END)
    dur=yt.playlist_duration(pl_id=reference)
    text_box.delete(1.0,END)
    text_box.insert(END,f'Total Duration: {dur}')

# function to sort the videos on the basis of most popular (most viewed) video in the playlist
def get_pv(reference):
    text_field.delete(0,END)
    videos_list=yt.popular_videos(pl_id=reference)
    text_box.delete(1.0,END)
    for video in videos_list:
        text_box.insert(END,"Views: {} \nURL: {} \n".format(video['views'],video['url'])+'\n')        

# function to clear the output from the text box
def clear():
    text_box.delete(1.0,END)

# function to remove the placeholder kind text from the text field
def text_field_change(event):
    text_field.configure(state=NORMAL)
    text_field.delete(0,END)

# creating canvas for YouTube heading and icon
my_canvas=Canvas(win,bg='black',width=400,height=125,highlightthickness=5,highlightbackground='red')
my_canvas.place(x=10,y=10)

# inserting a text inside the my_canvas
yt_label1=Label(my_canvas,text='You',font=('times 55 bold'),fg='red',bg='black',height=1)
yt_label1.place(x=10,y=20)

# inserting a text inside the my_canvas
yt_label1=Label(my_canvas,text='Tube',font=('times 55 bold'),fg='white',bg='black',height=1)
yt_label1.place(x=140,y=20)

# inserting logo inside the my_canvas
logo=ImageTk.PhotoImage(PIL.Image.open("C:\\Users\\patel\\Documents\\System Icons\\yt.png"))
logo_label=Label(my_canvas,image=logo,bg='black')
logo_label.place(x=320,y=40)

# creating frame for text_box
my_frame=Frame(win,bg='black',width=380, height=500)
my_frame.place(x=420,y=5)

# creating a scrollbar for text_box 
bar=Scrollbar(my_frame,orient=VERTICAL)

# creating text box for diaplaying result
text_box=Text(my_frame,bg='#e9dd9a',fg='black',font=('Helvetica 15 bold'),width=31,height=19,highlightthickness=5,highlightbackground='#6c1002',selectbackground='#6c1002',yscrollcommand=bar.set)

# configuring scrollbar
bar.config(command=text_box.yview)
bar.pack(side=RIGHT,fill=Y)

text_box.pack(padx=10,pady=10)

# creating a text field
text_field=Entry(win,width=25,font=('Helvetica 20 bold'),bg='white',fg='black',bd=10)
text_field.place(x=15,y=170)
text_field.insert(END,'    Channel ID / Playlist ID')
text_field.configure(state=DISABLED)

# binding the event key with text_field
text_field.bind('<Button-1>',text_field_change)

# creating buttons for getting subscribers
sub_btn=Button(win, width=15,text='Subscribers',bg='red',fg='black',font=('times 20 bold'),command=lambda:get_channel(text_field.get()))
sub_btn.place(x=95,y=250)

# creating buttons for getting playlist duration
dur_btn=Button(win, width=15,text='Playlist Duration',bg='red',fg='black',font=('times 20 bold'),command=lambda:get_play_dur(text_field.get()))
dur_btn.place(x=95,y=310)

# creating buttons for getting popular videos
pv_btn=Button(win, width=15,text='Popular Videos',bg='red',fg='black',font=('times 20 bold'),command=lambda:get_pv(text_field.get()))
pv_btn.place(x=95,y=370)

# creating buttons for clearing the output in the text box
clear_btn=Button(win, width=15,text='Clear',bg='red',fg='black',font=('times 20 bold'),command=clear)
clear_btn.place(x=95,y=430)

win.mainloop()
