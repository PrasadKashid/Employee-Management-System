# ------------------------------------Employee Management System----------------------------------

import matplotlib.pyplot as plt
from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from pymongo import *
import pandas as pd
import requests

# ---------------------------------fetching Location of user------------------------------

try:
    wa = "https://ipinfo.io/"
    res = requests.get(wa)
    data = res.json()
    city = data["city"]
except Exception as e:
    print("Issue", e)

# ----------------------------fetching Weather---------------------------

try:
    a1 = "https://api.openweathermap.org/data/2.5/weather?"
    a2 = "q=" + city
    a3 = "&appid=" + "6375451b26374fe7f225f659fa0074c8"
    a4 = "&units=" + "metric"
    wa = a1+a2+a3+a4
    res = requests.get(wa)
    data = res.json()
    temp = data["main"]["temp"]
except Exception as e:
    print("issue", e)

# ---------------------------------All Functions------------------------------


def awOpen():
    mw.withdraw()
    aw.deiconify()


def awBack():
    aw.withdraw()
    mw.deiconify()


def vwOpen():
    mw.withdraw()
    vw.deiconify()
    vw_st_data.delete(1.0, END)
    con = None
    try:
        con = MongoClient("mongodb://localhost:27017")
        db = con["emspro"]
        coll = db["emp"]
        data = coll.find()
        info = ""
        for d in data:
            info = info + "ID = " + \
                str(d["_id"]) + "  Name = " + str(d["name"]) + \
                "  Salary = " + str(d["salary"]) + "\n"
        vw_st_data.insert(INSERT, info)
    except Exception as e:
        showerror("Error", e)
    finally:
        if con is not None:
            con.close()


def vwBack():
    vw.withdraw()
    mw.deiconify()


def uwOpen():
    mw.withdraw()
    uw.deiconify()


def uwBack():
    uw.withdraw()
    mw.deiconify()


def dwOpen():
    mw.withdraw()
    dw.deiconify()


def dwBack():
    dw.withdraw()
    mw.deiconify()


def addUser():
    con = None
    try:
        con = MongoClient("mongodb://localhost:27017")
        db = con["emspro"]
        coll = db["emp"]
        id = int(aw_ent_id.get())
        name = (aw_ent_name.get())
        salary = float(aw_ent_salary.get())
        if (id > 0):
            if ((name.isalpha()) and (len(name) >= 2)):
                count = coll.count_documents({"_id": id})
                if (salary >= 8000):
                    if count == 1:
                        showinfo(id, "already exists")
                    else:
                        info = {"_id": id, "name": name, "salary": salary}
                        coll.insert_one(info)
                        showinfo("success", "record created")
                else:
                    showerror("Error", "salary should be more than 8K")
            else:
                showerror(
                    "Error", "Enter Valid Name,Name should of more than 2 Aplhas")
        else:
            showerror("Error", "Enter postive ID")
    except Exception as e:
        showerror("Error", e)
    finally:
        if con is not None:
            con.close()
        aw_ent_id.delete(0, END)
        aw_ent_name.delete(0, END)
        aw_ent_salary.delete(0, END)
        aw_ent_id.focus()


def deleteUser():
    con = None
    try:
        con = MongoClient("mongodb://localhost:27017")
        db = con["emspro"]
        coll = db["emp"]
        id = int(dw_ent_id.get())
        count = coll.count_documents({"_id": id})
        if count == 1:
            coll.delete_one({"_id": id})
            showinfo(id, "Deleted")
        elif count == 0:
            showinfo(id, "Does Not Exists")
        else:
            showinfo(id, "Already Exists")
    except Exception as e:
        showerror("Error", e)
    finally:
        if con is not None:
            con.close()
        dw_ent_id.delete(0, END)
        dw_ent_id.focus()


def updateUser():
    con = None
    try:
        con = MongoClient("mongodb://localhost:27017")
        db = con["emspro"]
        coll = db["emp"]
        id = int(uw_ent_id.get())
        count = coll.count_documents({"_id": id})
        if count == 1:
            info = {}
            name = (uw_ent_name.get())
            salary = float(uw_ent_salary.get())
            if ((name.isalpha()) and (len(name) >= 2)):
                if (salary > 8000):
                    info["name"] = name
                    info["salary"] = salary
                    ndata = {"$set": info}
                    coll.update_one({"_id": id}, ndata)
                    showinfo(id, "updated")
                else:
                    showerror("Error", "salary should be more than 8K")
            else:
                showerror(
                    "Error", "Enter Valid Name,Name should of more than 2 Aplhas")
        else:
            showinfo("id", "does not exists")
    except Exception as e:
        showerror("Error", e)
    finally:
        if con is not None:
            con.close()
        uw_ent_id.delete(0, END)
        uw_ent_name.delete(0, END)
        uw_ent_salary.delete(0, END)
        uw_ent_id.focus()


def openChart():
    con = None
    try:
        con = MongoClient("mongodb://localhost:27017")
        db = con["emspro"]
        coll = db["emp"]
        graph = list(coll.find().sort("salary", -1).limit(5))
        df_mango = pd.DataFrame(graph)
        df_mango.plot(kind="bar", x="name", y="salary", color="DarkMagenta")
        plt.xlabel("Employee")
        plt.ylabel("Salary")
        plt.show()
    except Exception as e:
        showerror("Error", e)
    finally:
        if con is not None:
            con.close()

# ---------------------------------Main Window Code----------------------------------------


mw = Tk()
mw.title("Employee Mgmt System")
mw.geometry("500x500+50+50")
mw.configure(bg="pale green")
f = ("Arial", 20, "bold")


btn_add = Button(mw, width=15, text="Add", font=f,
                 bd=3, bg="grey", command=awOpen)
btn_add.pack(pady=10)
btn_view = Button(mw, width=15, text="View", font=f,
                  bd=3, bg="grey", command=vwOpen)
btn_view.pack(pady=10)
btn_update = Button(mw, width=15, text="Update", font=f,
                    bd=3, bg="grey", command=uwOpen)
btn_update.pack(pady=10)
btn_delete = Button(mw, width=15, text="Delete", font=f,
                    bd=3, bg="grey", command=dwOpen)
btn_delete.pack(pady=10)
btn_charts = Button(mw, width=15, text="Charts", font=f,
                    bd=3, bg="grey", command=openChart)
btn_charts.pack(pady=10)
lab_ct = Label(mw, text="Location:" + city +
               "    Temp: " + str(temp), font=f, bg="grey")
lab_ct.pack(pady=10)

# ----------------------------------Add employee Window-----------------------------------

aw = Toplevel(mw)
aw.title("Add Emp")
aw.geometry("500x500+50+50")
aw.configure(bg="powder blue")
f = ("Arial", 20, "bold")

aw_lab_id = Label(aw, text="Enter ID: ", font=f)
aw_ent_id = Entry(aw, font=f)
aw_lab_id.pack(pady=10)
aw_ent_id.pack(pady=10)
aw_lab_name = Label(aw, text="Enter Name: ", font=f)
aw_ent_name = Entry(aw, font=f)
aw_lab_name.pack(pady=10)
aw_ent_name.pack(pady=10)
aw_lab_salary = Label(aw, text="Enter Salary:", font=f)
aw_ent_salary = Entry(aw, font=f)
aw_lab_salary.pack(pady=10)
aw_ent_salary.pack(pady=10)

aw_save_btn = Button(aw, text="Save", font=f, command=addUser)
aw_save_btn.pack(pady=10)
aw_back_btn = Button(aw, text="Back", font=f, command=awBack)
aw_back_btn.pack(pady=10)
aw.withdraw()

# ------------------------------------View Employee Window----------------------------------

vw = Toplevel(mw)
vw.title("View Emp")
vw.geometry("500x500+50+50")
vw.configure(bg="Wheat")
f = ("Arial", 15, "bold")

vw_st_data = ScrolledText(vw, width=38, height=10, font=f)
vw_back_btn = Button(vw, text="Back", font=f, command=vwBack)
vw_st_data.pack(pady=10)
vw_back_btn.pack(pady=10)
vw.withdraw()

# ----------------------------------Update Employee Window---------------------------------

uw = Toplevel(mw)
uw.title("Update Emp")
uw.geometry("500x500+50+50")
uw.configure(bg="papaya whip")
f = ("Arial", 20, "bold")

uw_lab_id = Label(uw, text="Enter ID: ", font=f)
uw_ent_id = Entry(uw, font=f)
uw_lab_id.pack(pady=10)
uw_ent_id.pack(pady=10)
uw_lab_name = Label(uw, text="Enter Name: ", font=f)
uw_ent_name = Entry(uw, font=f)
uw_lab_name.pack(pady=10)
uw_ent_name.pack(pady=10)
uw_lab_salary = Label(uw, text="Enter Salary:", font=f)
uw_ent_salary = Entry(uw, font=f)
uw_lab_salary.pack(pady=10)
uw_ent_salary.pack(pady=10)

uw_save_btn = Button(uw, text="Save", font=f, command=updateUser)
uw_save_btn.pack(pady=10)
uw_back_btn = Button(uw, text="Back", font=f, command=uwBack)
uw_back_btn.pack(pady=10)
uw.withdraw()

# ----------------------------------Delete Employee Window---------------------------------

dw = Toplevel(mw)
dw.title("Delete Emp")
dw.geometry("500x500+50+50")
dw.configure(bg="RoyalBlue1")
f = ("Arial", 20, "bold")

dw_lab_id = Label(dw, text="Enter ID: ", font=f)
dw_ent_id = Entry(dw, font=f)
dw_lab_id.pack(pady=10)
dw_ent_id.pack(pady=10)

dw_save_btn = Button(dw, text="Save", font=f, command=deleteUser)
dw_save_btn.pack(pady=10)
dw_back_btn = Button(dw, text="Back", font=f, command=dwBack)
dw_back_btn.pack(pady=10)

dw.withdraw()


def windowclose():
    if askyesno("Quit", "Do You Want to Exit"):
        mw.destroy()


mw.protocol("WM_DELETE_WINDOW", windowclose)

mw.mainloop()
