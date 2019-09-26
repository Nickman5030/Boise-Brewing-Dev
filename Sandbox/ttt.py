import tkinter as tk
from tkinter import messagebox

player_a_victory = None
player_b_victory = None

b_turn = True
flag = 0
button_grid = list()

def play():
    global player_a_victory, player_b_victory

    root = tk.Tk()
    root.title("Tic Tac Toe")
    player_a_victory = tk.StringVar()
    player_b_victory = tk.StringVar()

    # Entry for player info
    p1_name = tk.StringVar()
    p2_name = tk.StringVar()
    p1_name_entry = tk.Entry(root, textvariable=p1_name, bd=5)
    p2_name_entry = tk.Entry(root, textvariable=p2_name, bd=5)
    p1_name_entry.grid(row=1, column=1, columnspan=8)
    p2_name_entry.grid(row=2, column=1, columnspan=8)

    # Set up player info display
    label = tk.Label(root, text="Player 1:", font='Times 20 bold', bg='white', fg='black', height=1, width=8)
    label.grid(row=1, column=0)

    label = tk.Label(root, text="Player 2:", font='Times 20 bold', bg='white', fg='black', height=1, width=8)
    label.grid(row=2, column=0)
    
    # Set up the 3x3 grid of buttons
    button1 = tk.Button(root, text=" ", font='Times 20 bold', bg='gray', fg='white', height=4, width=8,
                     command=lambda: button_click(button1, p1_name, p2_name))
    button1.grid(row=3, column=0)

    button2 = tk.Button(root, text=' ', font='Times 20 bold', bg='gray', fg='white', height=4, width=8,
                     command=lambda: button_click(button2, p1_name, p2_name))
    button2.grid(row=3, column=1)

    button3 = tk.Button(root, text=' ', font='Times 20 bold', bg='gray', fg='white', height=4, width=8,
                     command=lambda: button_click(button3, p1_name, p2_name))
    button3.grid(row=3, column=2)
    
    # Add first row of buttons to grid
    button_grid.append([button1, button2, button3])

    button4 = tk.Button(root, text=' ', font='Times 20 bold', bg='gray', fg='white', height=4, width=8,
                     command=lambda: button_click(button4, p1_name, p2_name))
    button4.grid(row=4, column=0)

    button5 = tk.Button(root, text=' ', font='Times 20 bold', bg='gray', fg='white', height=4, width=8,
                     command=lambda: button_click(button5, p1_name, p2_name))
    button5.grid(row=4, column=1)

    button6 = tk.Button(root, text=' ', font='Times 20 bold', bg='gray', fg='white', height=4, width=8,
                     command=lambda: button_click(button6, p1_name, p2_name))
    button6.grid(row=4, column=2)

    # Add second row of buttons to grid
    button_grid.append([button4, button5, button6])

    button7 = tk.Button(root, text=' ', font='Times 20 bold', bg='gray', fg='white', height=4, width=8,
                     command=lambda: button_click(button7, p1_name, p2_name))
    button7.grid(row=5, column=0)

    button8 = tk.Button(root, text=' ', font='Times 20 bold', bg='gray', fg='white', height=4, width=8,
                     command=lambda: button_click(button8, p1_name, p2_name))
    button8.grid(row=5, column=1)

    button9 = tk.Button(root, text=' ', font='Times 20 bold', bg='gray', fg='white', height=4, width=8,
                     command=lambda: button_click(button9, p1_name, p2_name))
    button9.grid(row=5, column=2)

    # Add final row of buttons to grid
    button_grid.append([button7, button8, button9])
    
    # Run the game
    root.mainloop()


def button_click(button, p1_name, p2_name):
    """
        Handles the clicking of a button

    :param button: The button that was clicked
    :param p1_name: Name of player 1
    :param p2_name: Name of player 2
    :return: None
    """
    # I'm not a fan of globals but this is necessary in this case
    global b_turn, flag, button_grid

    if button["text"] == " " and b_turn == True:
        button["text"] = "X"
        b_turn = False
        player_b_victory.set(p2_name.get() + " Wins!")
        player_a_victory.set(p1_name.get() + " Wins!")
        check_for_win()
        flag += 1


    elif button["text"] == " " and b_turn == False:
        button["text"] = "O"
        b_turn = True
        check_for_win()
        flag += 1
    else:
        messagebox.showinfo("Tic-Tac-Toe", "Button already Clicked!")


def check_for_win():
    if (button_grid[0][0]['text'] == 'X' and button_grid[0][1]['text'] == 'X' and button_grid[0][2]['text'] == 'X' or
                        button_grid[1][0]['text'] == 'X' and button_grid[1][1]['text'] == 'X' and button_grid[1][2]['text'] == 'X' or
                        button_grid[2][0]['text'] == 'X' and button_grid[2][1]['text'] == 'X' and button_grid[2][2]['text'] == 'X' or
                        button_grid[0][0]['text'] == 'X' and button_grid[1][1]['text'] == 'X' and button_grid[2][2]['text'] == 'X' or
                        button_grid[0][2]['text'] == 'X' and button_grid[1][1]['text'] == 'X' and button_grid[2][0]['text'] == 'X' or
                        button_grid[0][0]['text'] == 'X' and button_grid[0][1]['text'] == 'X' and button_grid[0][2]['text'] == 'X' or
                        button_grid[0][0]['text'] == 'X' and button_grid[1][0]['text'] == 'X' and button_grid[2][0]['text'] == 'X' or
                        button_grid[0][1]['text'] == 'X' and button_grid[1][1]['text'] == 'X' and button_grid[2][1]['text'] == 'X' or
                        button_grid[2][0]['text'] == 'X' and button_grid[1][2]['text'] == 'X' and button_grid[2][2]['text'] == 'X'):
        disable_buttons()
        messagebox.showinfo("Tic-Tac-Toe", player_a_victory.get())

    elif (flag == 8):
        messagebox.showinfo("Tic-Tac-Toe", "It is a Tie")

    elif (button_grid[0][0]['text'] == 'O' and button_grid[0][1]['text'] == 'O' and button_grid[0][2]['text'] == 'O' or
                          button_grid[1][0]['text'] == 'O' and button_grid[1][1]['text'] == 'O' and button_grid[1][2]['text'] == 'O' or
                          button_grid[2][0]['text'] == 'O' and button_grid[2][1]['text'] == 'O' and button_grid[2][2]['text'] == 'O' or
                          button_grid[0][0]['text'] == 'O' and button_grid[1][1]['text'] == 'O' and button_grid[2][2]['text'] == 'O' or
                          button_grid[0][2]['text'] == 'O' and button_grid[1][1]['text'] == 'O' and button_grid[2][0]['text'] == 'O' or
                          button_grid[0][0]['text'] == 'O' and button_grid[0][1]['text'] == 'O' and button_grid[0][2]['text'] == 'O' or
                          button_grid[0][0]['text'] == 'O' and button_grid[1][0]['text'] == 'O' and button_grid[2][0]['text'] == 'O' or
                          button_grid[0][1]['text'] == 'O' and button_grid[1][1]['text'] == 'O' and button_grid[2][1]['text'] == 'O' or
                          button_grid[2][0]['text'] == 'O' and button_grid[1][2]['text'] == 'O' and button_grid[2][2]['text'] == 'O'):
        disable_buttons()
        messagebox.showinfo("Tic-Tac-Toe", player_b_victory.get())


def disable_buttons():
    for row in button_grid:
        for col in row:
            col.configure(state="disabled")


if __name__ == "__main__":
    play()