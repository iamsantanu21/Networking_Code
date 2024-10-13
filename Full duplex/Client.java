import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class Client {
    public static void main(String[] args) {
        try {
            // Connect to the server on localhost at port 12345
            Socket socket = new Socket("localhost", 12345);

            // Set up input and output streams
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);

            // Start a new thread to listen for messages from the server
            new Thread(() -> {
                try {
                    String receivedMessage;
                    while ((receivedMessage = in.readLine()) != null) {
                        System.out.println("Server: " + receivedMessage);
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }).start();

            // Read user input and send it to the server
            BufferedReader userInputReader = new BufferedReader(new InputStreamReader(System.in));
            String userInput;
            while ((userInput = userInputReader.readLine()) != null) {
                out.println(userInput);
            }

            // Close resources
            userInputReader.close();
            socket.close();

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
