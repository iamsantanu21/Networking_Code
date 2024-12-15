import java.rmi.Naming;
import java.util.Scanner;

public class ChatClient {
    public static void main(String[] args) {
        try {
            // Lookup the remote object
            ChatService chatService = (ChatService) Naming.lookup("rmi://localhost/ChatService");
            @SuppressWarnings("resource")
            Scanner scanner = new Scanner(System.in);

            while (true) {
                System.out.print("Enter your message (or type 'exit' to quit): ");
                String message = scanner.nextLine();

                if ("exit".equalsIgnoreCase(message)) {
                    break;
                }

                // Call the remote method
                String response = chatService.sendMessage(message);
                System.out.println("Server: " + response);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
