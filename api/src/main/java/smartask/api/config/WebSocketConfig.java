package smartask.api.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.socket.config.annotation.EnableWebSocket;
import org.springframework.web.socket.config.annotation.WebSocketConfigurer;
import org.springframework.web.socket.config.annotation.WebSocketHandlerRegistry;
import smartask.api.event.TaskStatusWebSocketHandler;

@Configuration
@EnableWebSocket
public class WebSocketConfig implements WebSocketConfigurer {

    @Override
    public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
        // Define the WebSocket endpoint
        registry.addHandler(new TaskStatusWebSocketHandler(), "/task-status")
                .setAllowedOrigins("*");  // Allow any origin (adjust for security in production)
    }
}
