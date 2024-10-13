import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
public class Server {
    public static void main(String[] args) throws IOException {
        ServerSocket serverSocket = new ServerSocket(12345);
        System.out.println("Server waiting for client on port 12345...");
        Socket clientSocket = serverSocket.accept();
        System.out.println("Client connected: " + clientSocket.getInetAddress());
        // Set up input and output streams
        BufferedReader in = new BufferedReader(new
        InputStreamReader(clientSocket.getInputStream()));
        PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);
        new Thread(() -> {
            try {
                String receivedMessage;
                while ((receivedMessage = in.readLine()) != null) {
                    System.out.println("Client: " + receivedMessage);
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }).start();
        BufferedReader userInputReader = new BufferedReader(new
        InputStreamReader(System.in));
        String userInput;
        while ((userInput = userInputReader.readLine()) != null) {
            out.println(userInput);
        }
        userInputReader.close();
        clientSocket.close();
        serverSocket.close();
    }
}