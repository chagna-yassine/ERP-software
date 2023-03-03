import os
import random
import sqlite3
import customtkinter
import datetime
import num2words
from PIL import Image
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import filedialog
from tkinter import scrolledtext as tkst


# databases
# client daatabase 
client_db = sqlite3.connect('client.db')
client_cur = client_db.cursor()
client_cur.execute("CREATE TABLE if not exists h_client(client, voiture, modele, matricule, telephone, km)")
client_db.commit()
client_db.close()

# stock database
stock_db = sqlite3.connect('tree_crm.db')
stock_cur = stock_db.cursor()
stock_cur.execute("CREATE TABLE if not exists Stock_piece(piece, referance, quantite, prix, vente)")
stock_cur.execute("CREATE TABLE if not exists rep_stock(piece, referance, quantite, prix)")
stock_db.commit()
stock_db.close()

# facture payer database
facture_db = sqlite3.connect('facture.db')
facture_cur = facture_db.cursor()
facture_cur.execute("CREATE TABLE if not exists Factures_payer (n_facture, client, matricule, date, responsable, total, path)")
facture_db.commit()
facture_db.close()

# facture non payer database
factureNp_db = sqlite3.connect('n_facture.db')
factureNp_cur = factureNp_db.cursor()
factureNp_cur.execute("CREATE TABLE if not exists non_Factures (n_facture, client, matricule, date, responsable, total, avance, path)")
factureNp_db.commit()
factureNp_db.close()

# bon database
bon_db = sqlite3.connect('b_commande.db')
bon_cur = bon_db.cursor()
bon_cur.execute("CREATE TABLE if not exists bon (n_bon, client, date, total, path)")
bon_db.commit()
bon_db.close()

# bon non payer
bonNp_db = sqlite3.connect('n_bon.db')
bonNp_cur = bonNp_db.cursor()
bonNp_cur.execute("CREATE TABLE if not exists non_commande (n_bon, client, date, total, avance, path)")
bonNp_db.commit()
bonNp_db.close()

# devie
devie_db = sqlite3.connect('facture.db')
devie_cur = devie_db.cursor()
devie_cur.execute("CREATE TABLE if not exists devie (n_devie, client, matricule, total, path)")
devie_db.commit()
devie_db.close()


window = customtkinter.CTk()

# configure window
window.title("ERP Software")
window.geometry(f"{1150}x{580}")

# configure grid layout (4x4)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure((2, 3), weight=0)
window.grid_rowconfigure((0, 1, 2), weight=1)

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


def liste():
    
    stock_db = sqlite3.connect('tree_crm.db')
    stock_cur = stock_db.cursor()
    stock_cur.execute('SELECT * FROM Stock_piece')
    records = stock_cur.fetchall()
    stock_list = []
    for record in records:
        stock_list.append(record[1])
    
    stock_db.commit()
    stock_db.close()

    return stock_list


def search(event):
     
    global global_frame
    value = event.widget.get() 

    if value == '':
       
       global_frame.referance_entry['values'] = liste()
    
    else:
       
        data = []
        for item in liste():
            if value.lower() in item.lower():
                data.append(item)
        global_frame.referance_entry['values'] = data



def client_frame():
    global global_frame
    menu.destroy_menu(global_frame)
    stock.destroy_stock(global_frame)
    facture.destroy_facture(global_frame)
    bill_window.destroy_bill(global_frame)
    bon_window.destroy_bill(global_frame)
    ouvrire_facture.destroy_oFacture(global_frame)
    ouvrire_bon.destroy_obon(global_frame)
    devie_entry.destroy_enry_D(global_frame)
    devie_window.destroy_devie(global_frame)
    global_frame = client()


def stock_frame():
    global global_frame
    menu.destroy_menu(global_frame)
    client.destroy_client(global_frame)
    facture.destroy_facture(global_frame)
    bill_window.destroy_bill(global_frame)
    bon_window.destroy_bill(global_frame)
    ouvrire_facture.destroy_oFacture(global_frame)
    ouvrire_bon.destroy_obon(global_frame)
    devie_entry.destroy_enry_D(global_frame)
    devie_window.destroy_devie(global_frame)
    global_frame = stock()


def facture_frame():
    global global_frame
    menu.destroy_menu(global_frame)
    stock.destroy_stock(global_frame)
    client.destroy_client(global_frame)
    bill_window.destroy_bill(global_frame)
    bon_window.destroy_bill(global_frame)
    ouvrire_facture.destroy_oFacture(global_frame)
    ouvrire_bon.destroy_obon(global_frame)
    devie_entry.destroy_enry_D(global_frame)
    devie_window.destroy_devie(global_frame)
    global_frame = facture()


def menu_frame():
    global global_frame
    client.destroy_client(global_frame)
    stock.destroy_stock(global_frame)
    facture.destroy_facture(global_frame)
    bill_window.destroy_bill(global_frame)
    bon_window.destroy_bill(global_frame)
    ouvrire_facture.destroy_oFacture(global_frame)
    ouvrire_bon.destroy_obon(global_frame)
    devie_entry.destroy_enry_D(global_frame)
    devie_window.destroy_devie(global_frame)
    global_frame = menu()


def bill_number():

    x1 = random.randint(10,10000)
    x2 = random.randint(10,10000)
    x3 = random.randint(10,10000)

    return x1 + x2 + x3


# historique client
def client_database(client_tree):

    for record in client_tree.get_children():
        client_tree.delete(record)

    client_db = sqlite3.connect('client.db')
    client_cur = client_db.cursor()
    client_cur.execute("SELECT rowid, * FROM h_client")

    records = client_cur.fetchall()
    count = 0

    for record in records:

        if count % 2 == 0:
            client_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]), tags=('evenrow',))
        else:
            client_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]), tags=('oddrow',))

        count += 1

    client_db.commit()
    client_db.close()


def vider_client():

    global_frame.H_id_entry.delete(0, END)
    global_frame.H_client_entry.delete(0, END)
    global_frame.H_voiture_entry.delete(0, END)
    global_frame.H_modele_entry.delete(0, END)
    global_frame.H_matricule_entry.delete(0, END)
    global_frame.H_k_entry.delete(0, END)
    global_frame.H_t_entry.delete(0, END)


def select_client(e):

    vider_client()

    selected = global_frame.client_tree.focus()
    values = global_frame.client_tree.item(selected, 'values')

    global_frame.H_id_entry.insert(0, values[0])
    global_frame.H_client_entry.insert(0, values[1])
    global_frame.H_voiture_entry.insert(0, values[2])
    global_frame.H_modele_entry.insert(0, values[3])
    global_frame.H_matricule_entry.insert(0, values[4])
    global_frame.H_k_entry.insert(0, values[6])
    global_frame.H_t_entry.insert(0, values[5])


def suprimer_c():

	s = global_frame.client_tree.selection()[0]
	global_frame.client_tree.delete(s)

	client_db = sqlite3.connect('client.db')
	client_cur = client_db.cursor()
	client_cur.execute("DELETE from h_client WHERE oid=" + global_frame.H_id_entry.get())
	client_db.commit()
	client_db.close()

	vider_client()

	messagebox.showinfo("Suprimer!", "client a été suprimer!")


def update_c():

	selected = global_frame.client_tree.focus()
	global_frame.client_tree.item(selected, text="", values=(global_frame.H_id_entry.get(), global_frame.H_client_entry.get(), global_frame.H_voiture_entry.get(), global_frame.H_modele_entry.get(), global_frame.H_matricule_entry.get(), global_frame.H_t_entry.get(), global_frame.H_k_entry.get()))

	client_db = sqlite3.connect('client.db')
	client_cur = client_db.cursor()
	client_cur.execute("""UPDATE h_client set
		client = :v1,
		voiture = :v2,
	  	modele = :v3,
	   	matricule = :v4,
		telephone = :v5,
		km = :v6
	    WHERE oid = :oid""",
		{
			'v1': global_frame.H_client_entry.get(),
			'v2': global_frame.H_voiture_entry.get(),
			'v3': global_frame.H_modele_entry.get(),
			'v4': global_frame.H_matricule_entry.get(),
			'v5': global_frame.H_t_entry.get(),
			'v6': global_frame.H_k_entry.get(),
			'oid': global_frame.H_id_entry.get()
		})

	client_db.commit()
	client_db.close()

	vider_client()


def add_Hclient():

    if (global_frame.H_client_entry.get() == '' or global_frame.H_voiture_entry.get() == '' or global_frame.H_modele_entry.get() == '' or global_frame.H_matricule_entry.get() == '' or global_frame.H_t_entry.get() == '' or global_frame.H_k_entry.get() == ''):

        messagebox.showinfo("Erreur", "Saisir les information")

    else:

        client_db = sqlite3.connect('client.db')
        client_cur = client_db.cursor()
        client_cur.execute("""INSERT INTO h_client VALUES (:client, :voiture, :modele, :matricule, :telephone, :km)""",
            {
                'client': global_frame.H_client_entry.get(),
                'voiture': global_frame.H_voiture_entry.get(),
                'modele': global_frame.H_modele_entry.get(),
                'matricule': global_frame.H_matricule_entry.get(),
                'telephone': global_frame.H_t_entry.get(),
                'km':global_frame.H_k_entry.get()
            })

        client_db.commit()
        client_db.close()

        vider_client()
        client_database(global_frame.client_tree)


def search_client():

	lookup_record = global_frame.entry.get()

	for record in global_frame.client_tree.get_children():
		global_frame.client_tree.delete(record)

	client_db = sqlite3.connect('client.db')
	client_cur = client_db.cursor()
	client_cur.execute("SELECT rowid, * FROM h_client WHERE client like ? or voiture like ? or modele like ? or matricule like ? or telephone like ? ", (lookup_record, lookup_record, lookup_record, lookup_record, lookup_record, ))
	records = client_cur.fetchall()
	count = 0

	for record in records:
		if count % 2 == 0:
			global_frame.client_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]), tags=('evenrow',))
		else:
			global_frame.client_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]), tags=('oddrow',))

		count += 1

	client_db.commit()
	client_db.close()
        

def H_facture():

    global global_frame, x1, x2, x3, x4, x5, x6
    x1 = global_frame.H_client_entry.get()
    x2 = global_frame.H_voiture_entry.get()
    x3 = global_frame.H_modele_entry.get()
    x4 = global_frame.H_matricule_entry.get()
    x5 = global_frame.H_k_entry.get()
    x6 = global_frame.H_t_entry.get()

    menu.destroy_menu(global_frame)
    client.destroy_client(global_frame)
    stock.destroy_stock(global_frame)
    facture.destroy_facture(global_frame)
    bon_window.destroy_bill(global_frame)
    ouvrire_facture.destroy_oFacture(global_frame)
    ouvrire_bon.destroy_obon(global_frame)
    devie_entry.destroy_enry_D(global_frame)
    devie_window.destroy_devie(global_frame)

    global_frame = bill_window()

    global x, d
    date = (datetime.datetime.now())
    d = date.strftime("%x")
    x = bill_number()

    global liste3, liste4
    liste3 = []
    liste4 = []
    liste3.clear()
    liste4.clear()
    l2.clear()

    global_frame.bill.insert('insert',"\n\n Numero de facture : b{}\t\t\t\t\t\t SAFI le:{}\t\t\t\t\t\n".format(x, d))
    global_frame.bill.insert('insert',"\n\n Client  : {}\t\t\t\t\t Telephone : {}\t\t\t\t\t\n".format(x1, x6))
    global_frame.bill.insert('insert',"\n\n voiture :  {}\t\t\t model : {}\t\t matricule : {}\n".format(x2, x3, x4))
    global_frame.bill.insert('insert',"________________________________________________________________________")
    global_frame.bill.insert('insert',"\n\n disignation \t\t referance \t\t  QTE\t\t P U\t\t P T\n".format())
    global_frame.bill.insert('insert',"________________________________________________________________________")

    global a1, a2, a3, a4, a6
    a1, a2, a3, a4, a6 = x1, x2, x3, x4, x6
    x1, x2, x3, x4, x6 = '', '', '', '', ''
    global_frame.referance_entry.bind('<KeyRelease>', search)


# nouveu client facture
def add_client():

    global global_frame, v1, v2, v3, v4, v5, v6
    v1 = global_frame.nouveau_client_entry.get()
    v2 = global_frame.voiture_entry.get()
    v3 = global_frame.modele_entry.get()
    v4 = global_frame.matricule_entry.get()
    v5 = global_frame.km_entry.get()
    v6 = global_frame.tp_entry.get()

    if (v1 == '' or v2 == '' or v3 == '' or v4 == '' or v5 == '' or v6 == ''):

        messagebox.showinfo("Erreur", "Saisir les information")

    else:

        client_db = sqlite3.connect('client.db')
        client_cur = client_db.cursor()

        client_cur.execute("""INSERT INTO h_client VALUES (:client, :voiture, :modele, :matricule, :telephone, :km)""",
            {
                'client': v1,
                'voiture': v2,
                'modele': v3,
                'matricule': v4,
                'telephone': v5,
                'km':v6
            })

        client_db.commit()
        client_db.close()

        Nc_facture()


def Nc_facture():

    global global_frame, v1, v2, v3, v4, v5, v6
    menu.destroy_menu(global_frame)
    client.destroy_client(global_frame)
    stock.destroy_stock(global_frame)
    facture.destroy_facture(global_frame)
    bon_window.destroy_bill(global_frame)
    ouvrire_facture.destroy_oFacture(global_frame)
    ouvrire_bon.destroy_obon(global_frame)
    devie_entry.destroy_enry_D(global_frame)
    devie_window.destroy_devie(global_frame)

    global_frame = bill_window()

    global x, d
    date = (datetime.datetime.now())
    d = date.strftime("%x")
    x = bill_number()

    global liste3, liste4
    liste3 = []
    liste4 = []
    liste3.clear()
    liste4.clear()
    l2.clear()

    global_frame.bill.insert('insert',"\n\n Numero de facture : b{}\t\t\t\t\t\t SAFI le:{}\t\t\t\t\t\n".format(x, d))
    global_frame.bill.insert('insert',"\n\n Client  : {}\t\t\t\t\t Telephone : {}\t\t\t\t\t\n".format(v1, v6))
    global_frame.bill.insert('insert',"\n\n voiture :  {}\t\t\t model : {}\t\t matricule : {}\n".format(v2, v3, v4))
    global_frame.bill.insert('insert',"________________________________________________________________________")
    global_frame.bill.insert('insert',"\n\n disignation \t\t referance \t\t  QTE\t\t P U\t\t P T\n".format())
    global_frame.bill.insert('insert',"________________________________________________________________________")

    global a1, a2, a3, a4, a6
    a1, a2, a3, a4, a6 = v1, v2, v3, v4, v6 
    v1, v2, v3, v4, v6 = '', '', '', '', ''
    global_frame.referance_entry.bind('<KeyRelease>', search)


def add_produit():

    if (global_frame.dg_entry.get()=='' or global_frame.referance_entry.get()=='' or global_frame.prix_entry.get()=='' or global_frame.quantite_entry.get()==''):

        messagebox.showinfo("Erreur", "Saisir les information")

    else:

        stock_db = sqlite3.connect('tree_crm.db')
        stock_cur = stock_db.cursor()

        try:

            stock_cur.execute("SELECT rowid, * FROM Stock_piece WHERE referance like ?", [global_frame.referance_entry.get()])
            rec = stock_cur.fetchall()

            if rec == '':

                messagebox.showinfo("Erreur", "Quntité en stock insuffisante")

            if int(global_frame.quantite_entry.get()) <= int(rec[0][3]) :

                liste3.append(global_frame.referance_entry.get())
                liste4.append(int(global_frame.quantite_entry.get()))

                calcule()

                Pt =float(global_frame.quantite_entry.get()) * float(global_frame.prix_entry.get())
                global_frame.bill.insert('insert',"\n\n {} \t\t {} \t\t  {}\t\t {}\t\t {}\n".format(global_frame.dg_entry.get(), global_frame.referance_entry.get(), global_frame.prix_entry.get(), global_frame.quantite_entry.get(), Pt))

                global_frame.dg_entry.delete(0, END)
                global_frame.referance_entry.set('')
                global_frame.prix_entry.delete(0, END)
                global_frame.quantite_entry.delete(0, END)

            else:

                messagebox.showinfo("Erreur", "Quntité en stock insuffisante")

        except:

            messagebox.showinfo("Erreur", "Article introuvable")

        stock_db.commit()
        stock_db.close()
       

def calcule():

    p = float(global_frame.prix_entry.get())
    q = float(global_frame.quantite_entry.get())*p
    l2.append(q)

    return l2


def prix_total():

    main_douevre = simpledialog.askfloat("Input", "Entrer la main d'ouvre", parent=window)

    global total1
    total1 = sum(l2) + main_douevre

    global_frame.bill.insert('insert',"\n\n Main d'oevre \t\t\t\t\t\t\t\t {}\n".format(main_douevre))
    global_frame.bill.insert('insert',"________________________________________________________________________")
    global_frame.bill.insert('insert',"\n\n\t\t\t\t\t\t Totale\t\t {}\n".format(total1))
    global_frame.bill.insert('insert',"\n\n\t\t\t\t\t\t _______________________")
    global_frame.bill.insert('insert',"\n\n\n\n  Arétée la présente facture a la somme de : {} Dirhams".format(num2words( total1, lang='fr')))
    global_frame.bill.configure(state="disabled")

    l2.clear()


def F_Initialiser():

    global_frame.bill.delete("1.0", END)

    global_frame.bill.insert('insert',"\n\n Numero de facture : b{}\t\t\t\t\t\t SAFI le:{}\t\t\t\t\t\n".format(x, d))
    global_frame.bill.insert('insert',"\n\n Client  : {}\t\t\t\t\t Telephone : {}\t\t\t\t\t\n".format(a1, a6))
    global_frame.bill.insert('insert',"\n\n voiture :  {}\t\t\t model : {}\t\t matricule : {}\n".format(a2, a3, a4))
    global_frame.bill.insert('insert',"________________________________________________________________________")
    global_frame.bill.insert('insert',"\n\n disignation \t\t referance \t\t  QTE\t\t P U\t\t P T\n".format())
    global_frame.bill.insert('insert',"________________________________________________________________________")

    liste3.clear()
    liste4.clear()
    l2.clear()


def F_etat():

    global  save1
    save1 = Toplevel(window)

    save1.title("Facture")
    save1.geometry("")

    global radio_var1
    radio_var1 = IntVar()

    responsable_label = customtkinter.CTkLabel(save1, text="Nom du reponsable")
    responsable_label.pack(pady=10, padx=10)

    global responsable
    responsable = customtkinter.CTkEntry(save1, height=25, border_width=2, corner_radius=10)
    responsable.pack(pady=10, padx=10)

    radiobutton_1 = customtkinter.CTkRadioButton(master=save1, text="Facture payer", variable= radio_var1, value=1)
    radiobutton_2 = customtkinter.CTkRadioButton(master=save1, text="facture non payer", variable= radio_var1, value=2)

    radiobutton_1.pack(padx=20, pady=10)
    radiobutton_2.pack(padx=20, pady=10)

    avance_label = customtkinter.CTkLabel(save1, text="Avance (en cas non payer)")
    avance_label.pack(pady=10, padx=10)

    global avance1
    avance1 = customtkinter.CTkEntry(save1, height=25, border_width=2, corner_radius=10)
    avance1.pack(pady=10, padx=10)

    s_button = customtkinter.CTkButton(save1, text="sauvgarder", fg_color='gray', width=115, command=save_as_file)
    s_button.pack(pady=10, padx=10)


def requet():

    stock_db = sqlite3.connect('tree_crm.db')
    stock_cur = stock_db.cursor()

    for i in range(len(liste3)):

        stock_cur.execute("SELECT rowid, * FROM Stock_piece WHERE referance like ?", [liste3[i]])
        records = stock_cur.fetchall()

        x = int(records[0][3]) - int(liste4[i])

        stock_cur.execute("""UPDATE Stock_piece set
            quantite = :v3
            WHERE oid = :oid""",
            {
            'v3': x,
            'oid': records[0][0]
            })

    stock_db.commit()
    stock_db.close()


def save_as_file():

    global Av1, a1, a2
    Av1 = avance1.get()
    if Av1 == '':
        Av1 = 0

    global R1
    R1 = responsable.get()

    save1.destroy()

    if radio_var1.get() == 1:

        requet()

        facture_db = sqlite3.connect('facture.db')
        facture_cur = facture_db.cursor()
        facture_cur.execute("""INSERT INTO Factures_payer VALUES (:n_facture, :client, :matricule, :date, :responsable, :total, :path)""",
            {

                'n_facture': ("b{}".format(x)),
                'client': a1,
                'matricule': a4,
                'date':d,
                'responsable':R1,
                'total':total1,
                'path': ('./facture/b{}.txt'.format(x))
            })

        facture_db.commit()
        facture_db.close()
        text_file = ('./facture/b{}.txt'.format(x))

        if text_file:

            # Save the file
            text_file = open(text_file, 'w')
            text_file.write(global_frame.bill.get(1.0, END))
            # Close the file
            text_file.close()

            messagebox.showinfo("Sauvgarder", "Facture sauvgarder")

    else:

        requet()
        factureNp_db = sqlite3.connect('n_facture.db')
        factureNp_cur = factureNp_db.cursor()
        factureNp_cur.execute("""INSERT INTO non_Factures VALUES (:n_facture, :client, :matricule, :date, :responsable, :total, :avance, :path)""",
            {

                'n_facture': ("b{}".format(x)),
                'client': a1,
                'matricule': a4,
                'date':d,
                'responsable':R1,
                'total':total1,
                'avance':Av1,
                'path': ('./facture/b{}.txt'.format(x))
            })

        factureNp_db.commit()
        factureNp_db.close()

        text_file = ('./facture/b{}.txt'.format(x))
        if text_file:

            # Save the file
            text_file = open(text_file, 'w')
            text_file.write(global_frame.bill.get(1.0, END))
            # Close the file
            text_file.close()

            messagebox.showinfo("Sauvgarder", "Facture sauvgarder")


# stock
def query_database(stock_tree):
    
    for record in stock_tree.get_children():
        stock_tree.delete(record)

    stock_db = sqlite3.connect('tree_crm.db')
    stock_cur = stock_db.cursor()
    stock_cur.execute("SELECT rowid, * FROM Stock_piece")

    records = stock_cur.fetchall()
    count = 0

    for record in records:

        if int(record[3]) == 0 or int(record[3]) <= 2:
            stock_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5]), tags=('r_stock',))

        try:
            if count % 2 == 0:
                stock_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5]), tags=('evenrow',))
        except:
            pass

        try:
            if count % 2 != 0:
                stock_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5]), tags=('oddrow',))
        except:
            pass

        count += 1

    stock_db.commit()
    stock_db.close()


def vider_stock():

    global_frame.id_entry.delete(0, END)
    global_frame.piece_entry.delete(0, END)
    global_frame.referance_entry.delete(0, END)
    global_frame.quantite_entry.delete(0, END)
    global_frame.prix_entry.delete(0, END)
    global_frame.prix_vente_entry.delete(0, END)


def add_stock():

    if global_frame.piece_entry.get()=='' or global_frame.referance_entry.get()=='' or global_frame.quantite_entry.get()=='' or global_frame.prix_entry.get()=='' or global_frame.prix_vente_entry.get()=='':

        messagebox.showinfo("Erreur", "Saisir les information")

    else:

        stock_db = sqlite3.connect('tree_crm.db')
        stock_cur = stock_db.cursor()
        stock_cur.execute("""INSERT INTO Stock_piece VALUES (:piece, :referance, :quantite, :prix, :vente)""",
            {
                'piece': global_frame.piece_entry.get(),
                'referance': global_frame.referance_entry.get(),
                'quantite': global_frame.quantite_entry.get(),
                'prix': global_frame.prix_entry.get(),
                'vente':global_frame.prix_vente_entry.get()
            })

        stock_db.commit()
        stock_db.close()

        vider_stock()

        global_frame.stock_tree.delete(*global_frame.stock_tree.get_children())

        query_database(global_frame.stock_tree)


def suprimer_stock():

	x = global_frame.stock_tree.selection()[0]
	global_frame.stock_tree.delete(x)

	stock_db = sqlite3.connect('tree_crm.db')
	stock_cur = stock_db.cursor()
	stock_cur.execute("DELETE from Stock_piece WHERE oid=" + global_frame.id_entry.get())
	stock_db.commit()
	stock_db.close()

	vider_stock()

	messagebox.showinfo("Suprimer!", "L'article a été suprimer!")
        

def select_stock(e):

    vider_stock()

    selected = global_frame.stock_tree.focus()

    values = global_frame.stock_tree.item(selected, 'values')

    global_frame.id_entry.insert(0,values[0])
    global_frame.piece_entry.insert(0, values[1])
    global_frame.referance_entry.insert(0, values[2])
    global_frame.quantite_entry.insert(0, values[3])
    global_frame.prix_entry.insert(0, values[4])
    global_frame.prix_vente_entry.insert(0, values[5])


def search_stock():

	lookup_record = global_frame.entry.get()

	for record in global_frame.stock_tree.get_children():
		global_frame.stock_tree.delete(record)

	stock_db = sqlite3.connect('tree_crm.db')
	stock_cur = stock_db.cursor()
	stock_cur.execute("SELECT rowid, * FROM Stock_piece WHERE piece like ? or referance like ? ", (lookup_record, lookup_record,))
	records = stock_cur.fetchall()
	count = 0

	for record in records:
		if count % 2 == 0:
			global_frame.stock_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5]), tags=('evenrow',))
		else:
			global_frame.stock_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5]), tags=('oddrow',))

		count += 1

	stock_db.commit()
	stock_db.close()
        

def update_stock():

	selected = global_frame.stock_tree.focus()

	global_frame.stock_tree.item(selected, text="", values=(global_frame.id_entry.get(), global_frame.piece_entry.get(), global_frame.referance_entry.get(), global_frame.quantite_entry.get(), global_frame.prix_entry.get(), global_frame.prix_vente_entry.get()))

	stock_db = sqlite3.connect('tree_crm.db')
	stock_cur = stock_db.cursor()
	stock_cur.execute("""UPDATE Stock_piece set
		piece = :v1,
		referance = :v2,
	  	quantite = :v3,
	   	prix = :v4,
        vente = :v5
	    WHERE oid = :oid""",
		{
			'v1': global_frame.piece_entry.get(),
			'v2': global_frame.referance_entry.get(),
			'v3': global_frame.quantite_entry.get(),
			'v4': global_frame.prix_entry.get(),
            'v5': global_frame.prix_vente_entry.get(),
			'oid': global_frame.id_entry.get()
		})

	stock_db.commit()
	stock_db.close()

	vider_stock()


def ajouter_bon():

    global y_client
    y_client = simpledialog.askstring("Input", "Entrer le nom complet du client", parent=window)

    global global_frame
    menu.destroy_menu(global_frame)
    client.destroy_client(global_frame)
    stock.destroy_stock(global_frame)
    facture.destroy_facture(global_frame)
    bill_window.destroy_bill(global_frame)
    ouvrire_facture.destroy_oFacture(global_frame)
    ouvrire_bon.destroy_obon(global_frame)
    devie_entry.destroy_enry_D(global_frame)
    devie_window.destroy_devie(global_frame)

    global_frame = bon_window()

    global x, d
    date = (datetime.datetime.now())
    d = date.strftime("%x")
    x = bill_number()

    global liste3, liste4
    liste3 = []
    liste4 = []
    liste3.clear()
    liste4.clear()
    l2.clear()

    global_frame.bill.insert('insert',"\n\n Numero de bon : k{}\t\t\t\t\t\t SAFI le:{}\t\t\t\t\t\n".format(x, d))
    global_frame.bill.insert('insert',"________________________________________________________________________")
    global_frame.bill.insert('insert',"\n\n disignation \t\t referance \t\t  QTE\t\t P U\t\t P T\n".format())
    global_frame.bill.insert('insert',"________________________________________________________________________")
    global_frame.referance_entry.bind('<KeyRelease>', search)


def bon_total():

    global total1
    total1 = sum(l2)

    global_frame.bill.insert('insert',"________________________________________________________________________")
    global_frame.bill.insert('insert',"\n\n\t\t\t\t\t\t Totale\t\t {}\n".format(total1))
    global_frame.bill.insert('insert',"\n\n\t\t\t\t\t\t _______________________")
    global_frame.bill.configure(state="disabled")

    l2.clear()


def B_etat():

    global  save1
    save1 = Toplevel(window)

    save1.title("Bon")
    save1.geometry("")

    global radio_var2
    radio_var2 = IntVar()

    radiobutton_1 = customtkinter.CTkRadioButton(master=save1, text="Bon payer", variable= radio_var2, value=1)
    radiobutton_2 = customtkinter.CTkRadioButton(master=save1, text="Bon non payer", variable= radio_var2, value=2)

    radiobutton_1.pack(padx=20, pady=10)
    radiobutton_2.pack(padx=20, pady=10)

    avance_label = customtkinter.CTkLabel(save1, text="Avance (en cas non payer)")
    avance_label.pack(pady=10, padx=10)

    global avance2
    avance2 = customtkinter.CTkEntry(save1, height=25, border_width=2, corner_radius=10)
    avance2.pack(pady=10, padx=10)

    s_button = customtkinter.CTkButton(save1, text="sauvgarder", fg_color='gray', width=115, command=save_bon)
    s_button.pack(pady=10, padx=10)


def save_bon():

    global Av1, a1, a2
    Av1 = avance2.get()
    if Av1 == '':
        Av1 = 0

    save1.destroy()

    if radio_var2.get() == 1:

        requet()

        bon_db = sqlite3.connect('b_commande.db')
        bon_cur = bon_db.cursor()
        bon_cur.execute("""INSERT INTO bon VALUES (:n_bon, :client, :date, :total, :path)""",
            {

                'n_bon': ("k{}".format(x)),
                'client': y_client,
                'date': d,
                'total':total1,
                'path': ('./bon/k{}.txt'.format(x))
            })

        bon_db.commit()
        bon_db.close()

        text_file = ('./bon/k{}.txt'.format(x))

        if text_file:

            text_file = open(text_file, 'w')
            text_file.write(global_frame.bill.get(1.0, END))

            text_file.close()

            messagebox.showinfo("Sauvgarder", "Bon sauvgarder")

    else:

        requet()

        bon_db = sqlite3.connect('n_bon.db')
        bon_cur = bon_db.cursor()
        bon_cur.execute("""INSERT INTO non_commande VALUES (:n_bon, :client, :date, :total, :avance, :path)""",
            {

                'n_bon': ("k{}".format(x)),
                'client': y_client,
                'date': d,
                'total':total1,
                'avance': Av1,
                'path': ('./bon/k{}.txt'.format(x))
            })

        bon_db.commit()
        bon_db.close()

        text_file = ('./bon/k{}.txt'.format(x))

        if text_file:

            text_file = open(text_file, 'w')
            text_file.write(global_frame.bill.get(1.0, END))
            text_file.close()

            messagebox.showinfo("Sauvgarder", "Bon sauvgarder")


def B_Initialiser():

    global_frame.bill.delete("1.0", END)

    global_frame.bill.insert('insert',"\n\n Numero de bon : k{}\t\t\t\t\t\t SAFI le:{}\t\t\t\t\t\n".format(x, d))
    global_frame.bill.insert('insert',"________________________________________________________________________")
    global_frame.bill.insert('insert',"\n\n disignation \t\t referance \t\t  QTE\t\t P U\t\t P T\n".format())
    global_frame.bill.insert('insert',"________________________________________________________________________")

    liste3.clear()
    liste4.clear()
    l2.clear()


# facture payer
def facture_database(facture_tree):

	for record in facture_tree.get_children():
		facture_tree.delete(record)

	facture_db = sqlite3.connect('facture.db')
	facture_cur = facture_db.cursor()
	facture_cur.execute("SELECT rowid, * FROM Factures_payer")
        
	records = facture_cur.fetchall()
	count_f = 0
        
	for record in records:

		if count_f % 2 == 0:
			facture_tree.insert(parent='', index='end', iid=count_f, text='', values=(record[0], record[1], record[2], record[3], record[4], record[6]), tags=('evenrow',))
		else:
			facture_tree.insert(parent='', index='end', iid=count_f, text='', values=(record[0], record[1], record[2], record[3], record[4], record[6]), tags=('oddrow',))

		count_f += 1

	facture_db.commit()
	facture_db.close()
        

def vider_facture():

    global_frame.id1_entry.delete(0, END)
    global_frame.nFacture_entry.delete(0, END)
    

def select_facture(e):

    vider_facture()

    selected = global_frame.facture_tree.focus()

    values = global_frame.facture_tree.item(selected, 'values')

    global_frame.id1_entry.insert(0,values[0])
    global_frame.nFacture_entry.insert(0, values[1])


def search_facture():

	lookup_record = global_frame.entry1.get()

	for record in global_frame.facture_tree.get_children():
		global_frame.facture_tree.delete(record)

	facture_db = sqlite3.connect('facture.db')
	facture_cur = facture_db.cursor()
	facture_cur.execute("SELECT rowid, * FROM Factures_payer WHERE n_facture like ? or client like ? or matricule like ? ", (lookup_record, lookup_record, lookup_record,))
	records = facture_cur.fetchall()
	count = 0

	for record in records:
		if count % 2 == 0:
			global_frame.facture_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[6]), tags=('evenrow',))
		else:
			global_frame.facture_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[6]), tags=('oddrow',))

		count += 1

	facture_db.commit()
	facture_db.close()


def F_path(factureID):

    facture_db = sqlite3.connect('facture.db')
    facture_cur = facture_db.cursor()
    facture_cur.execute("SELECT * from Factures_payer WHERE oid=" + factureID)
    records = facture_cur.fetchall()
    facture_db.commit()
    facture_db.close()

    return records[0][6]
        

def F_suprimer():

    x = global_frame.facture_tree.selection()[0]
    global_frame.facture_tree.delete(x)

    facture_db = sqlite3.connect('facture.db')
    
    try:
        facture_cur = facture_db.cursor()
        facture_cur.execute("DELETE from Factures_payer WHERE oid=" + global_frame.id1_entry.get())
        os.remove(F_path(global_frame.id1_entry.get()))
        
        messagebox.showinfo("Suprimer!", "Facture a été suprimer!")
    except:
        messagebox.showinfo("Erreur!", "Facture introuvable!")

    global_frame.nFacture_entry.delete(0, END)
    global_frame.id1_entry.delete(0, END)

    facture_db.commit()
    facture_db.close()


def ouvrire_f():

    global global_frame
    if global_frame.id1_entry.get() =='':
        messagebox.showinfo("Erreur!", "Selectioner une Facture!")
    else:
        global numero_facture
        numero_facture = global_frame.id1_entry.get()

        facture_db = sqlite3.connect('facture.db')
        facture_cur = facture_db.cursor()
        facture_cur.execute("SELECT * from Factures_payer WHERE oid=" + numero_facture)
        records = facture_cur.fetchall()
        facture_db.commit()
        facture_db.close()
        try:
            text_file = records[0][6]
            text_file = open(text_file, 'r')
            stuff = text_file.read()

            menu.destroy_menu(global_frame)
            client.destroy_client(global_frame)
            stock.destroy_stock(global_frame)
            facture.destroy_facture(global_frame)
            bill_window.destroy_bill(global_frame)
            bon_window.destroy_bill(global_frame)
            ouvrire_bon.destroy_obon(global_frame)
            devie_entry.destroy_enry_D(global_frame)
            devie_window.destroy_devie(global_frame)
                
            global_frame = ouvrire_facture()

            global_frame.responsable_entry.insert(0, records[0][4])
            global_frame.bill.insert(END, stuff)
            text_file.close()
        except:
            messagebox.showinfo("Erreur!", "Un Probleme s'est Produit lors D'ouverture du Fichier!")


def F_imprimer():

    file_to_print= filedialog.askopenfilename(
      initialdir="./facture", title="Select file", 
      filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
    try:
        os.startfile(file_to_print, 'print')
    except:
        messagebox.showinfo("Erreur!", "Un Probleme s'est Produit. Fichier Introuvable!") 


# facture non payer
def factureNp_database(factureNp_tree):

	for record in factureNp_tree.get_children():
		factureNp_tree.delete(record)

	factureNp_db = sqlite3.connect('n_facture.db')
	factureNp_cur = factureNp_db.cursor()
	factureNp_cur.execute("SELECT rowid, * FROM non_Factures")

	records = factureNp_cur.fetchall()
	n_count_f = 0

	for record in records:

		if n_count_f % 2 == 0:
			factureNp_tree.insert(parent='', index='end', iid=n_count_f, text='', values=(record[0], record[1], record[2], record[3], record[4], record[6], record[7]), tags=('evenrow',))
		else:
			factureNp_tree.insert(parent='', index='end', iid=n_count_f, text='', values=(record[0], record[1], record[2], record[3], record[4], record[6], record[7]), tags=('oddrow',))

		n_count_f += 1

	factureNp_db.commit()
	factureNp_db.close()
        

def vider_Nfacture():

    global_frame.id2_entry.delete(0, END)
    global_frame.nFactureNp_entry.delete(0, END)
    

def select_Nfacture(e):

    vider_Nfacture()

    selected = global_frame.factureNp_tree.focus()

    values = global_frame.factureNp_tree.item(selected, 'values')

    global_frame.id2_entry.insert(0,values[0])
    global_frame.nFactureNp_entry.insert(0, values[1])


def search_Nfacture():

	lookup_record = global_frame.entry2.get()

	for record in global_frame.factureNp_tree.get_children():
		global_frame.factureNp_tree.delete(record)

	factureNp_db = sqlite3.connect('n_facture.db')
	factureNp_cur = factureNp_db.cursor()
	factureNp_cur.execute("SELECT rowid, * FROM non_Factures WHERE n_facture like ? or client like ? or matricule like ? ", (lookup_record, lookup_record, lookup_record,))
	records = factureNp_cur.fetchall()
	count = 0

	for record in records:
		if count % 2 == 0:
			global_frame.factureNp_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[6], record[7]), tags=('evenrow',))
		else:
			global_frame.factureNp_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[6], record[7]), tags=('oddrow',))

		count += 1

	factureNp_db.commit()
	factureNp_db.close()
        

def NF_path(factureID):

    factureNp_db = sqlite3.connect('n_facture.db')
    factureNp_cur = factureNp_db.cursor()
    factureNp_cur.execute("SELECT * from non_Factures WHERE oid=" + factureID)
    records = factureNp_cur.fetchall()
    factureNp_db.commit()
    factureNp_db.close()

    return records[0][7]
        

def NF_suprimer():

    x = global_frame.factureNp_tree.selection()[0]
    global_frame.factureNp_tree.delete(x)

    factureNp_db = sqlite3.connect('n_facture.db')
    factureNp_cur = factureNp_db.cursor()
    factureNp_cur.execute("DELETE from non_Factures WHERE oid=" + global_frame.id2_entry.get())
    os.remove(NF_path(global_frame.id2_entry.get()))
    global_frame.nFactureNp_entry.delete(0, END)
    global_frame.id2_entry.delete(0, END)

    messagebox.showinfo("Suprimer!", "Facture a été suprimer!")

    factureNp_db.commit()
    factureNp_db.close()


def ouvrire_Nf():

    global global_frame
    if global_frame.id2_entry.get() =='':
        messagebox.showinfo("Erreur!", "Selectioner une Facture!")
    else:
        global numero_facture
        numero_facture = global_frame.id2_entry.get()

        factureNp_db = sqlite3.connect('n_facture.db')
        factureNp_cur = factureNp_db.cursor()
        factureNp_cur.execute("SELECT * from non_Factures WHERE oid=" + numero_facture)
        records = factureNp_cur.fetchall()
        factureNp_db.commit()
        factureNp_db.close()
        try:
            text_file = records[0][7]
            text_file = open(text_file, 'r')
            stuff = text_file.read()

            menu.destroy_menu(global_frame)
            client.destroy_client(global_frame)
            stock.destroy_stock(global_frame)
            facture.destroy_facture(global_frame)
            bill_window.destroy_bill(global_frame)
            bon_window.destroy_bill(global_frame)
            ouvrire_bon.destroy_obon(global_frame)
            devie_entry.destroy_enry_D(global_frame)
            devie_window.destroy_devie(global_frame)
                
            global_frame = ouvrire_facture()

            global_frame.responsable_entry.insert(0, records[0][4])
            global_frame.bill.insert(END, stuff)
            text_file.close()
        except:
            messagebox.showinfo("Erreur!", "Un Probleme s'est Produit lors D'ouverture du Fichier!")


def f_payment():

    factureNp_db = sqlite3.connect('n_facture.db')
    factureNp_cur = factureNp_db.cursor()
    factureNp_cur.execute("SELECT rowid, * FROM non_Factures WHERE n_facture like ?", [global_frame.nFactureNp_entry.get()])
    records = factureNp_cur.fetchall()

    avance = float(records[0][7])

    factureNp_cur.execute("""UPDATE non_Factures set
	   	avance = :v1
	    WHERE oid = :oid""",
		{
			'v1': float(global_frame.FacturePayement_entry.get()) + avance,
			'oid': global_frame.id2_entry.get()
		})

    factureNp_cur.execute("SELECT rowid, * FROM non_Factures WHERE n_facture like ?", [global_frame.nFactureNp_entry.get()])
    n_records = factureNp_cur.fetchall()

    if n_records[0][6] <= n_records[0][7]:

        facture_db = sqlite3.connect('facture.db')
        facture_cur = facture_db.cursor()
        facture_cur.execute("""INSERT INTO Factures_payer VALUES (:n_facture, :client, :matricule, :date, :responsable, :total, :path)""",
            {

                'n_facture': n_records[0][1],
                'client': n_records[0][2],
                'matricule': n_records[0][3],
                'date':n_records[0][4],
                'responsable':n_records[0][5],
                'total':n_records[0][6],
                'path': n_records[0][8]
            })

        facture_db.commit()
        facture_db.close()
        factureNp_cur.execute("DELETE from non_Factures WHERE oid=" + global_frame.id2_entry.get())

    factureNp_db.commit()
    factureNp_db.close()
    factureNp_database(global_frame.factureNp_tree)


# bon payer
def bon_database(bon_tree):

	for record in bon_tree.get_children():
		bon_tree.delete(record)

	bon_db = sqlite3.connect('b_commande.db')
	bon_cur = bon_db.cursor()
	bon_cur.execute("SELECT rowid, * FROM bon")

	records = bon_cur.fetchall()
	count_b = 0

	for record in records:

		if count_b % 2 == 0:
			bon_tree.insert(parent='', index='end', iid=count_b, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('evenrow',))
		else:
			bon_tree.insert(parent='', index='end', iid=count_b, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('oddrow',))

		count_b += 1

	bon_db.commit()
	bon_db.close()
        

def vider_bon():

    global_frame.id3_entry.delete(0, END)
    global_frame.nbon_entry.delete(0, END)
    

def select_bon(e):

    vider_bon()

    selected = global_frame.bon_tree.focus()

    values = global_frame.bon_tree.item(selected, 'values')

    global_frame.id3_entry.insert(0,values[0])
    global_frame.nbon_entry.insert(0, values[1])


def search_bon():

	lookup_record = global_frame.entry3.get()

	for record in global_frame.bon_tree.get_children():
		global_frame.bon_tree.delete(record)

	bon_db = sqlite3.connect('b_commande.db')
	bon_cur = bon_db.cursor()
	bon_cur.execute("SELECT rowid, * FROM bon WHERE n_bon like ? or client like ?", (lookup_record, lookup_record,))
	records = bon_cur.fetchall()
	count = 0

	for record in records:
		if count % 2 == 0:
			global_frame.bon_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('evenrow',))
		else:
			global_frame.bon_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('oddrow',))

		count += 1

	bon_db.commit()
	bon_db.close()
        

def ouvrire_b():

    global global_frame
    if global_frame.id3_entry.get() =='':
        messagebox.showinfo("Erreur!", "Selectioner un Bon!")
    else:
        global numero_facture
        numero_facture = global_frame.id3_entry.get()

        bon_db = sqlite3.connect('b_commande.db')
        bon_cur = bon_db.cursor()
        bon_cur.execute("SELECT * from bon WHERE oid=" + numero_facture)
        records = bon_cur.fetchall()
        bon_db.commit()
        bon_db.close()
        try:
            text_file = records[0][4]
            text_file = open(text_file, 'r')
            stuff = text_file.read()

            menu.destroy_menu(global_frame)
            client.destroy_client(global_frame)
            stock.destroy_stock(global_frame)
            facture.destroy_facture(global_frame)
            bill_window.destroy_bill(global_frame)
            bon_window.destroy_bill(global_frame)
            ouvrire_facture.destroy_oFacture(global_frame)
            devie_entry.destroy_enry_D(global_frame)
            devie_window.destroy_devie(global_frame)
                
            global_frame = ouvrire_bon()

            global_frame.client_entry.insert(0, records[0][1])
            global_frame.bill.insert(END, stuff)
            text_file.close()
        except:
            messagebox.showinfo("Erreur!", "Un Probleme s'est Produit lors D'ouverture du Fichier!")


def b_imprimer():

    file_to_print= filedialog.askopenfilename(
      initialdir="./bon", title="Select file", 
      filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
    try:
        os.startfile(file_to_print, 'print')
    except:
        messagebox.showinfo("Erreur!", "Un Probleme s'est Produit. Fichier Introuvable!") 


def b_path(factureID):

    factureNp_db = sqlite3.connect('b_commande.db')
    factureNp_cur = factureNp_db.cursor()
    factureNp_cur.execute("SELECT * from bon WHERE oid=" + factureID)
    records = factureNp_cur.fetchall()
    factureNp_db.commit()
    factureNp_db.close()

    return records[0][4]


def b_suprimer():

    x = global_frame.bon_tree.selection()[0]
    global_frame.bon_tree.delete(x)

    bon_db = sqlite3.connect('b_commande.db')
    bon_cur = bon_db.cursor()
    bon_cur.execute("DELETE from bon WHERE oid=" + global_frame.id3_entry.get())
    os.remove(b_path(global_frame.id3_entry.get()))
    bon_db.commit()
    bon_db.close()

    global_frame.nbon_entry.delete(0, END)
    global_frame.id3_entry.delete(0, END)

    messagebox.showinfo("Suprimer!", "Bon a été suprimer!")
 
        
# bon non payer
def bonNp_database(bonNp_tree):

	for record in bonNp_tree.get_children():
		bonNp_tree.delete(record)

	bonNp_db = sqlite3.connect('n_bon.db')
	bonNp_cur = bonNp_db.cursor()
	bonNp_cur.execute("SELECT rowid, * FROM non_commande")

	records = bonNp_cur.fetchall()
	count_nb = 0

	for record in records:

		if count_nb % 2 == 0:
			bonNp_tree.insert(parent='', index='end', iid=count_nb, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5]), tags=('evenrow',))
		else:
			bonNp_tree.insert(parent='', index='end', iid=count_nb, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5]), tags=('oddrow',))

		count_nb += 1

	bonNp_db.commit()
	bonNp_db.close()
        

def vider_Nbon():

    global_frame.id4_entry.delete(0, END)
    global_frame.nbonNp_entry.delete(0, END)
    

def select_Nbon(e):

    vider_Nbon()

    selected = global_frame.bonNp_tree.focus()

    values = global_frame.bonNp_tree.item(selected, 'values')

    global_frame.id4_entry.insert(0,values[0])
    global_frame.nbonNp_entry.insert(0, values[1])


def search_Nbon():

	lookup_record = global_frame.entry4.get()

	for record in global_frame.bonNp_tree.get_children():
		global_frame.bonNp_tree.delete(record)

	bonNp_db = sqlite3.connect('n_bon.db')
	bonNp_cur = bonNp_db.cursor()
	bonNp_cur.execute("SELECT rowid, * FROM non_commande WHERE n_bon like ? or client like ?", (lookup_record, lookup_record,))
	records = bonNp_cur.fetchall()
	count = 0

	for record in records:
		if count % 2 == 0:
			global_frame.bonNp_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[6], record[7]), tags=('evenrow',))
		else:
			global_frame.bonNp_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[6], record[7]), tags=('oddrow',))

		count += 1

	bonNp_db.commit()
	bonNp_db.close()
        

def Nb_path(factureID):

    bonNp_db = sqlite3.connect('n_bon.db')
    bonNp_cur = bonNp_db.cursor()
    bonNp_cur.execute("SELECT * from non_commande WHERE oid=" + factureID)
    records = bonNp_cur.fetchall()
    bonNp_db.commit()
    bonNp_db.close()

    return records[0][5]
        

def Nb_suprimer():

    x = global_frame.bonNp_tree.selection()[0]
    global_frame.bonNp_tree.delete(x)

    bonNp_db = sqlite3.connect('n_bon.db')
    bonNp_cur = bonNp_db.cursor()
    bonNp_cur.execute("DELETE from non_commande WHERE oid=" + global_frame.id4_entry.get())
    os.remove(Nb_path(global_frame.id4_entry.get()))
    global_frame.nbonNp_entry.delete(0, END)
    global_frame.id5_entry.delete(0, END)

    messagebox.showinfo("Suprimer!", "Bon a été suprimer!")

    bonNp_db.commit()
    bonNp_db.close()


def ouvrire_Nb():

    global global_frame
    if global_frame.id4_entry.get() =='':
        messagebox.showinfo("Erreur!", "Selectioner un Bon!")
    else:
        global numero_bon
        numero_bon = global_frame.id4_entry.get()

        bonNp_db = sqlite3.connect('n_bon.db')
        bonNp_cur = bonNp_db.cursor()
        bonNp_cur.execute("SELECT * from non_commande WHERE oid=" + numero_bon)
        records = bonNp_cur.fetchall()
        bonNp_db.commit()
        bonNp_db.close()
        try:
            text_file = records[0][5]
            text_file = open(text_file, 'r')
            stuff = text_file.read()

            menu.destroy_menu(global_frame)
            client.destroy_client(global_frame)
            stock.destroy_stock(global_frame)
            facture.destroy_facture(global_frame)
            bill_window.destroy_bill(global_frame)
            bon_window.destroy_bill(global_frame)
            ouvrire_facture.destroy_oFacture(global_frame)
            devie_entry.destroy_enry_D(global_frame)
            devie_window.destroy_devie(global_frame)
                
            global_frame = ouvrire_bon()

            global_frame.client_entry.insert(0, records[0][1])
            global_frame.bill.insert(END, stuff)
            text_file.close()
        except:
            messagebox.showinfo("Erreur!", "Un Probleme s'est Produit lors D'ouverture du Fichier!")


def b_payment():

    bonNp_db = sqlite3.connect('n_bon.db')
    bonNp_cur = bonNp_db.cursor()
    bonNp_cur.execute("SELECT rowid, * FROM non_commande WHERE n_bon like ?", [global_frame.nbonNp_entry.get()])
    records = bonNp_cur.fetchall()

    avance = float(records[0][5])

    bonNp_cur.execute("""UPDATE non_commande set
	   	avance = :v1
	    WHERE oid = :oid""",
		{
			'v1': float(global_frame.bonPayement_entry.get()) + avance,
			'oid': global_frame.id4_entry.get()
		})

    bonNp_cur.execute("SELECT rowid, * FROM non_commande WHERE n_bon like ?", [global_frame.nbonNp_entry.get()])
    n_records = bonNp_cur.fetchall()

    if n_records[0][4] <= n_records[0][5]:

        bon_db = sqlite3.connect('b_commande.db')
        bon_cur = bon_db.cursor()
        bon_cur.execute("""INSERT INTO bon VALUES (:n_bon, :client, :date, :total, :path)""",
            {

                'n_bon': n_records[0][1],
                'client': n_records[0][2],
                'date':n_records[0][3],
                'total':n_records[0][4],
                'path': n_records[0][6]
            })
        
        bon_db.commit()
        bon_db.close()
        bonNp_cur.execute("DELETE from non_commande WHERE oid=" + global_frame.id4_entry.get())

    bonNp_db.commit()
    bonNp_db.close()
    bonNp_database(global_frame.bonNp_tree)


# devie
def devie_database(devie_tree):

    for record in devie_tree.get_children():
        devie_tree.delete(record)

    devie_db = sqlite3.connect('facture.db')
    devie_cur = devie_db.cursor()
    devie_cur.execute("SELECT rowid, * FROM devie")

    records = devie_cur.fetchall()
    count_d = 0

    for record in records:

        if count_d % 2 == 0:
            devie_tree.insert(parent='', index='end', iid=count_d, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5]), tags=('evenrow',))
        else:
            devie_tree.insert(parent='', index='end', iid=count_d, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5]), tags=('oddrow',))

        count_d += 1

    devie_db.commit()
    devie_db.close()


def vider_devie():

    global_frame.id5_entry.delete(0, END)
    global_frame.ndevie_entry.delete(0, END)
    

def select_devie(e):

    vider_devie()

    selected = global_frame.devie_tree.focus()

    values = global_frame.devie_tree.item(selected, 'values')

    global_frame.id5_entry.insert(0,values[0])
    global_frame.ndevie_entry.insert(0, values[1])


def search_devie():

	lookup_record = global_frame.entry5.get()

	for record in global_frame.devie_tree.get_children():
		global_frame.devie_tree.delete(record)

	devie_db = sqlite3.connect('facture.db')
	devie_cur = devie_db.cursor()
	devie_cur.execute("SELECT rowid, * FROM devie WHERE n_devie like ? or client like ?", (lookup_record, lookup_record,))
	records = devie_cur.fetchall()
	count = 0

	for record in records:
		if count % 2 == 0:
			global_frame.devie_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5]), tags=('evenrow',))
		else:
			global_frame.devie_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5]), tags=('oddrow',))

		count += 1

	devie_db.commit()
	devie_db.close()


def client_entry():

    global global_frame
    menu.destroy_menu(global_frame)
    client.destroy_client(global_frame)
    stock.destroy_stock(global_frame)
    facture.destroy_facture(global_frame)
    bill_window.destroy_bill(global_frame)
    bon_window.destroy_bill(global_frame)
    ouvrire_facture.destroy_oFacture(global_frame)
    ouvrire_bon.destroy_obon(global_frame)
    devie_window,devie_window(global_frame)

    global_frame = devie_entry()


def add_devie():

    global global_frame, d1, d2, d3, d4, d5, d6
    d1 = global_frame.client_entry.get()
    d2 = global_frame.voiture_entry.get()
    d3 = global_frame.modele_entry.get()
    d4 = global_frame.matricule_entry.get()
    d5 = global_frame.km_entry.get()
    d6 = global_frame.tp_entry.get()

    menu.destroy_menu(global_frame)
    client.destroy_client(global_frame)
    stock.destroy_stock(global_frame)
    facture.destroy_facture(global_frame)
    bill_window.destroy_bill(global_frame)
    bon_window.destroy_bill(global_frame)
    ouvrire_facture.destroy_oFacture(global_frame)
    ouvrire_bon.destroy_obon(global_frame) 
    devie_entry.destroy_enry_D(global_frame)

    global_frame = devie_window()

    global x, d
    date = (datetime.datetime.now())
    d = date.strftime("%x")
    x = bill_number()

    global liste3, liste4
    liste3 = []
    liste4 = []
    liste3.clear()
    liste4.clear()
    l2.clear()

    global_frame.bill.insert('insert',"\n\n Numero de devis : b{}\t\t\t\t\t\t SAFI le:{}\t\t\t\t\t\n".format(x, d))
    global_frame.bill.insert('insert',"\n\n Client  : {}\t\t\t\t\t Telephone : {}\t\t\t\t\t\n".format(d1, d6))
    global_frame.bill.insert('insert',"\n\n voiture :  {}\t\t\t model : {}\t\t matricule : {}\n".format(d2, d3, d4))
    global_frame.bill.insert('insert',"________________________________________________________________________")
    global_frame.bill.insert('insert',"\n\n disignation \t\t referance \t\t  QTE\t\t P U\t\t P T\n".format())
    global_frame.bill.insert('insert',"________________________________________________________________________")
    global_frame.referance_entry.bind('<KeyRelease>', search)


def D_Initialiser():

    global_frame.bill.delete("1.0", END)

    global_frame.bill.insert('insert',"\n\n Numero de devis : b{}\t\t\t\t\t\t SAFI le:{}\t\t\t\t\t\n".format(x, d))
    global_frame.bill.insert('insert',"\n\n Client  : {}\t\t\t\t\t Telephone : {}\t\t\t\t\t\n".format(d1, d6))
    global_frame.bill.insert('insert',"\n\n voiture :  {}\t\t\t model : {}\t\t matricule : {}\n".format(d2, d3, d4))
    global_frame.bill.insert('insert',"________________________________________________________________________")
    global_frame.bill.insert('insert',"\n\n disignation \t\t referance \t\t  QTE\t\t P U\t\t P T\n".format())
    global_frame.bill.insert('insert',"________________________________________________________________________")

    liste3.clear()
    liste4.clear()
    l2.clear()


def devie_product():

    if (global_frame.dg_entry.get()=='' or global_frame.referance_entry.get()=='' or global_frame.quantite_entry.get()=='' or global_frame.prix_entry.get()==''):

        messagebox.showinfo("Erreur", "Saisir les information")

    else:   

        devi_calcule()

        Pt =float(global_frame.prix_entry.get()) * float(global_frame.quantite_entry.get())
        global_frame.bill.insert('insert',"\n\n {} \t\t {} \t\t  {}\t\t {}\t\t {}\n".format(global_frame.dg_entry.get(), global_frame.referance_entry.get(), global_frame.quantite_entry.get(), global_frame.prix_entry.get(), Pt))

        global_frame.dg_entry.delete(0, END)
        global_frame.referance_entry.set('')
        global_frame.quantite_entry.delete(0, END)
        global_frame.prix_entry.delete(0, END)


def devi_calcule():

    p = float(global_frame.quantite_entry.get())
    q = float(global_frame.prix_entry.get())*p
    l2.append(q)


def total_devie():

    main_douevre = simpledialog.askfloat("Input", "Entrer la main d'ouvre", parent=window)

    global totald
    totald = sum(l2) + main_douevre

    global_frame.bill.insert('insert',"\n\n Main d'oevre \t\t\t\t\t\t\t\t {}\n".format(main_douevre))
    global_frame.bill.insert('insert',"________________________________________________________________________")
    global_frame.bill.insert('insert',"\n\n\t\t\t\t\t\t Totale\t\t {}\n".format(totald))
    global_frame.bill.insert('insert',"\n\n\t\t\t\t\t\t _______________________")
    global_frame.bill.insert('insert',"\n\n\n\n  Arétée la présent devis a la somme de : {} Dirhams".format(num2words( totald, lang='fr')))
    
    global_frame.bill.configure(state="disabled")
    
    l2.clear()


def save_devie():

    devie_db = sqlite3.connect('facture.db')
    devie_cur = devie_db.cursor()
    devie_cur.execute("""INSERT INTO devie VALUES (:n_devie, :client, :matricule, :total, :path)""",
        {

            'n_devie': ("d{}".format(x)),
            'client': d1,
            'matricule': d4,
            'total':totald,
            'path': ('./devis/d{}.txt'.format(x))
        })

    devie_db.commit()
    devie_db.close()

    text_file = ('./devis/d{}.txt'.format(x))

    if text_file:

        text_file = open(text_file, 'w')
        text_file.write(global_frame.bill.get(1.0, END))
        text_file.close()


    messagebox.showinfo("Sauvgarder", "Devis sauvgarder")


def D_path(factureID):

    devie_db = sqlite3.connect('facture.db')
    devie_cur = devie_db.cursor()
    devie_cur.execute("SELECT * from devie WHERE oid=" + factureID)
    records = devie_cur.fetchall()
    devie_db.commit()
    devie_db.close()

    return records[0][4]


def D_suprimer():

    x = global_frame.devie_tree.selection()[0]
    global_frame.devie_tree.delete(x)

    devie_db = sqlite3.connect('facture.db')
    devie_cur = devie_db.cursor()
    devie_cur.execute("DELETE from devie WHERE oid=" + global_frame.id5_entry.get())
    os.remove(D_path(global_frame.id5_entry.get()))
    global_frame.ndevie_entry.delete(0, END)
    global_frame.id5_entry.delete(0, END)

    messagebox.showinfo("Suprimer!", "Devis a été suprimer!")

    devie_db.commit()
    devie_db.close()


def ouvrire_devie():

    global global_frame
    if global_frame.id5_entry.get() =='':
        messagebox.showinfo("Erreur!", "Selectioner un Devis!")
    else:
        global numero_facture
        numero_facture = global_frame.id5_entry.get()

        devie_db = sqlite3.connect('facture.db')
        devie_cur = devie_db.cursor()
        devie_cur.execute("SELECT * from devie WHERE oid=" + numero_facture)
        records = devie_cur.fetchall()
        devie_db.commit()
        devie_db.close()
        try:
            text_file = records[0][4]
            text_file = open(text_file, 'r')
            stuff = text_file.read()

            menu.destroy_menu(global_frame)
            client.destroy_client(global_frame)
            stock.destroy_stock(global_frame)
            facture.destroy_facture(global_frame)
            bill_window.destroy_bill(global_frame)
            bon_window.destroy_bill(global_frame)
            ouvrire_facture.destroy_oFacture(global_frame)
            devie_entry.destroy_enry_D(global_frame)
            devie_window.destroy_devie(global_frame)
                
            global_frame = ouvrire_bon()

            global_frame.client_entry.insert(0, records[0][1])
            global_frame.bill.insert(END, stuff)
            text_file.close()
        except:
            messagebox.showinfo("Erreur!", "Un Probleme s'est Produit lors D'ouverture du Fichier!")


class menu:
    def __init__(self) -> None:
        super().__init__()

        # load images with light and dark mode image
        self.text_image = PhotoImage(file='./imgs/ERP.png')
       
        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(window, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.menu_label = customtkinter.CTkLabel(self.sidebar_frame, text="MENU", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.menu_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Client", font=customtkinter.CTkFont(size=15, weight="bold"), command=client_frame)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Stock", font=customtkinter.CTkFont(size=15, weight="bold"), command=stock_frame)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Facture", font=customtkinter.CTkFont(size=15, weight="bold"), command=facture_frame)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Mode d'Apparance:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        
        # Recommendation enrty
        self.entry = customtkinter.CTkEntry(window, placeholder_text="Voiture")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=window, text="Recherche", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        self.home_frame_large_image_label = Label(window, image=self.text_image)
        self.home_frame_large_image_label.grid(row=0, column=1, columnspan=3, padx=20, pady=10)
        
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def destroy_menu(self):
        for widget in window.winfo_children():
            widget.destroy()


class sidebar:
    def __init__(self) -> None:
        super().__init__()

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(window, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.menu_label = customtkinter.CTkLabel(self.sidebar_frame, text="MENU", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.menu_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Client", font=customtkinter.CTkFont(size=15, weight="bold"), command=client_frame)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Stock", font=customtkinter.CTkFont(size=15, weight="bold"), command=stock_frame)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Facture", font=customtkinter.CTkFont(size=15, weight="bold"), command=facture_frame)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Menu", font=customtkinter.CTkFont(size=15, weight="bold"), command=menu_frame)
        self.sidebar_button_3.grid(row=6, column=0, padx=20, pady=10)    


class client:
    def __init__(self) -> None:
        super().__init__()

        # create sidebar frame with widgets
        self.sidebar = sidebar()

        # create tabview
        self.tabview = customtkinter.CTkTabview(window, width=250)
        self.tabview.grid(row=0, column=1, columnspan=3, rowspan=4, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Nouveau Client")
        self.tabview.add("Historique Client")
        self.tabview.tab("Nouveau Client").grid_columnconfigure(4, weight=1) 
        self.tabview.tab("Historique Client").grid_columnconfigure(4, weight=1)

        self.nouveau_client_label = customtkinter.CTkLabel(self.tabview.tab("Nouveau Client"), text="Client", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.nouveau_client_label.grid(row=0, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.nouveau_client_entry = customtkinter.CTkEntry(self.tabview.tab("Nouveau Client"), width=500, border_width=2, corner_radius=10)
        self.nouveau_client_entry.grid(row=0, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.voiture_label = customtkinter.CTkLabel(self.tabview.tab("Nouveau Client"), text="Voiture", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.voiture_label.grid(row=1, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.voiture_entry = customtkinter.CTkEntry(self.tabview.tab("Nouveau Client"), width=500, border_width=2, corner_radius=10)
        self.voiture_entry.grid(row=1, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.modele_label = customtkinter.CTkLabel(self.tabview.tab("Nouveau Client"), text="Modele", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.modele_label.grid(row=2, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.modele_entry = customtkinter.CTkEntry(self.tabview.tab("Nouveau Client"), width=500, border_width=2, corner_radius=10)
        self.modele_entry.grid(row=2, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.matricule_label = customtkinter.CTkLabel(self.tabview.tab("Nouveau Client"), text="Matricule", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.matricule_label.grid(row=3, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.matricule_entry = customtkinter.CTkEntry(self.tabview.tab("Nouveau Client"), width=500, border_width=2, corner_radius=10)
        self.matricule_entry.grid(row=3, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.km_label = customtkinter.CTkLabel(self.tabview.tab("Nouveau Client"), text="Kilometrage", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.km_label.grid(row=4, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.km_entry = customtkinter.CTkEntry(self.tabview.tab("Nouveau Client"), width=500, border_width=2, corner_radius=10)
        self.km_entry.grid(row=4, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.tp_label = customtkinter.CTkLabel(self.tabview.tab("Nouveau Client"), text="Telephone", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.tp_label.grid(row=5, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.tp_entry = customtkinter.CTkEntry(self.tabview.tab("Nouveau Client"), width=500, border_width=2, corner_radius=10)
        self.tp_entry.grid(row=5, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.save_client = customtkinter.CTkButton(self.tabview.tab("Nouveau Client"), text="Valider", font=customtkinter.CTkFont(size=15, weight="bold"), command=add_client)
        self.save_client.grid(row=6, column=0, padx=(20, 0), pady=(10, 10))
        
        # Historique Client 

        # Rechrche
        self.entry = customtkinter.CTkEntry(self.tabview.tab("Historique Client"), placeholder_text="...")
        self.entry.grid(row=0, column=0, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self.tabview.tab("Historique Client"), text="Recherche", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=search_client)
        self.main_button_1.grid(row=0, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.main_button_2 = customtkinter.CTkButton(master=self.tabview.tab("Historique Client"), text="Rafrichir", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command= lambda: client_database(self.client_tree))
        self.main_button_2.grid(row=0, column=3)
        
        # Treeview
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("c_Treeview",
            background="#D3D3D3",
            foreground="black",
            rowheight=25,
            fieldbackground="#D3D3D3")
        self.style.map('c_Treeview',
            background=[('selected', "#347083")])
        
        self.client_frame = customtkinter.CTkFrame(self.tabview.tab("Historique Client"))
        self.client_frame.grid(row=1, column=0, columnspan=4, rowspan=4, sticky="nsew")

        self.client_scroll = customtkinter.CTkScrollbar(self.client_frame)
        self.client_scroll.pack(side=RIGHT, fill=Y)

        self.client_tree = ttk.Treeview(self.client_frame, yscrollcommand=self.client_scroll.set, selectmode="extended")
        self.client_tree.pack()
        
        self.client_tree['columns'] = ("Num","client", "voiture", "modele","matricule", "telephone", "km")

        self.client_tree.column("#0", width=0, stretch=NO)
        self.client_tree.column("Num", anchor=CENTER, width=20)
        self.client_tree.column("client", anchor=CENTER, width=150)
        self.client_tree.column("voiture", anchor=CENTER, width=130)
        self.client_tree.column("modele", anchor=CENTER, width=130)
        self.client_tree.column("matricule", anchor=CENTER, width=130)
        self.client_tree.column("telephone", anchor=CENTER, width=130)
        self.client_tree.column("km", anchor=CENTER, width=130)

        self.client_tree.heading("#0", text="", anchor=CENTER)
        self.client_tree.heading("Num", text="N", anchor=CENTER)
        self.client_tree.heading("client", text="Client", anchor=CENTER)
        self.client_tree.heading("voiture", text="Voiture", anchor=CENTER)
        self.client_tree.heading("modele", text="Modele", anchor=CENTER)
        self.client_tree.heading("matricule", text="Matricule", anchor=CENTER)
        self.client_tree.heading("telephone", text="Telephone", anchor=CENTER)
        self.client_tree.heading("km", text="kilométrage", anchor=CENTER)

        self.client_tree.tag_configure('oddrow', background="#E8E8E8")
        self.client_tree.tag_configure('evenrow', background="#DFDFDF")

        client_database(self.client_tree)

        # entry frame
        self.entry_frame = customtkinter.CTkFrame(self.tabview.tab("Historique Client"))
        self.entry_frame.grid(row=6, column=0, columnspan=4, rowspan=4, sticky="nsew")

        self.id_label = customtkinter.CTkLabel(self.entry_frame, text="id")
        self.id_label.grid(row=0, column=0, padx=10, pady=5)
        self.H_id_entry = customtkinter.CTkEntry(self.entry_frame, height=25, border_width=2, corner_radius=10)
        self.H_id_entry.grid(row=0, column=1, padx=10, pady=5)

        self.client_label = customtkinter.CTkLabel(self.entry_frame, text="Client")
        self.client_label.grid(row=1, column=0, padx=10, pady=5)
        self.H_client_entry = customtkinter.CTkEntry(self.entry_frame, height=25, border_width=2, corner_radius=10)
        self.H_client_entry.grid(row=1, column=1, padx=10, pady=5)

        self.voiture_label = customtkinter.CTkLabel(self.entry_frame, text="Voiture")
        self.voiture_label.grid(row=1, column=2, padx=10, pady=5)
        self.H_voiture_entry = customtkinter.CTkEntry(self.entry_frame, height=25, border_width=2, corner_radius=10)
        self.H_voiture_entry.grid(row=1, column=3, padx=10, pady=5)

        self.modele_label = customtkinter.CTkLabel(self.entry_frame, text="Modele")
        self.modele_label.grid(row=2, column=2, padx=10, pady=5)
        self.H_modele_entry = customtkinter.CTkEntry(self.entry_frame, height=25, border_width=2, corner_radius=10)
        self.H_modele_entry.grid(row=2, column=3, padx=10, pady=5)

        self.matricule_label = customtkinter.CTkLabel(self.entry_frame, text="Matricule")
        self.matricule_label.grid(row=2, column=0, padx=10, pady=5)
        self.H_matricule_entry = customtkinter.CTkEntry(self.entry_frame, height=25, border_width=2, corner_radius=10)
        self.H_matricule_entry.grid(row=2, column=1, padx=10, pady=5)

        self.t_label = customtkinter.CTkLabel(self.entry_frame, text="Telephone")
        self.t_label.grid(row=3, column=2, padx=10, pady=5)
        self.H_t_entry = customtkinter.CTkEntry(self.entry_frame, height=25, border_width=2, corner_radius=10)
        self.H_t_entry.grid(row=3, column=3, padx=10, pady=5)

        self.k_label = customtkinter.CTkLabel(self.entry_frame, text="kilométrage")
        self.k_label.grid(row=3, column=0, padx=10, pady=5)
        self.H_k_entry = customtkinter.CTkEntry(self.entry_frame, height=25, border_width=2, corner_radius=10)
        self.H_k_entry.grid(row=3, column=1, padx=10, pady=5)

        self.vider_button = customtkinter.CTkButton(self.entry_frame, text="Vider les case", font=customtkinter.CTkFont(size=15, weight="bold"), command=vider_client)
        self.vider_button.grid(row=4, column=0, padx=50, pady=5)

        self.f_button = customtkinter.CTkButton(self.entry_frame, text="ajouter une facture", font=customtkinter.CTkFont(size=15, weight="bold"), command=H_facture)
        self.f_button.grid(row=4, column=1, padx=50, pady=5)

        self.add_button = customtkinter.CTkButton(self.entry_frame, text="Ajouter", font=customtkinter.CTkFont(size=15, weight="bold"), command=add_Hclient)
        self.add_button.grid(row=5, column=1, padx=50, pady=5)

        self.update_button = customtkinter.CTkButton(self.entry_frame, text="Modifier", font=customtkinter.CTkFont(size=15, weight="bold"), command=update_c)
        self.update_button.grid(row=5, column=0, padx=10, pady=5)

        self.suprimer_button = customtkinter.CTkButton(self.entry_frame, text="Suprimer", fg_color='red2', font=customtkinter.CTkFont(size=15, weight="bold"), command=suprimer_c)
        self.suprimer_button.grid(row=5, column=3, padx=10, pady=5)

        self.client_scroll.configure(command=self.client_tree.yview)
        self.client_tree.bind("<ButtonRelease-1>", select_client)


    def destroy_client(self):
        for widget in window.winfo_children():
            widget.destroy()


class stock:
    def __init__(self) -> None:
        super().__init__()

        # create sidebar frame with widgets
        self.sidebar = sidebar()
        
        # create tabview
        self.tabview = customtkinter.CTkTabview(window, width=250)
        self.tabview.grid(row=0, column=1, columnspan=3, rowspan=4, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Stock")
        self.tabview.tab("Stock").grid_columnconfigure(4, weight=1) 

        # Rechrche
        self.entry = customtkinter.CTkEntry(self.tabview.tab("Stock"), placeholder_text="...")
        self.entry.grid(row=0, column=0, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self.tabview.tab("Stock"), text="Recherche", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=search_stock)
        self.main_button_1.grid(row=0, column=2, padx=(5, 20), pady=(20, 20), sticky="nsew")

        self.main_button_2 = customtkinter.CTkButton(master=self.tabview.tab("Stock"), text="Rafrichir", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command= lambda: query_database(self.stock_tree))
        self.main_button_2.grid(row=0, column=3, padx=(5, 5), pady=(20, 20),)
        
        # Treeview
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("c_Treeview",
            background="#D3D3D3",
            foreground="black",
            rowheight=25,
            fieldbackground="#D3D3D3")
        self.style.map('c_Treeview',
            background=[('selected', "#347083")])
        
        self.stock_frame = customtkinter.CTkFrame(self.tabview.tab("Stock"))
        self.stock_frame.grid(row=1, column=0, columnspan=4, rowspan=4, sticky="nsew")

        self.stock_scroll = customtkinter.CTkScrollbar(self.stock_frame)
        self.stock_scroll.pack(side=RIGHT, fill=Y)

        self.stock_tree = ttk.Treeview(self.stock_frame, yscrollcommand=self.stock_scroll.set, selectmode="extended")
        self.stock_tree.pack()
        
        self.stock_tree['columns'] = ("N","piece", "referance", "quantite", "prix", "vente")

        self.stock_tree.column("#0", width=0, stretch=NO)
        self.stock_tree.column("N", anchor=CENTER, width=20)
        self.stock_tree.column("piece", anchor=CENTER, width=150)
        self.stock_tree.column("referance", anchor=CENTER, width=150)
        self.stock_tree.column("quantite", anchor=CENTER, width=150)
        self.stock_tree.column("prix", anchor=CENTER, width=150)
        self.stock_tree.column("vente", anchor=CENTER, width=150)

        self.stock_tree.heading("#0", text="", anchor=CENTER)
        self.stock_tree.heading("N", text="N", anchor=CENTER)
        self.stock_tree.heading("piece", text="Piece", anchor=CENTER)
        self.stock_tree.heading("referance", text="Referance", anchor=CENTER)
        self.stock_tree.heading("quantite", text="Quantite", anchor=CENTER)
        self.stock_tree.heading("prix", text="Prix", anchor=CENTER)
        self.stock_tree.heading("vente", text="Vente", anchor=CENTER)

        try:
            self.stock_tree.tag_configure('oddrow', background="#E8E8E8")
        except:
            pass

        try:
            self.stock_tree.tag_configure('evenrow', background="#DFDFDF")
        except:
            pass

        try:
            self.stock_tree.tag_configure('r_stock', background="#e46161")
        except:
            pass

        query_database(self.stock_tree)

        # entry frame
        self.entry_frame = customtkinter.CTkFrame(self.tabview.tab("Stock"))
        self.entry_frame.grid(row=6, column=0, columnspan=4, rowspan=4, sticky="nsew")

        self.id_label = customtkinter.CTkLabel(self.entry_frame, text="id")
        self.id_label.grid(row=0, column=0, padx=10, pady=5)
        self.id_entry = customtkinter.CTkEntry(self.entry_frame, height=25, border_width=2, corner_radius=10)
        self.id_entry.grid(row=0, column=1, padx=10, pady=5)

        self.piece_label = customtkinter.CTkLabel(self.entry_frame, text="Piece")
        self.piece_label.grid(row=1, column=0, padx=10, pady=5)
        self.piece_entry = customtkinter.CTkEntry(self.entry_frame, height=25, border_width=2, corner_radius=10)
        self.piece_entry.grid(row=1, column=1, padx=10, pady=5)

        self.referance_label = customtkinter.CTkLabel(self.entry_frame, text="Referance")
        self.referance_label.grid(row=0, column=2, padx=10, pady=5)
        self.referance_entry = customtkinter.CTkEntry(self.entry_frame, height=25, border_width=2, corner_radius=10)
        self.referance_entry.grid(row=0, column=3, padx=10, pady=5)

        self.quantite_label = customtkinter.CTkLabel(self.entry_frame, text="Quantite")
        self.quantite_label.grid(row=1, column=2, padx=10, pady=5)
        self.quantite_entry = customtkinter.CTkEntry(self.entry_frame, height=25, border_width=2, corner_radius=10)
        self.quantite_entry.grid(row=1, column=3, padx=10, pady=5)

        self.prix_label = customtkinter.CTkLabel(self.entry_frame, text="Prix d'achat")
        self.prix_label.grid(row=2, column=0, padx=10, pady=5)
        self.prix_entry = customtkinter.CTkEntry(self.entry_frame, height=25, border_width=2, corner_radius=10)
        self.prix_entry.grid(row=2, column=1, padx=10, pady=5)

        self.prix_vente_label = customtkinter.CTkLabel(self.entry_frame, text="Prix de vente")
        self.prix_vente_label.grid(row=2, column=2, padx=10, pady=5)
        self.prix_vente_entry = customtkinter.CTkEntry(self.entry_frame, height=25, border_width=2, corner_radius=10)
        self.prix_vente_entry.grid(row=2, column=3, padx=10, pady=5)

        self.vider_button = customtkinter.CTkButton(self.entry_frame, text="Vider les case", font=customtkinter.CTkFont(size=15, weight="bold"), command=vider_stock)
        self.vider_button.grid(row=4, column=0, padx=50, pady=5)

        self.f_button = customtkinter.CTkButton(self.entry_frame, text="Ajouter un Bon", font=customtkinter.CTkFont(size=15, weight="bold"), command=ajouter_bon)
        self.f_button.grid(row=4, column=1, padx=50, pady=5)

        self.add_button = customtkinter.CTkButton(self.entry_frame, text="Ajouter", font=customtkinter.CTkFont(size=15, weight="bold"), command=add_stock)
        self.add_button.grid(row=5, column=1, padx=50, pady=5)

        self.update_button = customtkinter.CTkButton(self.entry_frame, text="Modifier", font=customtkinter.CTkFont(size=15, weight="bold"), command=update_stock)
        self.update_button.grid(row=5, column=0, padx=10, pady=5)

        self.suprimer_button = customtkinter.CTkButton(self.entry_frame, text="Suprimer", fg_color='red2', font=customtkinter.CTkFont(size=15, weight="bold"), command=suprimer_stock)
        self.suprimer_button.grid(row=5, column=3, padx=10, pady=5)

        self.stock_scroll.configure(command=self.stock_tree.yview)
        self.stock_tree.bind("<ButtonRelease-1>", select_stock)


    def destroy_stock(self):
        for widget in window.winfo_children():
            widget.destroy()


class facture:
    def __init__(self) -> None:
        super().__init__()

        # create sidebar frame with widgets
        self.sidebar = sidebar()

        # create tabview
        self.tabview = customtkinter.CTkTabview(window, width=250)
        self.tabview.grid(row=0, column=1, columnspan=3, rowspan=4, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Facture Payer")
        self.tabview.add("Facture non Payer")
        self.tabview.add("Bon Payer")
        self.tabview.add("Bon non Payer")
        self.tabview.add("Devis")
        self.tabview.tab("Facture Payer").grid_columnconfigure(4, weight=1)
        self.tabview.tab("Facture non Payer").grid_columnconfigure(4, weight=1)
        self.tabview.tab("Bon Payer").grid_columnconfigure(4, weight=1)
        self.tabview.tab("Bon non Payer").grid_columnconfigure(4, weight=1)
        self.tabview.tab("Devis").grid_columnconfigure(4, weight=1)
        
        # facture payer
        # Rechrche
        self.entry1 = customtkinter.CTkEntry(self.tabview.tab("Facture Payer"), placeholder_text="...")
        self.entry1.grid(row=0, column=0, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self.tabview.tab("Facture Payer"), text="Recherche", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=search_facture)
        self.main_button_1.grid(row=0, column=2, padx=(5, 20), pady=(20, 20), sticky="nsew")

        self.main_button_2 = customtkinter.CTkButton(master=self.tabview.tab("Facture Payer"), text="Rafrichir", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command= lambda: facture_database(self.facture_tree))
        self.main_button_2.grid(row=0, column=3, padx=(5, 5), pady=(20, 20),)
       
        # Treeview
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("c_Treeview",
            background="#D3D3D3",
            foreground="black",
            rowheight=25,
            fieldbackground="#D3D3D3")
        self.style.map('c_Treeview',
            background=[('selected', "#347083")])
        
        self.facture_frame = customtkinter.CTkFrame(self.tabview.tab("Facture Payer"))
        self.facture_frame.grid(row=1, column=0, columnspan=4, rowspan=4, sticky="nsew")

        self.facture_scroll = customtkinter.CTkScrollbar(self.facture_frame)
        self.facture_scroll.pack(side=RIGHT, fill=Y)

        self.facture_tree = ttk.Treeview(self.facture_frame, yscrollcommand=self.facture_scroll.set, selectmode="extended")
        self.facture_tree.pack()
        
        self.facture_tree['columns'] = ("N","n_facture", "client", "matricule", "date", "total")

        self.facture_tree.column("#0", width=0, stretch=NO)
        self.facture_tree.column("N", anchor=CENTER, width=20)
        self.facture_tree.column("n_facture", anchor=CENTER, width=150)
        self.facture_tree.column("client", anchor=CENTER, width=150)
        self.facture_tree.column("matricule", anchor=CENTER, width=150)
        self.facture_tree.column("date", anchor=CENTER, width=150)
        self.facture_tree.column("total", anchor=CENTER, width=150)

        self.facture_tree.heading("#0", text="", anchor=CENTER)
        self.facture_tree.heading("N", text="N", anchor=CENTER)
        self.facture_tree.heading("n_facture", text="Facture", anchor=CENTER)
        self.facture_tree.heading("client", text="Client", anchor=CENTER)
        self.facture_tree.heading("matricule", text="Matricule", anchor=CENTER)
        self.facture_tree.heading("date", text="Date", anchor=CENTER)
        self.facture_tree.heading("total", text="Total", anchor=CENTER)

        self.facture_tree.tag_configure('oddrow', background="#E8E8E8")
        self.facture_tree.tag_configure('evenrow', background="#DFDFDF")

        facture_database(self.facture_tree)

        # entry frame
        self.entry_frame = customtkinter.CTkFrame(self.tabview.tab("Facture Payer"))
        self.entry_frame.grid(row=6, column=0, columnspan=4, rowspan=4, sticky="nsew")

        self.id1_entry = customtkinter.CTkEntry(self.entry_frame)
        
        self.nFacture_label = customtkinter.CTkLabel(self.entry_frame, text="Numero de Facture")
        self.nFacture_label.grid(row=0, column=0, padx=10, pady=20)
        self.nFacture_entry = customtkinter.CTkEntry(self.entry_frame, height=25, border_width=2, corner_radius=10)
        self.nFacture_entry.grid(row=0, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.ouvrire_button = customtkinter.CTkButton(self.entry_frame, text="Ouvrire", font=customtkinter.CTkFont(size=15, weight="bold"), command=ouvrire_f)
        self.ouvrire_button.grid(row=1, column=0, padx=10, pady=20)

        self.suprimer_button = customtkinter.CTkButton(self.entry_frame, text="Suprimer", fg_color='red2', font=customtkinter.CTkFont(size=15, weight="bold"), command=F_suprimer)
        self.suprimer_button.grid(row=1, column=3, padx=10, pady=20)

        self.facture_scroll.configure(command=self.facture_tree.yview)
        self.facture_tree.bind("<ButtonRelease-1>", select_facture)

        # facture non payer
        # Rechrche
        self.entry2 = customtkinter.CTkEntry(self.tabview.tab("Facture non Payer"), placeholder_text="...")
        self.entry2.grid(row=0, column=0, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self.tabview.tab("Facture non Payer"), text="Recherche", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=search_Nfacture)
        self.main_button_1.grid(row=0, column=2, padx=(5, 20), pady=(20, 20), sticky="nsew")

        self.main_button_2 = customtkinter.CTkButton(master=self.tabview.tab("Facture non Payer"), text="Rafrichir", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command= lambda: factureNp_database(self.factureNp_tree))
        self.main_button_2.grid(row=0, column=3, padx=(5, 5), pady=(20, 20),)

        # Treeview
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("c_Treeview",
            background="#D3D3D3",
            foreground="black",
            rowheight=25,
            fieldbackground="#D3D3D3")
        self.style.map('c_Treeview',
            background=[('selected', "#347083")])
        
        self.factureNp_frame = customtkinter.CTkFrame(self.tabview.tab("Facture non Payer"))
        self.factureNp_frame.grid(row=1, column=0, columnspan=4, rowspan=4, sticky="nsew")

        self.factureNp_scroll = customtkinter.CTkScrollbar(self.factureNp_frame)
        self.factureNp_scroll.pack(side=RIGHT, fill=Y)

        self.factureNp_tree = ttk.Treeview(self.factureNp_frame, yscrollcommand=self.factureNp_scroll.set, selectmode="extended")
        self.factureNp_tree.pack()
        
        self.factureNp_tree['columns'] = ("N","n_facture", "client", "matricule", "date","total", "avance")

        self.factureNp_tree.column("#0", width=0, stretch=NO)
        self.factureNp_tree.column("N", anchor=CENTER, width=20)
        self.factureNp_tree.column("n_facture", anchor=CENTER, width=140)
        self.factureNp_tree.column("client", anchor=CENTER, width=140)
        self.factureNp_tree.column("matricule", anchor=CENTER, width=140)
        self.factureNp_tree.column("date", anchor=CENTER, width=140)
        self.factureNp_tree.column("total", anchor=CENTER, width=140)
        self.factureNp_tree.column("avance", anchor=CENTER, width=140)

        self.factureNp_tree.heading("#0", text="", anchor=CENTER)
        self.factureNp_tree.heading("N", text="N", anchor=CENTER)
        self.factureNp_tree.heading("n_facture", text="Facture", anchor=CENTER)
        self.factureNp_tree.heading("client", text="Client", anchor=CENTER)
        self.factureNp_tree.heading("matricule", text="Matricule", anchor=CENTER)
        self.factureNp_tree.heading("date", text="Date", anchor=CENTER)
        self.factureNp_tree.heading("total", text="Total", anchor=CENTER)
        self.factureNp_tree.heading("avance", text="Avance", anchor=CENTER)

        self.factureNp_tree.tag_configure('oddrow', background="#E8E8E8")
        self.factureNp_tree.tag_configure('evenrow', background="#DFDFDF")

        factureNp_database(self.factureNp_tree)

        # entry frame
        self.N_entry_frame = customtkinter.CTkFrame(self.tabview.tab("Facture non Payer"))
        self.N_entry_frame.grid(row=6, column=0, columnspan=4, rowspan=4, sticky="nsew")

        self.id2_entry = customtkinter.CTkEntry(self.N_entry_frame)
        
        self.nFactureNp_label = customtkinter.CTkLabel(self.N_entry_frame, text="Numero de Facture")
        self.nFactureNp_label.grid(row=0, column=0, padx=10, pady=20)
        self.nFactureNp_entry = customtkinter.CTkEntry(self.N_entry_frame, height=25, border_width=2, corner_radius=10)
        self.nFactureNp_entry.grid(row=0, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.FacturePayement_label = customtkinter.CTkLabel(self.N_entry_frame, text="Payement")
        self.FacturePayement_label.grid(row=1, column=0, padx=10, pady=20)
        self.FacturePayement_entry = customtkinter.CTkEntry(self.N_entry_frame, height=25, border_width=2, corner_radius=10)
        self.FacturePayement_entry.grid(row=1, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.payement_button = customtkinter.CTkButton(self.N_entry_frame, text="Payement", font=customtkinter.CTkFont(size=15, weight="bold"), command=f_payment)
        self.payement_button.grid(row=1, column=3, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.Np_ouvrire_button = customtkinter.CTkButton(self.N_entry_frame, text="Ouvrire", font=customtkinter.CTkFont(size=15, weight="bold"), command=ouvrire_Nf)
        self.Np_ouvrire_button.grid(row=2, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.Np_suprimer_button = customtkinter.CTkButton(self.N_entry_frame, text="Suprimer", fg_color='red2', font=customtkinter.CTkFont(size=15, weight="bold"), command=NF_suprimer)
        self.Np_suprimer_button.grid(row=2, column=3, padx=(20, 0), pady=(20, 20), sticky="nsew")
        
        self.factureNp_scroll.configure(command=self.factureNp_tree.yview)
        self.factureNp_tree.bind("<ButtonRelease-1>", select_Nfacture)

        # bon payer
        # Rechrche
        self.entry3 = customtkinter.CTkEntry(self.tabview.tab("Bon Payer"), placeholder_text="...")
        self.entry3.grid(row=0, column=0, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self.tabview.tab("Bon Payer"), text="Recherche", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=search_bon)
        self.main_button_1.grid(row=0, column=2, padx=(5, 20), pady=(20, 20), sticky="nsew")

        self.main_button_2 = customtkinter.CTkButton(master=self.tabview.tab("Bon Payer"), text="Rafrichir", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command= lambda: bon_database(self.bon_tree))
        self.main_button_2.grid(row=0, column=3, padx=(5, 5), pady=(20, 20),)
       
        # Treeview
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("c_Treeview",
            background="#D3D3D3",
            foreground="black",
            rowheight=25,
            fieldbackground="#D3D3D3")
        self.style.map('c_Treeview',
            background=[('selected', "#347083")])
        
        self.bon_frame = customtkinter.CTkFrame(self.tabview.tab("Bon Payer"))
        self.bon_frame.grid(row=1, column=0, columnspan=4, rowspan=4, sticky="nsew")

        self.bon_scroll = customtkinter.CTkScrollbar(self.bon_frame)
        self.bon_scroll.pack(side=RIGHT, fill=Y)

        self.bon_tree = ttk.Treeview(self.bon_frame, yscrollcommand=self.bon_scroll.set, selectmode="extended")
        self.bon_tree.pack()
        
        self.bon_tree['columns'] = ("N","n_bon", "client", "date", "total")

        self.bon_tree.column("#0", width=0, stretch=NO)
        self.bon_tree.column("N", anchor=CENTER, width=20)
        self.bon_tree.column("n_bon", anchor=CENTER, width=180)
        self.bon_tree.column("client", anchor=CENTER, width=180)
        self.bon_tree.column("date", anchor=CENTER, width=180)
        self.bon_tree.column("total", anchor=CENTER, width=180)

        self.bon_tree.heading("#0", text="", anchor=CENTER)
        self.bon_tree.heading("N", text="N", anchor=CENTER)
        self.bon_tree.heading("n_bon", text="Bon", anchor=CENTER)
        self.bon_tree.heading("client", text="Client", anchor=CENTER)
        self.bon_tree.heading("date", text="Date", anchor=CENTER)
        self.bon_tree.heading("total", text="Total", anchor=CENTER)

        self.bon_tree.tag_configure('oddrow', background="#E8E8E8")
        self.bon_tree.tag_configure('evenrow', background="#DFDFDF")

        bon_database(self.bon_tree)

        # entry frame
        self.entry_frame = customtkinter.CTkFrame(self.tabview.tab("Bon Payer"))
        self.entry_frame.grid(row=6, column=0, columnspan=4, rowspan=4, sticky="nsew")

        self.id3_entry = customtkinter.CTkEntry(self.entry_frame)
        
        self.nbon_label = customtkinter.CTkLabel(self.entry_frame, text="Numero de Bon")
        self.nbon_label.grid(row=0, column=0, padx=10, pady=20)
        self.nbon_entry = customtkinter.CTkEntry(self.entry_frame, height=25, border_width=2, corner_radius=10)
        self.nbon_entry.grid(row=0, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.ouvrire_button = customtkinter.CTkButton(self.entry_frame, text="Ouvrire", font=customtkinter.CTkFont(size=15, weight="bold"), command=ouvrire_b)
        self.ouvrire_button.grid(row=1, column=0, padx=10, pady=20)

        self.suprimer_button = customtkinter.CTkButton(self.entry_frame, text="Suprimer", fg_color='red2', font=customtkinter.CTkFont(size=15, weight="bold"), command=b_suprimer)
        self.suprimer_button.grid(row=1, column=3, padx=10, pady=20)

        self.bon_scroll.configure(command=self.bon_tree.yview)
        self.bon_tree.bind("<ButtonRelease-1>", select_bon)

        # bon non payer
        # Rechrche
        self.entry4 = customtkinter.CTkEntry(self.tabview.tab("Bon non Payer"), placeholder_text="...")
        self.entry4.grid(row=0, column=0, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self.tabview.tab("Bon non Payer"), text="Recherche", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=search_Nbon)
        self.main_button_1.grid(row=0, column=2, padx=(5, 20), pady=(20, 20), sticky="nsew")

        self.main_button_2 = customtkinter.CTkButton(master=self.tabview.tab("Bon non Payer"), text="Rafrichir", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command= lambda: bonNp_database(self.bonNp_tree))
        self.main_button_2.grid(row=0, column=3, padx=(5, 5), pady=(20, 20),)

        # Treeview
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("c_Treeview",
            background="#D3D3D3",
            foreground="black",
            rowheight=25,
            fieldbackground="#D3D3D3")
        self.style.map('c_Treeview',
            background=[('selected', "#347083")])
        
        self.bonNp_frame = customtkinter.CTkFrame(self.tabview.tab("Bon non Payer"))
        self.bonNp_frame.grid(row=1, column=0, columnspan=4, rowspan=4, sticky="nsew")

        self.bonNp_scroll = customtkinter.CTkScrollbar(self.bonNp_frame)
        self.bonNp_scroll.pack(side=RIGHT, fill=Y)

        self.bonNp_tree = ttk.Treeview(self.bonNp_frame, yscrollcommand=self.bonNp_scroll.set, selectmode="extended")
        self.bonNp_tree.pack()
        
        self.bonNp_tree['columns'] = ("N","n_bon", "client", "date", "total", "avance")

        self.bonNp_tree.column("#0", width=0, stretch=NO)
        self.bonNp_tree.column("N", anchor=CENTER, width=20)
        self.bonNp_tree.column("n_bon", anchor=CENTER, width=150)
        self.bonNp_tree.column("client", anchor=CENTER, width=150)
        self.bonNp_tree.column("date", anchor=CENTER, width=150)
        self.bonNp_tree.column("total", anchor=CENTER, width=150)
        self.bonNp_tree.column("avance", anchor=CENTER, width=150)

        self.bonNp_tree.heading("#0", text="", anchor=CENTER)
        self.bonNp_tree.heading("N", text="N", anchor=CENTER)
        self.bonNp_tree.heading("n_bon", text="Bon", anchor=CENTER)
        self.bonNp_tree.heading("client", text="Client", anchor=CENTER)
        self.bonNp_tree.heading("date", text="Date", anchor=CENTER)
        self.bonNp_tree.heading("total", text="Total", anchor=CENTER)
        self.bonNp_tree.heading("avance", text="Avance", anchor=CENTER)

        self.bonNp_tree.tag_configure('oddrow', background="#E8E8E8")
        self.bonNp_tree.tag_configure('evenrow', background="#DFDFDF")

        bonNp_database(self.bonNp_tree)

        # entry frame
        self.N_entry_frame = customtkinter.CTkFrame(self.tabview.tab("Bon non Payer"))
        self.N_entry_frame.grid(row=6, column=0, columnspan=4, rowspan=4, sticky="nsew")

        self.id4_entry = customtkinter.CTkEntry(self.N_entry_frame)
        
        self.nbonNp_label = customtkinter.CTkLabel(self.N_entry_frame, text="Numero de Bon")
        self.nbonNp_label.grid(row=0, column=0, padx=10, pady=20)
        self.nbonNp_entry = customtkinter.CTkEntry(self.N_entry_frame, height=25, border_width=2, corner_radius=10)
        self.nbonNp_entry.grid(row=0, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.bonPayement_label = customtkinter.CTkLabel(self.N_entry_frame, text="Payement")
        self.bonPayement_label.grid(row=1, column=0, padx=10, pady=20)
        self.bonPayement_entry = customtkinter.CTkEntry(self.N_entry_frame, height=25, border_width=2, corner_radius=10)
        self.bonPayement_entry.grid(row=1, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.payement_button = customtkinter.CTkButton(self.N_entry_frame, text="Payement", font=customtkinter.CTkFont(size=15, weight="bold"), command=b_payment)
        self.payement_button.grid(row=1, column=3, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.Np_ouvrire_button = customtkinter.CTkButton(self.N_entry_frame, text="Ouvrire", font=customtkinter.CTkFont(size=15, weight="bold"), command=ouvrire_Nb)
        self.Np_ouvrire_button.grid(row=2, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.Np_suprimer_button = customtkinter.CTkButton(self.N_entry_frame, text="Suprimer", fg_color='red2', font=customtkinter.CTkFont(size=15, weight="bold"), command=Nb_suprimer)
        self.Np_suprimer_button.grid(row=2, column=3, padx=(20, 0), pady=(20, 20), sticky="nsew")
        
        self.factureNp_scroll.configure(command=self.factureNp_tree.yview)
        self.bonNp_tree.bind("<ButtonRelease-1>", select_Nbon)

        # devie
        # Rechrche
        self.entry5 = customtkinter.CTkEntry(self.tabview.tab("Devis"), placeholder_text="...")
        self.entry5.grid(row=0, column=0, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self.tabview.tab("Devis"), text="Recherche", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=search_devie)
        self.main_button_1.grid(row=0, column=2, padx=(5, 20), pady=(20, 20), sticky="nsew")

        self.main_button_2 = customtkinter.CTkButton(master=self.tabview.tab("Devis"), text="Rafrichir", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command= lambda: devie_database(self.devie_tree))
        self.main_button_2.grid(row=0, column=3, padx=(5, 5), pady=(20, 20),)
       
        # Treeview
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("c_Treeview",
            background="#D3D3D3",
            foreground="black",
            rowheight=25,
            fieldbackground="#D3D3D3")
        self.style.map('c_Treeview',
            background=[('selected', "#347083")])
        
        self.devie_frame = customtkinter.CTkFrame(self.tabview.tab("Devis"))
        self.devie_frame.grid(row=1, column=0, columnspan=4, rowspan=4, sticky="nsew")

        self.devie_scroll = customtkinter.CTkScrollbar(self.devie_frame)
        self.devie_scroll.pack(side=RIGHT, fill=Y)

        self.devie_tree = ttk.Treeview(self.devie_frame, yscrollcommand=self.devie_scroll.set, selectmode="extended")
        self.devie_tree.pack()
        
        self.devie_tree['columns'] = ("N","n_devie", "client", "matricule", "total")

        self.devie_tree.column("#0", width=0, stretch=NO)
        self.devie_tree.column("N", anchor=CENTER, width=20)
        self.devie_tree.column("n_devie", anchor=CENTER, width=180)
        self.devie_tree.column("client", anchor=CENTER, width=180)
        self.devie_tree.column("matricule", anchor=CENTER, width=180)
        self.devie_tree.column("total", anchor=CENTER, width=180)

        self.devie_tree.heading("#0", text="", anchor=CENTER)
        self.devie_tree.heading("N", text="N", anchor=CENTER)
        self.devie_tree.heading("n_devie", text="Devis", anchor=CENTER)
        self.devie_tree.heading("client", text="Client", anchor=CENTER)
        self.devie_tree.heading("matricule", text="Matricule", anchor=CENTER)
        self.devie_tree.heading("total", text="Total", anchor=CENTER)

        self.devie_tree.tag_configure('oddrow', background="#E8E8E8")
        self.devie_tree.tag_configure('evenrow', background="#DFDFDF")

        devie_database(self.devie_tree)

        # entry frame
        self.entry_frame = customtkinter.CTkFrame(self.tabview.tab("Devis"))
        self.entry_frame.grid(row=6, column=0, columnspan=4, rowspan=4, sticky="nsew")

        self.id5_entry = customtkinter.CTkEntry(self.entry_frame)
        
        self.ndevie_label = customtkinter.CTkLabel(self.entry_frame, text="Numero de Devis")
        self.ndevie_label.grid(row=0, column=0, padx=10, pady=20)
        self.ndevie_entry = customtkinter.CTkEntry(self.entry_frame, height=25, border_width=2, corner_radius=10)
        self.ndevie_entry.grid(row=0, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.ouvrire_button = customtkinter.CTkButton(self.entry_frame, text="Ouvrire", font=customtkinter.CTkFont(size=15, weight="bold"), command=ouvrire_devie)
        self.ouvrire_button.grid(row=1, column=0, padx=10, pady=20)

        self.ajouter_button = customtkinter.CTkButton(self.entry_frame, text="Ajouter un Devis", font=customtkinter.CTkFont(size=15, weight="bold"), command=client_entry)
        self.ajouter_button.grid(row=1, column=1, padx=10, pady=20)

        self.suprimer_button = customtkinter.CTkButton(self.entry_frame, text="Suprimer", fg_color='red2', font=customtkinter.CTkFont(size=15, weight="bold"), command=D_suprimer)
        self.suprimer_button.grid(row=1, column=3, padx=10, pady=20)

        self.devie_scroll.configure(command=self.devie_tree.yview)
        self.devie_tree.bind("<ButtonRelease-1>", select_devie)


    def destroy_facture(self):
        for widget in window.winfo_children():
            widget.destroy()


class bill_window:
    def __init__(self, top=None):
        super().__init__()

        self.liste = liste()
        # sidebare
        self.sidebar = sidebar()

        # Bill frame
        self.F_entry_frame = customtkinter.CTkFrame(window)
        self.F_entry_frame.grid(row=0, column=1, columnspan=4, rowspan=4, sticky="nsew")
        self.F_entry_frame.grid_columnconfigure(4, weight=1) 

        self.dg_label = customtkinter.CTkLabel(self.F_entry_frame, text="disignation", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.dg_label.grid(row=0, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.dg_entry = customtkinter.CTkEntry(self.F_entry_frame, width=200, height=15)
        self.dg_entry.grid(row=0, column=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.referance_label = customtkinter.CTkLabel(self.F_entry_frame, text="Referance", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.referance_label.grid(row=1, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.referance_entry = customtkinter.CTkComboBox(self.F_entry_frame, values=self.liste, width=200, height=15)
        self.referance_entry.grid(row=1, column=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.prix_label = customtkinter.CTkLabel(self.F_entry_frame, text="Prix unite", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.prix_label.grid(row=2, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.prix_entry = customtkinter.CTkEntry(self.F_entry_frame, width=200, height=15)
        self.prix_entry.grid(row=2, column=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.quantite_label = customtkinter.CTkLabel(self.F_entry_frame, text="Quantite", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.quantite_label.grid(row=3, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.quantite_entry = customtkinter.CTkEntry(self.F_entry_frame, width=200, height=15)
        self.quantite_entry.grid(row=3, column=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.button = customtkinter.CTkButton(self.F_entry_frame, text="ajouter", fg_color='gray', font=customtkinter.CTkFont(size=15, weight="bold"), command=add_produit)
        self.button.grid(row=4, column=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.button = customtkinter.CTkButton(self.F_entry_frame, text="Total", fg_color='gray', font=customtkinter.CTkFont(size=15, weight="bold"), command=prix_total)
        self.button.grid(row=5, column=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.button = customtkinter.CTkButton(self.F_entry_frame, text="Sauvgarder", fg_color='gray', font=customtkinter.CTkFont(size=15, weight="bold"), command=F_etat)
        self.button.grid(row=6, column=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.button = customtkinter.CTkButton(self.F_entry_frame, text="Initialiser", fg_color='gray', font=customtkinter.CTkFont(size=15, weight="bold"), command=F_Initialiser)
        self.button.grid(row=7, column=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.bill = tkst.ScrolledText(self.F_entry_frame, bg='white')
        self.bill.grid(row=0, column=4, rowspan=8, padx=(20, 0), pady=(20, 20))
        self.referance_entry.set('')
        self.referance_entry.bind('<KeyRelease>', search)
        

    def destroy_bill(self):
        for widget in window.winfo_children():
            widget.destroy()  


class bon_window:
    def __init__(self, top=None):
        super().__init__()

        self.liste = liste()
        # sidebare
        self.sidebar = sidebar()

        # Bill frame
        self.F_entry_frame = customtkinter.CTkFrame(window)
        self.F_entry_frame.grid(row=0, column=1, columnspan=4, rowspan=4, sticky="nsew")
        self.F_entry_frame.grid_columnconfigure(4, weight=1) 

        self.dg_label = customtkinter.CTkLabel(self.F_entry_frame, text="Piece", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.dg_label.grid(row=0, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.dg_entry = customtkinter.CTkEntry(self.F_entry_frame, width=200, height=15)
        self.dg_entry.grid(row=0, column=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.referance_label = customtkinter.CTkLabel(self.F_entry_frame, text="Referance", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.referance_label.grid(row=1, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.referance_entry = customtkinter.CTkComboBox(self.F_entry_frame, values=self.liste, width=200, height=15)
        self.referance_entry.grid(row=1, column=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.prix_label = customtkinter.CTkLabel(self.F_entry_frame, text="Prix unite", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.prix_label.grid(row=2, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.prix_entry = customtkinter.CTkEntry(self.F_entry_frame, width=200, height=15)
        self.prix_entry.grid(row=2, column=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.quantite_label = customtkinter.CTkLabel(self.F_entry_frame, text="Quantite", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.quantite_label.grid(row=3, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.quantite_entry = customtkinter.CTkEntry(self.F_entry_frame, width=200, height=15)
        self.quantite_entry.grid(row=3, column=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.button = customtkinter.CTkButton(self.F_entry_frame, text="ajouter", fg_color='gray', font=customtkinter.CTkFont(size=15, weight="bold"), command=add_produit)
        self.button.grid(row=4, column=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.button = customtkinter.CTkButton(self.F_entry_frame, text="Total", fg_color='gray', font=customtkinter.CTkFont(size=15, weight="bold"), command=bon_total)
        self.button.grid(row=5, column=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.button = customtkinter.CTkButton(self.F_entry_frame, text="Sauvgarder", fg_color='gray', font=customtkinter.CTkFont(size=15, weight="bold"), command=B_etat)
        self.button.grid(row=6, column=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.button = customtkinter.CTkButton(self.F_entry_frame, text="Initialiser", fg_color='gray', font=customtkinter.CTkFont(size=15, weight="bold"), command=B_Initialiser)
        self.button.grid(row=7, column=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.bill = tkst.ScrolledText(self.F_entry_frame, bg='white')
        self.bill.grid(row=0, column=4, rowspan=8, padx=(20, 0), pady=(20, 20))
        self.referance_entry.set('')
        self.referance_entry.bind('<KeyRelease>', search)


    def destroy_bill(self):
        for widget in window.winfo_children():
            widget.destroy()     


class ouvrire_facture:
    def __init__(self, top=None):
        super().__init__()

        # sidebare
        self.sidebar = sidebar()

        # Bill frame
        self.F_entry_frame = customtkinter.CTkFrame(window)
        self.F_entry_frame.grid(row=0, column=1, columnspan=4, rowspan=4, sticky="nsew")
        self.F_entry_frame.grid_columnconfigure(4, weight=1) 

        self.responsable_label = customtkinter.CTkLabel(self.F_entry_frame, text="Responsable", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.responsable_label.grid(row=0, column=1, padx=(15, 0), pady=(20, 20))
        self.responsable_entry = customtkinter.CTkEntry(self.F_entry_frame, width=200, height=15)
        self.responsable_entry.grid(row=0, column=2, padx=(15, 0), pady=(20, 20))

        self.button = customtkinter.CTkButton(self.F_entry_frame, text="Imprimer", fg_color='gray', font=customtkinter.CTkFont(size=15, weight="bold"), command=F_imprimer)
        self.button.grid(row=4, column=2, padx=(15, 0), pady=(20, 20))

        self.bill = tkst.ScrolledText(self.F_entry_frame, bg='white')
        self.bill.grid(row=0, column=4, rowspan=8, padx=(15, 0), pady=(20, 20))


    def destroy_oFacture(self):
        for widget in window.winfo_children():
            widget.destroy()


class ouvrire_bon:
    def __init__(self, top=None):
        super().__init__()

        # sidebare
        self.sidebar = sidebar()

        # Bill frame
        self.F_entry_frame = customtkinter.CTkFrame(window)
        self.F_entry_frame.grid(row=0, column=1, columnspan=4, rowspan=4, sticky="nsew")
        self.F_entry_frame.grid_columnconfigure(4, weight=1) 

        self.client_label = customtkinter.CTkLabel(self.F_entry_frame, text="Client", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.client_label.grid(row=0, column=1, padx=(15, 0), pady=(20, 20))
        self.client_entry = customtkinter.CTkEntry(self.F_entry_frame, width=200, height=15)
        self.client_entry.grid(row=0, column=2, padx=(15, 0), pady=(20, 20))

        self.button = customtkinter.CTkButton(self.F_entry_frame, text="Imprimer", fg_color='gray', font=customtkinter.CTkFont(size=15, weight="bold"), command=b_imprimer)
        self.button.grid(row=4, column=2, padx=(15, 0), pady=(20, 20))

        self.bill = tkst.ScrolledText(self.F_entry_frame, bg='white')
        self.bill.grid(row=0, column=4, rowspan=8, padx=(15, 0), pady=(20, 20))


    def destroy_obon(self):
        for widget in window.winfo_children():
            widget.destroy()  


class devie_entry:
    def __init__(self) -> None:
        super().__init__()

        # sidebare
        self.sidebar = sidebar()

        # entry frame
        self.entry_frame = customtkinter.CTkFrame(window)
        self.entry_frame.grid(row=0, column=1, columnspan=4, rowspan=4, sticky="nsew")
        self.entry_frame.grid_columnconfigure(4, weight=1) 

        self.client_label = customtkinter.CTkLabel(self.entry_frame, text="Client", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.client_label.grid(row=0, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.client_entry = customtkinter.CTkEntry(self.entry_frame, width=500, border_width=2, corner_radius=10)
        self.client_entry.grid(row=0, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.voiture_label = customtkinter.CTkLabel(self.entry_frame, text="Voiture", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.voiture_label.grid(row=1, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.voiture_entry = customtkinter.CTkEntry(self.entry_frame, width=500, border_width=2, corner_radius=10)
        self.voiture_entry.grid(row=1, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.modele_label = customtkinter.CTkLabel(self.entry_frame, text="Modele", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.modele_label.grid(row=2, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.modele_entry = customtkinter.CTkEntry(self.entry_frame, width=500, border_width=2, corner_radius=10)
        self.modele_entry.grid(row=2, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.matricule_label = customtkinter.CTkLabel(self.entry_frame, text="Matricule", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.matricule_label.grid(row=3, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.matricule_entry = customtkinter.CTkEntry(self.entry_frame, width=500, border_width=2, corner_radius=10)
        self.matricule_entry.grid(row=3, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.km_label = customtkinter.CTkLabel(self.entry_frame, text="Kilometrage", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.km_label.grid(row=4, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.km_entry = customtkinter.CTkEntry(self.entry_frame, width=500, border_width=2, corner_radius=10)
        self.km_entry.grid(row=4, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.tp_label = customtkinter.CTkLabel(self.entry_frame, text="Telephone", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.tp_label.grid(row=5, column=0, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.tp_entry = customtkinter.CTkEntry(self.entry_frame, width=500, border_width=2, corner_radius=10)
        self.tp_entry.grid(row=5, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.save_client = customtkinter.CTkButton(self.entry_frame, text="Valider", font=customtkinter.CTkFont(size=15, weight="bold"), command=add_devie)
        self.save_client.grid(row=6, column=0, padx=(20, 0), pady=(10, 10))

        
    def destroy_enry_D(self):
        for widget in window.winfo_children():
            widget.destroy()


class devie_window:
    def __init__(self, top=None):
        super().__init__()

        self.liste = liste()
        # sidebare
        self.sidebar = sidebar()

        # Bill frame
        self.F_entry_frame = customtkinter.CTkFrame(window)
        self.F_entry_frame.grid(row=0, column=1, columnspan=4, rowspan=4, sticky="nsew")
        self.F_entry_frame.grid_columnconfigure(4, weight=1) 

        self.dg_label = customtkinter.CTkLabel(self.F_entry_frame, text="disignation", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.dg_label.grid(row=0, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.dg_entry = customtkinter.CTkEntry(self.F_entry_frame, width=200, height=15)
        self.dg_entry.grid(row=0, column=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.referance_label = customtkinter.CTkLabel(self.F_entry_frame, text="Referance", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.referance_label.grid(row=1, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.referance_entry = customtkinter.CTkComboBox(self.F_entry_frame, values=self.liste, width=200, height=15)
        self.referance_entry.grid(row=1, column=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.prix_label = customtkinter.CTkLabel(self.F_entry_frame, text="Prix unite", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.prix_label.grid(row=2, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.prix_entry = customtkinter.CTkEntry(self.F_entry_frame, width=200, height=15)
        self.prix_entry.grid(row=2, column=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.quantite_label = customtkinter.CTkLabel(self.F_entry_frame, text="Quantite", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.quantite_label.grid(row=3, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.quantite_entry = customtkinter.CTkEntry(self.F_entry_frame, width=200, height=15)
        self.quantite_entry.grid(row=3, column=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.button = customtkinter.CTkButton(self.F_entry_frame, text="ajouter", fg_color='gray', font=customtkinter.CTkFont(size=15, weight="bold"), command=devie_product)
        self.button.grid(row=4, column=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.button = customtkinter.CTkButton(self.F_entry_frame, text="Total", fg_color='gray', font=customtkinter.CTkFont(size=15, weight="bold"), command=total_devie)
        self.button.grid(row=5, column=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.button = customtkinter.CTkButton(self.F_entry_frame, text="Sauvgarder", fg_color='gray', font=customtkinter.CTkFont(size=15, weight="bold"), command=save_devie)
        self.button.grid(row=6, column=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.button = customtkinter.CTkButton(self.F_entry_frame, text="Initialiser", fg_color='gray', font=customtkinter.CTkFont(size=15, weight="bold"), command=D_Initialiser)
        self.button.grid(row=7, column=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.bill = tkst.ScrolledText(self.F_entry_frame, bg='white')
        self.bill.grid(row=0, column=4, rowspan=8, padx=(20, 0))
        self.referance_entry.set('')
        self.referance_entry.bind('<KeyRelease>', search)

        
    def destroy_devie(self):
        for widget in window.winfo_children():
            widget.destroy()




l2 = []

global_frame = menu()
window.mainloop()