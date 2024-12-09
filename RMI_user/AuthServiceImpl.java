import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.sql.*;

public class AuthServiceImpl extends UnicastRemoteObject implements AuthService {
    private static final String DB_URL = "jdbc:mysql://localhost:3306/userdb"; // Database URL
    private static final String DB_USER = "root"; // MySQL username
    private static final String DB_PASSWORD = "Sm210899@"; // MySQL password

    public AuthServiceImpl() throws RemoteException {
        super();
    }

    // Verify if email exists and password matches
    public String verifyCredentials(String email, String password) {
        // Check if email exists
        boolean emailExists = false;
        boolean passwordCorrect = false;
        
        try (Connection connection = DriverManager.getConnection(DB_URL, DB_USER, DB_PASSWORD)) {
            // Query to check if email exists
            String emailQuery = "SELECT * FROM users WHERE email = ?";
            try (PreparedStatement emailStatement = connection.prepareStatement(emailQuery)) {
                emailStatement.setString(1, email);

                try (ResultSet emailResultSet = emailStatement.executeQuery()) {
                    if (emailResultSet.next()) {
                        emailExists = true; // Email exists
                        
                        // If email exists, check password
                        String passwordQuery = "SELECT * FROM users WHERE email = ? AND password = ?";
                        try (PreparedStatement passwordStatement = connection.prepareStatement(passwordQuery)) {
                            passwordStatement.setString(1, email);
                            passwordStatement.setString(2, password);

                            try (ResultSet passwordResultSet = passwordStatement.executeQuery()) {
                                if (passwordResultSet.next()) {
                                    passwordCorrect = true; // Password matches
                                }
                            }
                        }
                    }
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }

        if (!emailExists) {
            return "Email doesn't exist";
        } else if (!passwordCorrect) {
            return "Wrong password. Try again";
        } else {
            return "Login Successful"; // Credentials are correct
        }
    }

    @Override
    public boolean verifyEmail(String email) throws RemoteException {
        throw new UnsupportedOperationException("Unimplemented method 'verifyEmail'");
    }

    @Override
    public boolean verifyPassword(String email, String password) throws RemoteException {
        throw new UnsupportedOperationException("Unimplemented method 'verifyPassword'");
    }
}
