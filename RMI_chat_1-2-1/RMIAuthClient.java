import java.rmi.Naming;
import java.util.Scanner;

public class RMIAuthClient {
    public static void main(String[] args) {
        try {
            AuthService authService = (AuthService) Naming.lookup("rmi://localhost:9080/AuthService");

            @SuppressWarnings("resource")
            Scanner scanner = new Scanner(System.in);
            System.out.print("Enter email: ");
            String email = scanner.nextLine();
            System.out.print("Enter password: ");
            String password = scanner.nextLine();

            String response = authService.verifyCredentials(email, password);
            System.out.println("Server Response: " + response);

            if ("Login Successful".equals(response)) {
                ClientInterface client = new ClientImpl(email);
                authService.registerClient(email, client);

                // Start chat thread
                new Thread(() -> {
                    while (true) {
                        try {
                            System.out.print("Enter recipient email: ");
                            String recipient = scanner.nextLine();
                            System.out.print("Enter message: ");
                            String message = scanner.nextLine();
                            authService.sendMessage(email, recipient, message);
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                    }
                }).start();

                // Keep the main thread alive
                System.out.println("You can now send messages. Type your input below:");
                while (true) {
                    // Keep main thread running to prevent abrupt exit
                    Thread.sleep(1000);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
