import java.io.*;
import java.net.*;
import java.sql.*;

public class Server {
    private static final String DB_URL = "jdbc:mysql://localhost:3306/userdb"; // Database URL
    private static final String DB_USER = "root"; // Your MySQL username
    private static final String DB_PASSWORD = "Sm210899@"; // Your MySQL password

    public static void main(String[] args) {
        int port = 5050;

        try (ServerSocket serverSocket = new ServerSocket(port)) {
            System.out.println("Server is listening on port " + port);

            while (true) {
                try (Socket socket = serverSocket.accept();
                     BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                     PrintWriter output = new PrintWriter(socket.getOutputStream(), true)) {

                    System.out.println("New client connected");

                    // Read data from client (email and password)
                    String data = input.readLine();
                    if (data != null) {
                        String[] credentials = data.split(",");
                        String email = credentials[0];
                        String password = credentials[1];

                        // Verify email and password
                        if (verifyEmail(email)) {
                            boolean isPasswordCorrect = false;
                            while (!isPasswordCorrect) {
                                if (verifyPassword(email, password)) {
                                    output.println("Login Successful");
                                    isPasswordCorrect = true; // Exit loop on successful login
                                } else {
                                    output.println("Incorrect password. Please try again.");
                                    password = input.readLine(); // Re-prompt for password
                                }
                            }
                        } else {
                            output.println("Email doesn't exist");
                        }
                    }
                } catch (IOException e) {
                    System.out.println("Error handling client: " + e.getMessage());
                }
            }
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }

    // Verify if email exists
    private static boolean verifyEmail(String email) {
        boolean exists = false;

        try (Connection connection = DriverManager.getConnection(DB_URL, DB_USER, DB_PASSWORD)) {
            String query = "SELECT * FROM users WHERE email = ?";
            try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
                preparedStatement.setString(1, email);

                try (ResultSet resultSet = preparedStatement.executeQuery()) {
                    exists = resultSet.next(); // If there is a record, the email exists
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }

        return exists;
    }

    // Verify if the password matches the one for the provided email
    private static boolean verifyPassword(String email, String password) {
        boolean isValid = false;

        try (Connection connection = DriverManager.getConnection(DB_URL, DB_USER, DB_PASSWORD)) {
            String query = "SELECT * FROM users WHERE email = ? AND password = ?";
            try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
                preparedStatement.setString(1, email);
                preparedStatement.setString(2, password);

                try (ResultSet resultSet = preparedStatement.executeQuery()) {
                    isValid = resultSet.next(); // If a record is returned, password is correct
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }

        return isValid;
    }
}
