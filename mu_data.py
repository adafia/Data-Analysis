# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 13:02:38 2017

@author: qanda
"""

import tkinter as tk
from tkinter import ttk
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure 
import matplotlib.animation as animation
from matplotlib import style
import pandas as pd
from functools import partial

#from xlrd.sheet import ctype_text
import xlrd
from collections import defaultdict

LARGE_FONT = ('Verdana', 12)
MEDIUM_FONT = ('Verdana', 10)
SMALL_FONT = ('Verdana', 8)




style.use('ggplot')

f = Figure(figsize = (5, 5), dpi = 100)
a = f.add_subplot(111)



def popupmsg(msg):
    popup = tk.Tk()
    
    popup.wm_title("!")
    label = ttk.Label(popup, text = msg, font = MEDIUM_FONT)
    label.pack(side = "top", fill = "x", pady = 10)
    B1 = ttk.Button(popup, text = "Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()


def animate(i):
    pullData = open('sampleData.txt', 'r').read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))
            
    a.clear()
    a.fill_between(xList, yList, 0, color = 'grey')
        

class pen_app(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self, default ='C:/Users/qanda/OneDrive/Documents/Python Scripts/PEN/logo.ico')
        tk.Tk.wm_title(self, 'PEN Data Visualization')
        container = tk.Frame(self)
        container.pack(side = 'top', fill = 'both', expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff = 0)
        filemenu.add_command(label = "Save Graph", command = lambda:popupmsg("Not Supported yet!!"))
        filemenu.add_separator()
        filemenu.add_command(label = "Exit", command = lambda:popupmsg("Not Supported yet!!"))
        menubar.add_cascade(label = "File", menu = filemenu)
        
        
        tk.Tk.config(self, menu = menubar)
        
        self.Frames = {}
        for F in (Home, MainMenu, PageTwo, end_survey):
            frame = F(container, self)
            self.Frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = 'nsew')
        self.show_frame(Home)
        
    def show_frame(self, cont):
        frame = self.Frames[cont]
        frame.tkraise()
        
        
class Home(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = ttk.Label(self, text = "Practical Education Network", font = LARGE_FONT)
        label.pack(pady = 2, padx = 10)
        
        label = ttk.Label(self, text = "Data Analysis Automation", font = MEDIUM_FONT)
        label.pack(pady = 2, padx = 10)
    
        main_menu = ttk.Button(self, text = "Main Menu", command = lambda: controller.show_frame(MainMenu))
        main_menu.pack()
        
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        
        
    
        
class MainMenu(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        def select_file ():
            filechooser = tk.filedialog.askopenfilename( filetypes = ( ("Excel Files", "*.xlsx"),("All files", "*.*")))    
        
            label1 = ttk.Label(self, text = "%s" % filechooser)
            label1.grid(row = 5, column = 2, columnspan = 15, sticky='w', pady = 10, padx = 10)
       
            wb = xlrd.open_workbook("%s" % filechooser)
            sh_names = wb.sheet_names()
            num_sheets = len(sh_names)
        
            def load_sheets(i):
                #xl_sheet = wb.sheet_by_name(sh_names[i])
                df = pd.read_excel("%s" % filechooser, "%s" % sh_names[i])
                return df
            
            list_of_widgets = []
            selected = tk.StringVar(0)
            for i in range(0, num_sheets):
                
                sheet_select = ttk.Label(self, text = "Please Select Sheet...", font = MEDIUM_FONT)
                sheet_select.grid(row = 6, column = 0, columnspan = 5, sticky='w', pady = 5, padx = 10)
                
                button = ttk.Radiobutton(self, text="%s" % sh_names[i],
                                    command=partial(load_sheets, i), value = i, variable = selected)
                button.grid(sticky ='w', pady = 5, padx = 10)#row = 7, column = i+1, sticky='w', pady = 10, padx = 10)  
                list_of_widgets.append(button)
                
                
                
            def analyze_data ():
                popup = tk.Tk()
                
                nav_frame = tk.Frame(popup)
                nav_frame.grid(row = 6, column = 1, columnspan = 6, sticky='w', pady = 5, padx = 10)
                
                wb = xlrd.open_workbook("%s" % filechooser)
                sh_names = wb.sheet_names()
                
                x = selected.get()
                x_int = int(x)
                x_name = sh_names[x_int]
                popup.wm_title("%s" % x_name)
                
                
               
                df = pd.read_excel("%s" % filechooser, "%s" % sh_names[x_int])
                for i in sh_names: 
                    gender = df['Gender'] #.astype('category')
                    name = df['Name']
                    age = df['Age']
                    district = df['District']
                    school = df['School']
                    private_public = df['Is your school']	
                    settlement_type = df['Type of settlement']
                    subjects = df['Subjects you teach']	
                    classes = df['Forms you teach']	
                    teaching_exp = df['# of years teaching experience']	
                    training_college = df['Did you attend teacher training college?']	
                    if_yes = df['If yes, which one?']	
                    mandatory_trainings = df['How many mandatory trainings did you attend last year?']
                    optional_trainings = df['How many optional ones?']	
                    training_areas = df['What types of trainings were they?']	
                    meetings_DSC = df['How many times per year do you meet your District Science Coordinator?']	
                    preparatory_period_practcal = df['If you had 10 hours to prepare one hands-on activity for your class, how many hours would you use?']	
                    practical_frequency = df['How many hands-on activities do you perform for one class every month?']	
                    practical_Confidence = df['How confident are you to teach a hands-on activity tomorrow?']	
                    practical_feasibilty = df['How feasible is it to carry out a hands-on activity in your classroom?']	
                    example_of_practial = df["What is an example of a hands-on activity you have done in your classroom? If you haven't done one, what teaching techniques do you use?"] 
                    perceived_benefits_of_practical = df['What do you see as the benefits of doing hands-on activities?']	
                    challenges = df['What do you see as the challenges?']	
                    difficult_topics = df['What topics are the hardest for you to teach? Why?']
                    personal_aspirations = df['What are your personal aspirations?']	
                    part_time_jobs = df['What kinds of part-time jobs do you do?']	
                    aspirations_students = df['What are your aspirations for your students?']	
                    aim_science_math = df['What do you believe the purpose of science/math education is?']	
                    STEM = df['What does the word STEM mean to you?']	
                    cost = df['How much money would your colleagues pay for this workshop? '] 	
                    hear_abt_PEN = df['How did you learn about this workshop?']	
                    comms = df['What is your preferred mode of communication?']	
                    contact = df['Please provide that contact info here']
                    sign = df['Signature']
                    notes = df['My Notes']
                    
                    def plot_gender():
                        g = {}
                
                        for i in gender:
                            key = i[0]
                            if key not in g:
                                g[key] = []
                            g[key].append(i)
                            
               
                        # Counting the data in the Gender column 
                        g = defaultdict(int)
                        for i in gender:
                            g[i] += 1     
            
                        gender_v = list(g.keys())
                        gender_fr = list(g.values())
                        gender_v[0] = 'Female'
                        gender_v[1] = 'Male'
                         
                        fig = Figure(figsize = (5, 5), dpi = 100)
                        a = fig.add_subplot(111) 
                        a.pie(gender_fr, labels = gender_v, autopct = '%1.i%%')
                        a.set_title('Gender Distribiution for ' "%s" % x_name)
                          
                        canvas = FigureCanvasTkAgg(fig, popup)
                        canvas.show()
                        canvas.get_tk_widget().grid(row = 10, column = 1, columnspan = 10, pady = 10, padx = 10) 
                        toolbar = NavigationToolbar2TkAgg(canvas, nav_frame)
                        toolbar.update()
                        canvas._tkcanvas.grid(row = 5, column = 1, columnspan = 10, pady = 10, padx = 10) 
                        
                        
                    def plot_age():
                        age = df['Age']
                        age = list(age)
                        
                        a = []
                        b = []
                        c = []
                        d = []
                        e = []
                        for i in age:
                            if i <= 20:
                                a.append(i)
                            elif 20 < i <= 30:
                                b.append(i)
                            elif 30 < i <= 40:
                                c.append(i)
                            elif 40 < i <= 50:
                                d.append(i)
                            elif 50 < i <= 60:
                                e.append(i)
                        a_fr = len(a)
                        b_fr = len(b)
                        c_fr = len(c)
                        d_fr = len(d)
                        e_fr = len(e)
                        age_d = {'0 to 20(yrs)':a_fr,'21 to 30(yrs)':b_fr,'31 to 40(yrs)':c_fr, '41 to 50(yrs)':d_fr,'51 to 60(yrs)':e_fr}
                        age_v = list(age_d.keys())
                        age_fr = list(age_d.values())
                          
                        fig = Figure(figsize = (5, 5), dpi = 100)
                        a = fig.add_subplot(111) 
                        a.pie(age_fr, labels = age_v,autopct = '%1.i%%')
                        a.set_title('Age Distribiution for ' "%s" % x_name)
                           
                        canvas = FigureCanvasTkAgg(fig, popup)
                        canvas.show()
                        canvas.get_tk_widget().grid(row = 10, column = 1, columnspan = 6, pady = 10, padx = 10) 
                        toolbar = NavigationToolbar2TkAgg(canvas, nav_frame)
                        toolbar.update()
                        canvas._tkcanvas.grid(row = 5, column = 1, columnspan = 6, pady = 10, padx = 10)
            
            
                    
                    def plot_sch_type():
                        s = {}
                        for i in private_public:
                            key = len(i)
                            if key not in s:
                                s[key] = []
                            s[key].append(i)   
                        #print(s)
                    
                        s = defaultdict(int)
                        for i in private_public:
                            s[i] += 1 
                            
                        private_public_v = list(s.keys())
                        private_public_fr = list(s.values())
                        private_public_v[0] = 'Private'
                        private_public_v[1] = 'Public'
                        private_public_v[2] = 'Missing Data'
                      
                        fig = Figure(figsize = (5, 5), dpi = 100)
                        a = fig.add_subplot(111) 
                        a.pie(private_public_fr, labels = private_public_v, autopct = '%1.i%%')
                        a.set_title('Private/Public School Distribiution for ' "%s" % x_name)
                   
                        canvas = FigureCanvasTkAgg(fig, popup)
                        canvas.show()
                        canvas.get_tk_widget().grid(row = 10, column = 1, columnspan = 6, pady = 10, padx = 10) 
                        toolbar = NavigationToolbar2TkAgg(canvas, nav_frame)
                        toolbar.update()
                        canvas._tkcanvas.grid(row = 5, column = 1, columnspan = 6, pady = 10, padx = 10)
                    
                    
                    def plot_sett_typ():
                        sett = {}
                        for i in settlement_type:
                            key = i[0]
                            if key not in sett:
                                sett[key] = []
                            sett[key].append(i)   
                        #print(sett)
             
                        sett = defaultdict(int)
                        for i in settlement_type:
                            sett[i] += 1 
                        #print(sett)
             
                        sett_typ_v = list(sett.keys())
                        sett_typ_fr = list(sett.values())
                        
                        fig = Figure(figsize = (5, 5), dpi = 100)
                        a = fig.add_subplot(111) 
                        a.pie(sett_typ_fr, labels = sett_typ_v, autopct = '%1.i%%')
                        a.set_title('Human Settlement Type Distribiution for ' "%s" % x_name)
                         
                        canvas = FigureCanvasTkAgg(fig, popup)
                        canvas.show()
                        canvas.get_tk_widget().grid(row = 10, column = 1, columnspan = 6, pady = 10, padx = 10) 
                        toolbar = NavigationToolbar2TkAgg(canvas, nav_frame)
                        toolbar.update()
                        canvas._tkcanvas.grid(row = 5, column = 1, columnspan = 6, pady = 10, padx = 10)
                    
                    
                    
                    def plot_training_college ():
                        t = {}
                        for i in training_college:
                            key = len(i)
                            if key not in t:
                                t[key] = []
                            t[key].append(i)   
                        #print(t)
                   
                        t = defaultdict(int)
                        for i in training_college:
                            t[i] += 1 
                        #print(t)
                    
                        training_college_v = list(t.keys())
                        training_college_fr = list(t.values())
                        training_college_v[0] = 'No'
                        training_college_v[1] = 'Yes'
                        training_college_v[2] = 'Missing Data'
                    
                        fig = Figure(figsize = (5, 5), dpi = 100)
                        a = fig.add_subplot(111) 
                        a.pie(training_college_fr, labels = training_college_v, autopct = '%1.i%%')
                        a.set_title('Training College Attendance Distribiution for ' "%s" % x_name)
                        
                        canvas = FigureCanvasTkAgg(fig, popup)
                        canvas.show()
                        canvas.get_tk_widget().grid(row = 10, column = 1, columnspan = 6, pady = 10, padx = 10) 
                        toolbar = NavigationToolbar2TkAgg(canvas, nav_frame)
                        toolbar.update()
                        canvas._tkcanvas.grid(row = 5, column = 1, columnspan = 6, pady = 10, padx = 10)
                        
                        
                        
            
            
            
                B1 = tk.Button(popup, text = "Close", command = popup.destroy, fg = "white", bg = "red")
                B1.grid(row = 0)
                
                gender_b = ttk.Button(popup, text = "GENDER", command = plot_gender)
                gender_b.grid(row = 1, column = 1, pady = 10, padx = 10)
                
                age_b = ttk.Button(popup, text = "AGE", command = plot_age)
                age_b.grid(row = 1, column = 0, pady = 10, padx = 10)
                
                training_b = ttk.Button(popup, text = "TRAINING COLLEGE", command = plot_training_college)
                training_b.grid(row = 1, column = 2, pady = 10, padx = 10)
                
                sch_b = ttk.Button(popup, text = "SCHOOL TYPE", command = plot_sch_type)
                sch_b.grid(row = 1, column = 3, pady = 10, padx = 10)
                
                settlement_b = ttk.Button(popup, text = "SETTLEMENT TYPE", command = plot_sett_typ)
                settlement_b.grid(row = 1, column = 4, pady = 10, padx = 10)
                
                popup.geometry("900x650")
                popup.mainloop()
                
                
                
            analyze_dat = tk.Button(self, text = "Analyze Selected Sheet", command = analyze_data, bg = "grey", fg = "white")
            analyze_dat.grid(row = 8, column = 10, sticky='w', pady = 5, padx = 10)
                
                
            def cleargrid ():
                for widget in list_of_widgets:
                    widget.destroy()
                    
            def concat_sheets ():
                popup = tk.Tk()
                
                nav_frame = tk.Frame(popup)
                nav_frame.grid(row = 6, column = 1, columnspan = 6, sticky='w', pady = 5, padx = 10)
                
                file = r'%s' % filechooser
                list_dfs = []
                popup.wm_title("%s" % filechooser)
                
                xls = xlrd.open_workbook(file, on_demand=True)
                for sheet_name in xls.sheet_names():
                    df = pd.read_excel(file,sheet_name)
                    list_dfs.append(df)
                dfs = pd.concat(list_dfs,axis=0)
                
                
                for i in sh_names: 
                    gender = dfs['Gender'] #.astype('category')
                    name = dfs['Name']
                    age = dfs['Age']
                    district = dfs['District']
                    school = dfs['School']
                    private_public = dfs['Is your school']	
                    settlement_type = dfs['Type of settlement']
                    subjects = dfs['Subjects you teach']	
                    classes = dfs['Forms you teach']	
                    teaching_exp = dfs['# of years teaching experience']	
                    training_college = dfs['Did you attend teacher training college?']	
                    if_yes = dfs['If yes, which one?']	
                    mandatory_trainings = dfs['How many mandatory trainings did you attend last year?']
                    optional_trainings = dfs['How many optional ones?']	
                    training_areas = dfs['What types of trainings were they?']	
                    meetings_DSC = dfs['How many times per year do you meet your District Science Coordinator?']	
                    preparatory_period_practcal = dfs['If you had 10 hours to prepare one hands-on activity for your class, how many hours would you use?']	
                    practical_frequency = dfs['How many hands-on activities do you perform for one class every month?']	
                    practical_Confidence = dfs['How confident are you to teach a hands-on activity tomorrow?']	
                    practical_feasibilty = dfs['How feasible is it to carry out a hands-on activity in your classroom?']	
                    example_of_practial = dfs["What is an example of a hands-on activity you have done in your classroom? If you haven't done one, what teaching techniques do you use?"] 
                    perceived_benefits_of_practical = dfs['What do you see as the benefits of doing hands-on activities?']	
                    challenges = dfs['What do you see as the challenges?']	
                    difficult_topics = dfs['What topics are the hardest for you to teach? Why?']
                    personal_aspirations = dfs['What are your personal aspirations?']	
                    part_time_jobs = dfs['What kinds of part-time jobs do you do?']	
                    aspirations_students = dfs['What are your aspirations for your students?']	
                    aim_science_math = dfs['What do you believe the purpose of science/math education is?']	
                    STEM = dfs['What does the word STEM mean to you?']	
                    cost = dfs['How much money would your colleagues pay for this workshop? '] 	
                    hear_abt_PEN = dfs['How did you learn about this workshop?']	
                    comms = dfs['What is your preferred mode of communication?']	
                    contact = dfs['Please provide that contact info here']
                    sign = dfs['Signature']
                    notes = dfs['My Notes']
                    
                    def plot_gender():
                        g = {}
                
                        for i in gender:
                            key = i[0]
                            if key not in g:
                                g[key] = []
                            g[key].append(i)
                            
               
                        # Counting the data in the Gender column 
                        g = defaultdict(int)
                        for i in gender:
                            g[i] += 1     
            
                        gender_v = list(g.keys())
                        gender_fr = list(g.values())
                        gender_v[0] = 'Female'
                        gender_v[1] = 'Male'
                    
                        fig = Figure(figsize = (5, 5), dpi = 100)
                        a = fig.add_subplot(111) 
                        a.pie(gender_fr, labels = gender_v, autopct = '%1.i%%')
                        a.set_title('Gender Distribiution for Districts')
                        
                        canvas = FigureCanvasTkAgg(fig, popup)
                        canvas.show()
                        canvas.get_tk_widget().grid(row = 10, column = 1, columnspan = 6, pady = 10, padx = 10) 
                        toolbar = NavigationToolbar2TkAgg(canvas, nav_frame)
                        toolbar.update()
                        canvas._tkcanvas.grid(row = 5, column = 1, columnspan = 6, pady = 10, padx = 10) 
                        
                        
                    def plot_age():
                        age = dfs['Age']
                        age = list(age)
                        
                        a = []
                        b = []
                        c = []
                        d = []
                        e = []
                        for i in age:
                            if i <= 20:
                                a.append(i)
                            elif 20 < i <= 30:
                                b.append(i)
                            elif 30 < i <= 40:
                                c.append(i)
                            elif 40 < i <= 50:
                                d.append(i)
                            elif 50 < i <= 60:
                                e.append(i)
                        a_fr = len(a)
                        b_fr = len(b)
                        c_fr = len(c)
                        d_fr = len(d)
                        e_fr = len(e)
                        age_d = {'0 to 20(yrs)':a_fr,'21 to 30(yrs)':b_fr,'31 to 40(yrs)':c_fr, '41 to 50(yrs)':d_fr,'51 to 60(yrs)':e_fr}
                        age_v = list(age_d.keys())
                        age_fr = list(age_d.values())
                        
                        fig = Figure(figsize = (5, 5), dpi = 100)
                        a = fig.add_subplot(111) 
                        a.pie(age_fr, labels = age_v,autopct = '%1.i%%')
                        a.set_title('Age Distribiution for Districts')
                        
                        canvas = FigureCanvasTkAgg(fig, popup)
                        canvas.show()
                        canvas.get_tk_widget().grid(row = 10, column = 1, columnspan = 6, pady = 10, padx = 10) 
                        toolbar = NavigationToolbar2TkAgg(canvas, nav_frame)
                        toolbar.update()
                        canvas._tkcanvas.grid(row = 5, column = 1, columnspan = 6, pady = 10, padx = 10)
            
            
                    
                    def plot_sch_type():
                        s = {}
                        for i in private_public:
                            key = len(i)
                            if key not in s:
                                s[key] = []
                            s[key].append(i)   
                        #print(s)
                    
                        s = defaultdict(int)
                        for i in private_public:
                            s[i] += 1 
                            
                        private_public_v = list(s.keys())
                        private_public_fr = list(s.values())
                        private_public_v[0] = 'Private'
                        private_public_v[1] = 'Public'
                        private_public_v[2] = 'Missing Data'
                       
                        fig = Figure(figsize = (5, 5), dpi = 100)
                        a = fig.add_subplot(111) 
                        a.pie(private_public_fr, labels = private_public_v, autopct = '%1.i%%')
                        a.set_title('Private/Public School Distribiution for Districts')
                        
                        canvas = FigureCanvasTkAgg(fig, popup)
                        canvas.show()
                        canvas.get_tk_widget().grid(row = 10, column = 1, columnspan = 6, pady = 10, padx = 10) 
                        toolbar = NavigationToolbar2TkAgg(canvas, nav_frame)
                        toolbar.update()
                        canvas._tkcanvas.grid(row = 5, column = 1, columnspan = 6, pady = 10, padx = 10)
                    
                    
                    def plot_sett_typ():
                        sett = {}
                        for i in settlement_type:
                            key = i[0]
                            if key not in sett:
                                sett[key] = []
                            sett[key].append(i)   
                        #print(sett)
             
                        sett = defaultdict(int)
                        for i in settlement_type:
                            sett[i] += 1 
                        #print(sett)
             
                        sett_typ_v = list(sett.keys())
                        sett_typ_fr = list(sett.values())
                        
                        fig = Figure(figsize = (5, 5), dpi = 100)
                        a = fig.add_subplot(111) 
                        a.pie(sett_typ_fr, labels = sett_typ_v, autopct = '%1.i%%')
                        a.set_title('Human Settlement Type Distribiution for Districts')
                        
                        canvas = FigureCanvasTkAgg(fig, popup)
                        canvas.show()
                        canvas.get_tk_widget().grid(row = 10, column = 1, columnspan = 6, pady = 10, padx = 10) 
                        toolbar = NavigationToolbar2TkAgg(canvas, nav_frame)
                        toolbar.update()
                        canvas._tkcanvas.grid(row = 5, column = 1, columnspan = 6, pady = 10, padx = 10)
                    
                    
                    
                    def plot_training_college ():
                        t = {}
                        for i in training_college:
                            key = len(i)
                            if key not in t:
                                t[key] = []
                            t[key].append(i)   
                        #print(t)
                   
                        t = defaultdict(int)
                        for i in training_college:
                            t[i] += 1 
                        #print(t)
                    
                        training_college_v = list(t.keys())
                        training_college_fr = list(t.values())
                        training_college_v[0] = 'No'
                        training_college_v[1] = 'Yes'
                        training_college_v[2] = 'Missing Data'
                        
                        fig = Figure(figsize = (5, 5), dpi = 100)
                        a = fig.add_subplot(111) 
                        a.pie(training_college_fr, labels = training_college_v, autopct = '%1.i%%')
                        a.set_title('Training College Attendance Distribiution for Districts')
                        
                        canvas = FigureCanvasTkAgg(fig, popup)
                        canvas.show()
                        canvas.get_tk_widget().grid(row = 10, column = 1, columnspan = 6, pady = 10, padx = 10) 
                        toolbar = NavigationToolbar2TkAgg(canvas, nav_frame)
                        toolbar.update()
                        canvas._tkcanvas.grid(row = 5, column = 1, columnspan = 6, pady = 10, padx = 10)
            
            
            
                B1 = tk.Button(popup, text = "Close", command = popup.destroy, fg = "white", bg = "red")
                B1.grid(row = 0)
                
                gender_b = ttk.Button(popup, text = "GENDER", command = plot_gender)
                gender_b.grid(row = 1, column = 1, pady = 10, padx = 10)
                
                age_b = ttk.Button(popup, text = "AGE", command = plot_age)
                age_b.grid(row = 1, column = 0, pady = 10, padx = 10)
                
                training_b = ttk.Button(popup, text = "TRAINING COLLEGE", command = plot_training_college)
                training_b.grid(row = 1, column = 2, pady = 10, padx = 10)
                
                sch_b = ttk.Button(popup, text = "SCHOOL TYPE", command = plot_sch_type)
                sch_b.grid(row = 1, column = 3, pady = 10, padx = 10)
                
                settlement_b = ttk.Button(popup, text = "SETTLEMENT TYPE", command = plot_sett_typ)
                settlement_b.grid(row = 1, column = 4, pady = 10, padx = 10)
           
                popup.geometry("900x650")
                popup.mainloop()
            
                
                
            concat_data = tk.Button(self, text = "Analyze All at Once", command = concat_sheets, bg = "orange", fg = "white")
            concat_data.grid(row = 9, column = 10, sticky='w', pady = 5, padx = 10)
               
            deleteButton = tk.Button(self, text = "Clear Buttons", command = cleargrid, bg = "red", fg = "white")
            deleteButton.grid(row = 10, column = 10, sticky='w', pady = 5, padx = 10)
            
       
                
                
    
               
            
        
            
        select_l = ttk.Label(self, text = "UPLOAD FILE", font = MEDIUM_FONT)
        select_l.grid(row = 3, column = 0, columnspan = 7, sticky='w', padx = 10)
        
        select_l = tk.Label(self, text = "Please click on the 'Select file' button to upload an excel file...", fg = "blue")
        select_l.grid(row = 4, column = 0, columnspan = 7, sticky='w', padx = 10)
                
        home = tk.Button(self, text = "Home", command = lambda: controller.show_frame(Home), bg = "green", fg = "white")
        home.grid(row = 2, column = 0, sticky='w', pady = 15, padx = 10)
        
        en_survey = tk.Button(self, text = "Before & After Surveys", command = lambda: controller.show_frame(end_survey), bg = "turquoise", fg = "white")
        en_survey.grid(row = 2, column = 1, pady = 15, padx = 10)
       
        select_b = ttk.Button(self, text = "Select File", command = select_file)
        select_b.grid(row = 5, column = 0, sticky='w', pady = 10, padx = 10)
        
        
        
       
       
        
        
            
        
class end_survey(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text = "END OF SURVEY ANALYSIS", font = LARGE_FONT)
        label.grid(row = 0, columnspan = 6, pady = 10, padx = 10)

        
        home = tk.Button(self, text = "Home", command = lambda: controller.show_frame(Home), bg = "green", fg = "white")
        home.grid(row = 1, column = 0, pady = 10, padx = 10)
        
        menu = tk.Button(self, text = "Main Menu", command = lambda: controller.show_frame(MainMenu), bg = "green", fg = "white")
        menu.grid(row = 1, column = 1, pady = 10, padx = 10)
        
        



class PageTwo(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        
        home = tk.Button(self, text = "Home", command = lambda: controller.show_frame(Home), bg = "green", fg = "white")
        home.grid(row = 1, column = 0, pady = 10, padx = 10)
        
        button = tk.Button(self, text = "Main Menu", command = lambda: controller.show_frame(MainMenu), bg = "green", fg = "white")
        button.grid(row = 8, column = 3, pady = 10, padx = 10)
        
        button1 = ttk.Button(self, text = "Analyze Data", command = lambda: controller.show_frame(PageTwo))
        button1.grid(row = 8, column = 3, pady = 10, padx = 10)
        
        en_survey = tk.Button(self, text = "Before & After Surveys", command = lambda: controller.show_frame(end_survey), bg = "green", fg = "white")
        en_survey.grid()
        
        
app = pen_app()
app.geometry("900x650")
ani = animation.FuncAnimation(f, animate, interval = 1000)
app.mainloop()
        