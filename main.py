from Application import *


if __name__ == '__main__':
    app = Application()
    app.mainloop()


if __name__ == '__main2__':
    connection = cx_Oracle.connect(
        user="admin",
        password="admin",
        dsn="DESKTOP-KQ6B5GR:1521/XEPDB1")

    print("Successfully connected to Oracle Database")

    cursor = connection.cursor()

    #for row in cursor.execute('SELECT name, is_admin FROM consumer'):
    #    if row[1]:
    #        print(row[0], "is admin")
    #    else:
    #        print(row[0], "is NOT admin")
    root = Tk()
    root.title('Login')
    root.geometry('925x500+300+200')
    root.configure(bg="#fff")
    root.resizable(False, False)

    img = PhotoImage(file='assets/login.png')
    Label(root, image=img, bg='white').place(x=50, y=50)

    frame = Frame(root, width=350, height=350, bg="white")
    frame.place(x=480, y=70)

    heading = Label(frame, text='Sign in', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
    heading.place(x=100, y=5)

    user = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    user.place(x=30, y=80)
    user.insert(0, 'Username')
    user.bind('<FocusIn>', on_enter_name)
    user.bind('<FocusOut>', on_leave_name)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

    password = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
    password.place(x=30, y=150)
    password.insert(0, 'Password')
    password.bind('<FocusIn>', on_enter_password)
    password.bind('<FocusOut>', on_leave_password)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

    signIn = Button(frame, width=39, pady=7, text='Sign in', bg='#57a1f8', fg='white', border=0, command=sign_in)
    signIn.place(x=35, y=204)
    label = Label(frame, text="Don't have an account?", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
    label.place(x=75, y=270)

    signUp = Button(frame, width=6, text="Sign up", border=0, bg='white', cursor='hand2', fg='#57a1f8')
    signUp.place(x=215, y=270)

    root.mainloop()

