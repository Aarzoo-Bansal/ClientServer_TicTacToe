import socket
import sys

class TicTacToeClient:
    def __init__(self, server_name='127.0.0.1', server_port=12000):
        self.server_name = server_name
        self.server_port = server_port
        self.client_socket = None
        self.board = [' ' for _ in range(9)]

    #The TicTacToe board is defined as an !D array of 9 elements, where each element is either 'X', 'O', or ' ' (empty space)
    def print_board(self):
        print("\nCurrent board:")
        print(" -------------")
        for i in range(0, 9, 3):
            print(f" | {self.board[i]} | {self.board[i+1]} | {self.board[i+2]} | ")
            if i < 6:
                print(" -------------")
        print(" -------------")

    #The connect_to_server method creates a socket and connects to the server
    def connect_to_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(20) 
        try:
            self.client_socket.connect((self.server_name, self.server_port))
        except socket.error as e:
            print(f"Failed to connect to server: {e}")
            sys.exit(1)


    #The get_player_move method asks the player to enter a move and returns the move
    def get_player_move(self):
        while True:
            try:
                client_move = int(input("Enter your move between 1 - 9: ")) - 1
              
                if 0 <= client_move <= 8 and self.board[client_move] == ' ':
                    return client_move
                else:
                    print('Invalid input. Please choose an Empty Space between 1 - 9')
            except ValueError:
                print('Invalid input. Please enter a number between 1-9')
        

    #The make_move method gets the player's move and sends it to the server
    def make_move(self):
        move = self.get_player_move()
        self.client_socket.send(str(move).encode())
        self.board[move] = 'X'
        self.print_board()
        return move

    #The handle_server_response method waits for the server's response and updates the board accordingly
    def handle_server_response(self):
        print("Waiting for server's move...")
        server_response = self.client_socket.recv(1024).decode()
     
        if server_response == "You win" or server_response == "Server wins" or server_response == "Tie!":
            print(server_response)
            return True
        else:
            sub_string = "Invalid move"
            if server_response.find(sub_string) != -1:
                self.make_move()
            else:
                server_response = int(server_response)
                self.board[server_response] = 'O'
            self.print_board()
            return False

        
    #The play_game method is the main method that plays the game
    def play_game(self):
        game_over = False
        while not game_over:
            self.print_board()
            self.make_move()
            game_over = self.handle_server_response()
    
    def run(self):
        self.connect_to_server()
        self.play_game()
        self.client_socket.close()
        print("Game over. Connection closed.")

if __name__ == "__main__":
    client = TicTacToeClient()
    client.run()


