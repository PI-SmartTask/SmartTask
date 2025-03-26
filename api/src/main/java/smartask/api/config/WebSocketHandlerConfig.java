package smartask.api.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import smartask.api.event.TaskStatusWebSocketHandler;

@Configuration
public class WebSocketHandlerConfig {

    @Bean
    public TaskStatusWebSocketHandler taskStatusWebSocketHandler() {
        return new TaskStatusWebSocketHandler();
    }
}
