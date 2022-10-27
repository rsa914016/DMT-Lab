from tkinter import *
from scipy.spatial import distance_matrix
import numpy as np


def GetMatrix():
    dic = {"Manhattan Distance": 1,
           "Euclidean Distance": 2,
           "Mahalanobis Distance": 3,
           "Select Any Metric": 2}

    rows = T1.get("1.0", END).splitlines()
    mat = [list(map(int, row.split(' '))) for row in rows]
    # print(mat)
    dist_mat = distance_matrix(mat, mat, p=dic[menu.get()])
    dist_mat = np.round(np.matrix(dist_mat), 2)
    r, c = dist_mat.shape
    T2.delete("1.0", END)
    for i in range(r):
        for j in range(c):
            T2.insert(END, f'{dist_mat[i, j]: 02}  ')
        T2.insert(END, f'\n')


root = Tk()
root.geometry("800x400")
root.title('DISTANCE MATRIX')

menu = StringVar()
menu.set("Select Any Metric")
drop = OptionMenu(root, menu,
                  "Manhattan Distance",
                  "Euclidean Distance",
                  "Mahalanobis Distance")
drop.config(font=("Courier New CE", 18))
drop.pack()
frame = Frame(root)
T1 = Text(frame, height=10, width=22, font=("Courier New CE", 18))
T1.grid(row=0, column=0, padx=10, pady=10)
T2 = Text(frame, height=10, width=22, font=("Courier New CE", 18))
T2.grid(row=0, column=1, pady=10)
button1 = Button(frame, text='Get Matrix', font=("Courier New CE", 18))
button1.config(fg='black', command=GetMatrix)
button1.grid(row=1, column=0, columnspan=5)
frame.pack()
root.mainloop()
