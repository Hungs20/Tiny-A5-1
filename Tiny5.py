# coding=utf-8
import string
import tkinter as tk
from tkinter import *
from tkinter import messagebox

plain_text = ""
cipher_text = ""

def create_ui():
    window = Tk()
    window.geometry('600x400')
    window.title("Tiny A5/1")
    
    title = Label(window, text = "Tiny A5/1", bg="orange", width=300, height=3)
    title.config(font =("Courier", 30))
    title.pack()

    row = Frame(window)
    lbl_key = Label(row, text="", width = 10)
    lbx_bit = Label(row, text="6 bit", width = 15)
    lby_bit = Label(row, text="8 bit", width = 20)
    lbz_bit = Label(row, text="9 bit", width = 20)

    row.pack(side = TOP, padx = 5 , pady = 5)
    lbl_key.pack(side = LEFT)
    lbx_bit.pack(side = LEFT)
    lby_bit.pack(side = LEFT)
    lbz_bit.pack(side = RIGHT)

    row2 = Frame(window)
    lbl_key = Label(row2, text="Key", width = 10)
    keyX = Entry(row2,width=15)
    keyY = Entry(row2,width=20)
    keyZ = Entry(row2,width=20)
    row2.pack(side = TOP, padx = 5 , pady = 5)
    lbl_key.pack(side = LEFT)
    keyX.pack(side = LEFT)
    keyY.pack(side = LEFT)
    keyZ.pack(side = RIGHT)

    row3 = Frame(window)
    lbl = Label(row3, text="Plain", width = 10)
    txt = Entry(row3,width=60)
    row3.pack(side = TOP, padx = 5 , pady = 5)
    lbl.pack(side = LEFT)
    txt.pack(side = RIGHT, expand = YES)

    row4 = Frame(window)
    lbl = Label(row4, text="Cipher", width = 10)
    cipher = Entry(row4,width=60)
    row4.pack(side = TOP, padx = 5 , pady = 5)
    lbl.pack(side = LEFT)
    cipher.pack(side = RIGHT, expand = YES)

    def encrypt_btn_press():

        plain_text = txt.get()
        key_x_str = keyX.get()
        key_y_str = keyY.get()
        key_z_str = keyZ.get()
        if plain_text == "" or key_x_str == "" or key_y_str == "" or key_z_str == "":
            messagebox.showerror('Lỗi', 'Vui lòng nhập đủ dữ liệu')
            return
        if len(key_x_str) < 6 or len(key_y_str) < 8 or len(key_z_str) < 9:
            messagebox.showerror('Lỗi', 'Độ dài key không chính xác')
            return
        try:
            key_x = [int(x) for x in key_x_str]
            key_y = [int(x) for x in key_y_str]
            key_z = [int(x) for x in key_z_str]
        except:
            messagebox.showerror('Lỗi', 'Key phải là dãy nhị phân')
            return
        try:
            result = encrypt(plain_text, key_x, key_y, key_z)
            cipher.delete(0,END)
            cipher.insert(0,result)
        except:
            messagebox.showerror('Lỗi', 'Không thể mã hóa')
            return
    
    def decrypt_btn_press():
        cipher_text = cipher.get()
        key_x_str = keyX.get()
        key_y_str = keyY.get()
        key_z_str = keyZ.get()
        if cipher_text == "" or key_x_str == "" or key_y_str == "" or key_z_str == "":
            messagebox.showerror('Lỗi', 'Vui lòng nhập đủ dữ liệu')
            return
        if len(key_x_str) < 6 or len(key_y_str) < 8 or len(key_z_str) < 9:
            messagebox.showerror('Lỗi', 'Độ dài key không chính xác')
            return
        try:
            key_x = [int(x) for x in key_x_str]
            key_y = [int(x) for x in key_y_str]
            key_z = [int(x) for x in key_z_str]
        except:
            messagebox.showerror('Lỗi', 'Key phải là dãy nhị phân')
            return
        try:
            result = decrypt(cipher_text, key_x, key_y, key_z)
            txt.delete(0,END)
            txt.insert(0,result)
        except:
            messagebox.showerror('Lỗi', 'Không thể giải mã')
            return
        return
    
    row5 = Frame(window)
    btn_encrypt = Button(row5, text="Encrypt", command=encrypt_btn_press, width = 20, height = 2)
    btn_decrypt = Button(row5, text="Decrypt", command=decrypt_btn_press, width = 20, height = 2)
    row5.pack(side = TOP, padx = 5 , pady = 5)
    btn_encrypt.pack(side = LEFT)
    btn_decrypt.pack(side = RIGHT)

    auth = Label(window, text="Author: Chu Van Hung")
    auth.config(font =("Courier", 11), fg="red")
    auth.pack(side = BOTTOM, anchor=SE)
    window.mainloop()

def get_binary(plain):
    s = ""
    i = 0
    for i in plain:
        binary = str(' '.join(format(ord(x), 'b') for x in i))
        j = len(binary)
        s = binary
        while(j < 8):
            binary = "0" + binary
            s = binary
            j = j + 1
    binary_values = []
    k = 0
    while(k < len(s)):
        binary_values.insert(k, int(s[k]))
        k = k + 1
    return binary_values
def convert_bin_to_string(binary):
    s = ""
    res = 0
    binary = reversed(binary)
    for x,j in enumerate(binary):
        res += j<<x
    return chr(res)
def get_maj(x, y, z):
    if(x + y + z > 1):
        return 1
    else:
        return 0

def rotate(bits):
    res = 0
    for bit in bits:
        res ^= bit
    return res

def get_keystream(length, key_x, key_y, key_z):
    s = [0 for i in range(length)]
    x = key_x.copy()
    y = key_y.copy()
    z = key_z.copy()
    for i in range(length):
        m = get_maj(x[1], y[3], z[3])
        if m == x[1]:
            t = rotate([x[2], x[4], x[5]])
            for j in range(len(x) - 1, 0, -1):
                x[j] = x[j-1]
            x[0] = t
        if m == y[3]:
            t = rotate([y[6], y[7]])
            for j in range(len(y) - 1, 0, -1):
                y[j] = y[j-1]
            y[0] = t
        if m == z[3]:
            t = rotate([z[2], z[7], z[8]])
            for j in range(len(z) - 1, 0, -1):
                z[j] = z[j-1]
            z[0] = t
        s[i] = x[5] ^ y[7] ^ z[8]
    return s
def encrypt(plain, key_x, key_y, key_z):
    result = ""
    for char in plain:
        p = get_binary(char)
        s = get_keystream(len(p), key_x, key_y, key_z)
        c = list(s[i] ^ p[i] for i in range(len(s)))
        result += convert_bin_to_string(c)
    return result
def decrypt(cipher, key_x, key_y, key_z):
    result = ""
    for char in cipher:
        p = get_binary(char)
        s = get_keystream(len(p), key_x, key_y, key_z)
        c = list(s[i] ^ p[i] for i in range(len(s)))
        result += convert_bin_to_string(c)
    return result
    
if __name__ == "__main__":
    create_ui()