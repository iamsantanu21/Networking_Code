import java.io.*;
import java.net.*;

public class Client {
    public static void main(String[] args) {
        String host = "127.0.0.1"; // Server address
        int port = 5085;

        try (Socket socket = new Socket(host, port);
             BufferedReader input = new BufferedReader(new InputStreamReader(System.in));
             BufferedReader serverInput = new BufferedReader(new InputStreamReader(socket.getInputStream()));
             PrintWriter output = new PrintWriter(socket.getOutputStream(), true)) {

            // Get email and password from user
            System.out.print("Enter email: ");
            String email = input.readLine();

            System.out.print("Enter password: ");
            String password = input.readLine();

            // Send credentials to server
            output.println(email + "," + password);

            // Read server response
            String response = serverInput.readLine();
            System.out.println("Server Response: " + response);

            // If the password was incorrect, keep asking until successful login
            while (response.equals("Incorrect password. Please try again.")) {
                System.out.print("Enter password again: ");
                password = input.readLine();
                output.println(password);
                response = serverInput.readLine();
                System.out.println("Server Response: " + response);
            }

        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }
}