import socket


class TicTacToeServer:
    def __init__(self, port=12000):
        self.port = port #self.port = 12000
        self.board = [' ' for _ in range(9)] #creates a list which is initialized to ' ' from 0 to 8 (9 elements in total)
        self.server_socket = None

    #The print_board method prints the current state of the board
    def print_board(self): #a function to print the board
        print("\nCurrent board:")
        print(" -------------")
        for i in range(0, 9, 3):
            print(f" | {self.board[i]} | {self.board[i+1]} | {self.board[i+2]} | ")
            if i < 6:
                print(" -------------")
        print(" -------------")


    #The check_winner method checks if there is a winner or a tie
    def check_winner(self): 
        # Define win combinations
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  
            [0, 3, 6], [1, 4, 7], [2, 5, 8], 
            [0, 4, 8], [2, 4, 6] 
        ]

        for combo in win_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                return self.board[combo[0]]

        if ' ' not in self.board:
            return 'Tie'

        return None

    #The setup_server method creates a socket and listens for a client request
    def setup_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #setting up a TCP Socket
        self.server_socket.bind(('', self.port))
        self.server_socket.listen(1) #listening for a client request
        print('Tic-Tac-Toe Server is ready to play!')

    #The handle_client_move method waits for the client's move and updates the board accordingly
    def handle_client_move(self, connection_socket):
        while True:
            try:
                self.print_board()
                client_move = connection_socket.recv(1024).decode()
                client_move = int(client_move)
                
                if(0 <= client_move <=8 and self.board[client_move]==' '):
                    self.board[client_move] = 'X'
                    break
                else:
                    error_msg = "Invalid move. Please enter a number between 1 and 9 for an empty space"
                    connection_socket.send(error_msg.encode())
                    continue
                
            except ValueError:
                error_msg="Invalid move. Please enter a digit"
                connection_socket.send(error_msg.encode())
        self.print_board()

    #The make_server_move method asks the server to enter a move and updates the board accordingly
    def make_server_move(self):
        while True:
            try:
                server_move = int(input("Enter your move (1-9): ")) - 1
                if 0 <= server_move <= 8 and self.board[server_move] == ' ':
                    self.board[server_move] = 'O'
                    break
                else:
                    print("Invalid move. Please enter a number between 1 and 9 for an empty space.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        self.print_board() # Display the board after a server's move
        return server_move

    #The play_game method starts the game and alternates between the client and server moves
    def play_game(self, connection_socket):
        self.board = [' ' for _ in range(9)]
        game_over = False

        while not game_over:
            print("Waiting for client's move...")
            self.handle_client_move(connection_socket)

            winner = self.check_winner()
            win_msg = ''

            if(winner == 'X'):
                win_msg = "You win"
            elif winner == 'O':
                win_msg = "Server wins"
            elif winner == 'Tie':
                win_msg = "Tie!"
            
            if(winner != None):
                game_over = True
                connection_socket.send(win_msg.encode())
            

            if not game_over:
                server_move = self.make_server_move()
                winner = self.check_winner()
                win_msg = ''
                if(winner == 'X'):
                    win_msg = "You win"
                elif winner == 'O':
                    win_msg = "Server wins"
                elif winner == 'Tie':
                    win_msg = "Tie!"
                else:
                    win_msg = str(server_move)

                if(winner != None):
                    game_over = True
            
                connection_socket.send(win_msg.encode())

               

    def run(self):
        self.setup_server()
        while True:
            connection_socket, addr = self.server_socket.accept()
            print(f"Game started with {addr}")
            self.play_game(connection_socket)
            play_again = connection_socket.recv(1024).decode()
            if play_again.lower() != 'yes':
                break
            connection_socket.close()
        self.server_socket.close()

if __name__ == "__main__":
    server = TicTacToeServer()
    server.run()