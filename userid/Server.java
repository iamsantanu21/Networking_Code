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
                Socket socket = serverSocket.accept();
                System.out.println("New client connected");

                // Handle client in a separate thread
                new Thread(new ClientHandler(socket)).start();
            }
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }

    // Verify email and password
    public static boolean verifyCredentials(String email, String password) {
        boolean isValid = false;

        try (Connection connection = DriverManager.getConnection(DB_URL, DB_USER, DB_PASSWORD)) {
            String query = "SELECT * FROM users WHERE email = ? AND password = ?";
            PreparedStatement preparedStatement = connection.prepareStatement(query);
            preparedStatement.setString(1, email);
            preparedStatement.setString(2, password);

            ResultSet resultSet = preparedStatement.executeQuery();
            isValid = resultSet.next();
        } catch (SQLException e) {
            e.printStackTrace();
        }

        return isValid;
    }
}

class ClientHandler implements Runnable {
    private final Socket socket;

    public ClientHandler(Socket socket) {
        this.socket = socket;
    }

    @Override
    public void run() {
        try (BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
             PrintWriter output = new PrintWriter(socket.getOutputStream(), true)) {

            String data = input.readLine();
            if (data != null) {
                String[] credentials = data.split(",");
                String email = credentials[0];
                String password = credentials[1];

                if (Server.verifyCredentials(email, password)) {
                    output.println("Login Successful");
                } else {
                    output.println("Invalid Credentials");
                }
            }
        } catch (IOException ex) {
            ex.printStackTrace();
        } finally {
            try {
                socket.close();
            } catch (IOException ex) {
                ex.printStackTrace();
            }
        }
    }
}
