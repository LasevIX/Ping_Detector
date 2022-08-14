from time import perf_counter
import matplotlib as mpl
import matplotlib.backends.backend_tkagg as tkBEnd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tkinter as tk
import subprocess as sp
import re as re
import logging as lg
import CustomExceptionHandler
lg.basicConfig(level=lg.INFO)
class App(tk.Tk):
    def __init__(self,output_csv:str|None=r"example4.csv",input_url:str|None="python.org") -> None:
        super().__init__()
        self.resizable(width=False, height=False)  #custom window settings


        self.output_csv=output_csv
        self.pinged_adress=input_url
        self.MakeWidgets()
        self.ping_stream=sp.Popen(["ping",str(self.pinged_adress),"-t"],stdout=sp.PIPE,universal_newlines=True)
        with open(self.output_csv,'w')as f:
            print("",file=f,end='')  #clearing the file contents. (yes, inefficient, but it's enough)
        with open(self.output_csv,'a') as f:
            print("\"time(s)\",\"Ping(ms)\"",file=f)
        self.start_time_value=perf_counter()
        self.ReadPingStream()

    def ReadPingStream(self):
        self.last_line_read=self.ping_stream.stdout.readline()
        self.after(1000,self.ReadPingStream)
        #input sanitisation
        regex_match=re.search("time=[0-9]*",self.last_line_read)
        if regex_match:self.current_ping_time=regex_match.group()[5:]
        else:self.current_ping_time=np.NaN ;lg.info("failed to detect ping")
        self.time_since_start=round(perf_counter()-self.start_time_value,1)  #time index rounded to tenth for readability
          #log the value to relevant outputs 
        self.title(f"{self.current_ping_time}ms►{self.pinged_adress}")
        with open(self.output_csv,'a') as f:
            print(f"\"{self.time_since_start}\",\"{self.current_ping_time}\"",file=f)

    def MakeWidgets(self):
        self.top_label=tk.Label(self,text=f'pinging {self.pinged_adress}...',font=("Arial","20"))
        self.explaining_label=tk.Label(self,text="")

        self.top_label.pack(side=tk.TOP)
        self.explaining_label.pack(side=tk.TOP)


        




app=App(input_url="google.com")
app.mainloop()