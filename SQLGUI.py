from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from sqlite3 import *
from functools import partial
from tkinter import messagebox
import yaysql
import os
import EzOs


    

class Main:

    def __init__(self):
        self.cancel_conn = False
        self.query_chosen = False
        self.query_data = []
        self.query_name = ""
        
        #----- WINDOW -----#
        self.win = Tk()
        self.win.title("Database Editor") 
        self.win.configure(background="white")
        self.win.geometry("350x282")
        
        #----- READING PAGE -----#
        self.lower_pages = ttk.Notebook(self.win)
        self.READ_PAGE = ttk.Frame(self.win,height=66, width=210)
        self.lower_pages.add(self.READ_PAGE, text="Read Data")
        self.info = Label(self.READ_PAGE, text="Selected Query Is Applied", relief=RIDGE,bg="white",width=25)
        self.info.pack()
        
        #----- EDITING PAGE -----#
        self.EDIT_PAGE = ttk.Frame(self.win,height=66,width=210)
        self.lower_pages.add(self.EDIT_PAGE,text="Add Data")
        self.lower_pages.place(x = 0, y = 165)
        #----- DELETION PAGE -----#
        self.DEL_PAGE = ttk.Frame(self.win)
        self.lower_pages.add(self.DEL_PAGE, text="Delete Data")
        
        #----- SETTINGS PAGE -----#
        self.pages = ttk.Notebook(self.win)
        self.SETTINGS_PAGE = ttk.Frame(self.win, height=140, width=160)
        self.pages.add(self.SETTINGS_PAGE, text="Database Settings")
        self.pages.place(x=0,y=0)
        
        #----- CREATE NEW DB WIDGET -----#
        self.create_new_db = Button(self.win, text="Create New DB",relief=GROOVE,bg="white",command=self.create_db)
        self.create_new_db.place(x = 220, y = 200)
        
        #----- WIDGETS (DELETION PAGE) -----#
        self.sub_del_table = LabelFrame(self.DEL_PAGE, text="Table Deletion",bg="white")
        self.sub_del_table.place(x = 0, y = 0)
        self.subsubtbl = Label(self.sub_del_table, text="Current Table:",relief=RIDGE,bg="#7fa5e2")
        self.subsubtbl.pack(fill=X)
        self.current_table_DEL = Label(self.sub_del_table, text="No Table Selected",relief=SUNKEN,bg="lightblue")
        self.current_table_DEL.pack(fill=X)
        self.confirm_DEL = Button(self.sub_del_table, text="Delete", command=self.delete_table,width=5, relief=GROOVE, bg="white")
        self.confirm_DEL.pack(side=LEFT)
        self.confirm_CLEAR = Button(self.sub_del_table, text="Clear", command=self.clear_table, relief=GROOVE,bg="white")
        self.confirm_CLEAR.pack(side=RIGHT)
        """ DELETE BY QUERY """
        self.sub_del_byQ = LabelFrame(self.DEL_PAGE, text="Delete Data",bg="white")
        self.sub_del_byQ.place(x=92,y=0) 
        self.subsub_Q = Label(self.sub_del_byQ, text="Current Query:",bg="#7fa5e2",relief=RIDGE)
        self.subsub_Q.pack(fill=X)
        self.sub_cur_Q = Label(self.sub_del_byQ, text="No Query Selected",bg="lightblue",relief=SUNKEN)
        self.sub_cur_Q.pack(fill=X)
        self.sub_del_byQ_confirm = Button(self.sub_del_byQ, text="Perform Deletion",relief=GROOVE, command=self.perform_deletion,bg="white")
        self.sub_del_byQ_confirm.pack(fill=X)
        
        #----- WIDGETS (EDITING PAGE) -----#
        self.head_sub_col = LabelFrame(self.EDIT_PAGE, text="Add To Table", bg="white")
        self.head_sub_col.pack(side=LEFT) 
        self.sub = Label(self.head_sub_col, text="Current Table:",relief=RIDGE,bg="#7fa5e2")
        self.sub.pack(fill=X)
        self.current_table_EDIT = Label(self.head_sub_col, text="No Table Selected",relief=SUNKEN,bg="lightblue")
        self.current_table_EDIT.pack(fill=X)
        self.add_new = Button(self.head_sub_col, text = "Add Data",relief=GROOVE, command=self.add_to_DB,bg="white")
        self.add_new.pack(fill=X)
        """ TABLE CREATION """
        self.head_sub_tbl = LabelFrame(self.EDIT_PAGE, text="Table Creation", bg="white")
        self.head_sub_tbl.pack(side=LEFT) 
        self.sub_table = Label(self.head_sub_tbl,text="Create New Table",relief=RIDGE, bg="#7fa5e2")
        self.sub_table.pack(fill=X)
        self.new_table = Entry(self.head_sub_tbl, bg="lightblue",width=18)
        self.new_table.pack(fill=X)
        self.create_new_table = Button(self.head_sub_tbl, text="Create Table", relief=GROOVE, command=self.add_table,bg="white")
        self.create_new_table.pack(fill=X)
        
        #----- WIDGETS (SETTINGS PAGE) -----#
        self.title = Label(self.SETTINGS_PAGE, text="Current Database", bg="lightblue", width=22, font=("bold","11"))
        self.title.place(x = 0, y = 5)
        self.curDB = "No DB Selected"
        self.curDB_display = Label(self.SETTINGS_PAGE, text=self.curDB, relief=RIDGE)
        self.curDB_display.place(x = 112, y = 60)
        self.changeDB = Button(self.SETTINGS_PAGE, text="Select Database", command = self.db_select,bg="lightgrey",relief=GROOVE)
        self.changeDB.place(x = 108, y = 30)
        self.connect = Button(self.SETTINGS_PAGE, text="Renew Connection",width=15, command = self.full_refresh, relief=GROOVE)
        self.connect.place(x=0, y = 76)
        self.status = "No Connection"
        self.conn_stat = LabelFrame(self.SETTINGS_PAGE,text="Connection Status", padx=5, pady=5, bg="lightblue")
        self.conn_stat.place(x=0,y=28)
        self.stat_dis = Label(self.conn_stat,text=self.status)
        self.stat_dis.pack()
        
        #----- DATA PAGE -----#
        self.DATA_PAGE = ttk.Frame(self.win, height=140,width=196)
        self.pages.add(self.DATA_PAGE, text="Tables/Columns")

        #----- WIDGETS (DATA PAGE) -----#
        self.table_title = LabelFrame(self.DATA_PAGE, text="Details")
        self.table_title.place(x = 0, y = 0)
        self.table_subtitle = Label(self.table_title, text="Table List")
        self.table_subtitle.pack() 
        self.table_list = ttk.Combobox(self.table_title)
        self.table_list.pack()
        self.table_list.bind("<<ComboboxSelected>>", self.update_columns)
        self.column_subtitle = Label(self.table_title, text="Column List")
        self.column_subtitle.pack()
        self.column_list = ttk.Combobox(self.table_title)
        self.column_list.pack()
        self.column_list.bind("<<ComboboxSelected>>", self.update_data_type)
        self.data_type = Label(self.table_title, text="No Column Selected")
        self.data_type.pack()
        
        #----- WIDGETS (BUILD QUERY) -----#
        self.query_section = LabelFrame(self.win, text="Queries Section")
        self.query_section.place(x = 200, y = 0)
        self.build_query = Button(self.query_section, text = "Build New Query", command=self.query_creation, relief=GROOVE, bg="white")
        self.query_name = Entry(self.query_section, bg="lightblue")
        self.query_name_dis = Label(self.query_section, relief=RIDGE, text="Enter Query Name:")
        self.query_name_dis.pack(fill=X) 
        self.query_name.pack(fill=X)
        self.build_query.pack(fill=X)

        self.current_query_dis = Label(self.query_section, text="Current Query:",relief=RIDGE)
        self.current_query_dis.pack(fill=X)
        self.current_query = Label(self.query_section, text="No Query Selected",relief=SUNKEN,bg="lightblue")
        self.current_query.pack(fill=X)
        self.choose_query_button = Button(self.query_section, text="Select Query",relief=GROOVE, bg="white", command=self.select_query)
        self.choose_query_button.pack(fill=X)
        self.dechoose_query_button = Button(self.query_section, text="Deselect Query",relief=GROOVE,bg="white",command=self.de_select_query)
        self.dechoose_query_button.pack(fill=X)
        self.runquery = Button (self.query_section, text="Run Query As Command", relief=GROOVE, bg="white", command = self.run_query)
        self.runquery.pack(fill=X)
        
        #----- WIDGETS (READ SECTION) -----#
        self.read_section = LabelFrame(self.READ_PAGE, text="Read Column Data", bg="white")
        self.read_section.pack(side=LEFT)
        self.read_column = Label(self.read_section, text="Current Column:",bg="#7fa5e2")
        self.read_column.pack(fill=X)
        self.current_col = Label(self.read_section, text="No Column Selected",relief = SUNKEN, bg="lightblue")
        self.current_col.pack(fill=X)
        self.display_col = Button(self.read_section, text="Display Data", bg="white", relief=GROOVE, command=self.display_column_data)
        self.display_col.pack(fill=X)

        self.read_section2 = LabelFrame(self.READ_PAGE, text="Read Table Data", bg="white")
        self.read_section2.pack(side=LEFT)
        self.read_table = Label(self.read_section2, text="Current Table:", bg="#7fa5e2")
        self.read_table.pack(fill=X)
        self.current_table = Label(self.read_section2, text="No Table Selected", relief = SUNKEN, bg="lightblue")
        self.current_table.pack(fill=X)
        self.display_table = Button(self.read_section2, text="Display Data", bg="white", relief = GROOVE, command = self.display_table_data)
        self.display_table.pack(fill=X)
        
        #----- Keyboard Shortcuts -----#
        self.win.bind("<Control-s>", self.display_table_data)
        self.win.bind("<Escape>", self.close) 
    
        
        #----- WIDGETS (MAKE NEW DB SECTION) -----#


        
        self.win.mainloop()

    #----- Destroy By Event -----#
    def close(self, event):
        if messagebox.askyesno("Close","Are You Sure You Want To Exit?"):
            self.win.destroy()
        else:
            pass

    #----- DELETE BY QUERY OPEN -----#
    def perform_deletion(self):
        if messagebox.askyesno("Confirm","Perform Deletion"):
            self.editDB.cursor.execute(query_data) 
            self.de_select_query()
            

    #----- SELECT A QUERY OPEN -----#
    def de_select_query(self):
        self.query_chosen = False
        self.current_query.configure(text = "No Query Selected")
         
    def select_query(self):
        file = askopenfilename(title="Select Query")
        self.current_query.configure(text=file.split("/")[-1])
        self.sub_cur_Q.configure(text=file.split("/")[-1]) 
        self.query_chosen = True
        filename = open(file,"r")
        self.query_data = filename.read()
    def run_query(self):
        self.editDB.cursor.execute(self.query_data)
        
        
    #----- QUERY CREATION OPEN -----#

    def save_query(self, v):
        to_write = self.Qbox.get("1.0", END)
        if not os.path.exists("Queries"):
            os.mkdir("Queries")
        os.chdir("Queries") 
        query_file = open(self.query_name.get()+".txt", "w") 
        query_file.write(to_write)
        query_file.close() 
        v.destroy()
        EzOs.go_back()
        
    
    def query_creation(self):
        view = Toplevel(self.win)
        view.title("Query Creation")
        self.editDB.curtable = self.table_list.get()
        self.Qbox = Text(view)
        self.Qbox.pack()
        confirm = Button(view, text="Save Query", command = partial(self.save_query, view))
        confirm.pack() 
    #----- QUERY CREATION -----#
        
    #----- TABLE DELETION OPEN -----#
    def delete_table(self):
        self.editDB.curtable = self.table_list.get()
        if messagebox.askyesno("Confirm",f"Table: [{self.table_list.get()}] will be deleted"):
            self.editDB.delete_curtable()
            self.editDB.save()
            self.full_refresh()

    def clear_table(self):
        self.editDB.curtable = self.table_list.get()
        if messagebox.askyesno("Confirm",f"Table: [{self.table_list.get()}] will be cleared"):
            self.editDB.clear_curtable()
            self.editDB.save()
            self.full_refresh() 
            
    #----- TABLE DELETION CLOSED -----#
    
    #----- TABLE CREATION OPEN -----#
    def add_column(self):
        self.widget_count += 1
        name = "entry"+str(self.widget_count)
        name2 = "combo"+str(self.widget_count)

         
        
        placement = LabelFrame(self.view, text="Column "+str(self.widget_count))
        placement.place(x = self.x, y = self.y)
        
        self.tbl_creation_entries[name] = Entry(placement,bg="lightblue")
        self.tbl_creation_combos[name2] = ttk.Combobox(placement, values=["INTEGER","TEXT","REAL","AUTOINCREMENT"])

        self.tbl_creation_entries[name].pack()
        self.tbl_creation_combos[name2].pack()
        placement.pack(fill=X)

    def finalize(self):
        ent_values = [self.tbl_creation_entries[key].get() for key in self.tbl_creation_entries.keys()]
        combo_values = [self.tbl_creation_combos[key].get() for key in self.tbl_creation_combos.keys()]

        cols = {}

        index = -1
        for colname in ent_values:
            index += 1
            if combo_values[index] == "INTEGER":
                data_type = int()
            elif combo_values[index] == "TEXT":
                data_type = str()
            elif combo_values[index] == "REAL":
                data_type = float()
            elif combo_values[index] ==  "AUTOINCREMENT":
                data_type = "autoinc"
                
            cols[colname] =  data_type
            
        self.editDB.curtable = self.new_table.get()
        self.editDB.createTable(cols)
        self.editDB.save()
        self.full_refresh() 
        self.view.destroy() 
        
            
       
    
    def add_table(self, event="filler"):
        self.widget_count = 0
        self.tbl_creation_entries = {}
        self.tbl_creation_combos = {} 
            
        self.x = 0
        self.y = 0
            
        self.view = Toplevel(self.win)
        self.view.title("Table Creation")
        

        confirm = Button(self.view, text="Create Table", relief=GROOVE,bg="lightblue", command=self.finalize)
        confirm.pack(fill=X)
        
        add = Button(self.view, text="Add Column",relief=GROOVE,command=self.add_column)
        add.pack(fill=X)
    #----- TABLE CREATION CLOSED -----#
        
    #ohoj

    #----- ADDING VALUES TO DB OPEN -----#
    def add_to_DB(self):
        def add_values(entries, win):
            values = []
            for key in entries.keys():
                try:
                    val = int(entries[key].get())
                except:
                    val = entries[key].get() 
                values.append(val)
            self.editDB.addValue(values)
            self.editDB.save()
            win.destroy() 
            
        self.editDB.curtable = self.table_list.get()
        columns = self.editDB.list_col()
        ind = 0
        view = Toplevel(self.win)
        view.title("Add Values")
        entry_ids = {}
        for col in columns:
            ind += 1
            entry_ids["entry"+str(ind)] = Entry(view, bg="lightblue")
        index = -1
        for key in entry_ids.keys():
            index += 1
            sample_label = Label(view, text= columns[index],bg="#a4bf89")
            sample_label.pack(fill=X)
            entry_ids[key].pack(fill=X)
        confirm = Button(view, text="Confirm",command= partial(add_values, entry_ids, view),relief=GROOVE)
        confirm.pack(fill=X)
        
    #----- ADDING VALUES TO DB CLOSED -----#
            

    def create_db(self):
        file = asksaveasfilename(defaultextension = ".db", title="Create New DB")
        throwaway_var = connect(file)

    def save_data(self, textbox, win):
        file = asksaveasfilename(defaultextension = ".txt", title="Save DB Data")
        edit = open(file, "w+")
        edit = open(file, "a")
        edit.write(textbox.get("1.0",END))
        edit.close()
        win.destroy()
        
    def display_table_data(self, event="filler"):
        view = Toplevel(self.win)
        view.title(self.table_list.get())
        self.editDB.curtable = self.table_list.get()
        
        if self.query_chosen:
            self.editDB.cursor.execute(self.query_data)
            data = self.editDB.cursor.fetchall() 
        else:
            data = self.editDB.readTable()
        col_names = [i[0] for i in self.editDB.list_col()]
        col_names.insert(0,"") 
        box = Text(view)
        test = ttk.Treeview(view, columns=col_names[0:len(col_names)-1])
        test.pack()
        test["show"] = "headings"
        index = -1
        for col in col_names:
            index += 1
            test.heading("#"+str(index),text=col)

        for data in self.editDB.readTable():
            test.insert("",0,values=data[0:len(data)]) 
        
        data = self.editDB.readTable()
        
        for i in data:
            box.insert(END, str(i)+"\n")
        
        save_button = ttk.Button(view, text="Save Data", command = partial(self.save_data,box,view))
        save_button.pack() 

        
    def display_column_data(self):
        view = Toplevel(self.win)
        view.title("Column Data")
        box = Text(view)
        title = Label(view, text=self.column_list.get(),font=("bold",12))
        title.pack() 
        data = self.editDB.get_column(self.column_list.get())
        for i in data:
            box.insert(END, str(i[0])+"\n")
        save_button = ttk.Button(view, text="Save Data", command = partial(self.save_data,box,view))
        save_button.place(x=0,y=0)
        box.pack()
        
    def update_data_type(self, filler):
        columns = self.editDB.list_col()
        self.current_col.configure(text=self.column_list.get()) 
        for i in columns:
            if i[0] == self.column_list.get():
                self.data_type.configure(text = i[1])
                          
                
    def update_columns(self, filler):
        table_name = self.table_list.get()
        self.editDB.curtable = table_name
        columns = self.editDB.list_col()
        self.column_list.configure(values = [ i[0] for i in self.editDB.list_col()])
        self.current_table.configure(text = self.table_list.get())
        self.current_table_EDIT.configure(text = self.table_list.get())
        self.current_table_DEL.configure(text = self.table_list.get()) 

        
    def update_status(self, update):
        status = update
        self.stat_dis.configure(text = status) 
    def full_refresh(self):
        self.connect_to_db()
        try:
            self.renew_tables()
        except:
            pass
    def db_select(self):
        self.DB = askopenfilename(title="Open Database")
        if self.DB.split(".")[-1] != "db":
            self.cancel_conn = True
            self.update_status("Invalid File Type")
        else:
            self.cancel_conn = False
            self.update_status("No Connection")
        self.curDB = self.DB.split("/")[-1]
        self.curDB_display.configure(text = self.curDB)
    def connect_to_db(self):
        try:
            self.conn = connect(self.DB)
            self.cursor = self.conn.cursor()
            self.editDB = yaysql.DB(self.cursor,self.conn)
            if not self.cancel_conn:
                self.update_status("Connected")
            else:
                self.update_status("Invalid File Type")
        except AttributeError:
            self.update_status("No DB Selected")
             
        
    def renew_tables(self):
        try:
            self.table_list.configure(values = [ i[0] for i in self.editDB.list_tables()])
        except AttributeError:
            pass


x = Main() 
