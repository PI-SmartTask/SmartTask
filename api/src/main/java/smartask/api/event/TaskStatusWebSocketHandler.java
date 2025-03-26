package smartask.api.event;

import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;
import org.springframework.web.socket.TextMessage;
import java.util.concurrent.CopyOnWriteArrayList;

public class TaskStatusWebSocketHandler extends TextWebSocketHandler {

    // Track active WebSocket sessions
    private final CopyOnWriteArrayList<WebSocketSession> sessions = new CopyOnWriteArrayList<>();

    @Override
    public void afterConnectionEstablished(WebSocketSession session) throws Exception {
        sessions.add(session);
        System.out.println("New WebSocket connection established.");
    }

    @Override
    public void handleTextMessage(WebSocketSession session, TextMessage message) throws Exception {
        // You can handle incoming messages from clients if needed.
        System.out.println("Received message: " + message.getPayload());
    }

    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus status) throws Exception {
        sessions.remove(session);
        System.out.println("WebSocket connection closed.");
    }

    // Method to send task status update to all connected clients
    public void broadcastTaskStatus(String taskId, String status) {
        TextMessage message = new TextMessage("Task ID: " + taskId + " | Status: " + status);
        for (WebSocketSession session : sessions) {
            try {
                session.sendMessage(message);
            } catch (Exception e) {
                System.err.println("Error sending WebSocket message: " + e.getMessage());
            }
        }
    }
}
