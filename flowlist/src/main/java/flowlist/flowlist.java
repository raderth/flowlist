package flowlist;

import com.google.gson.Gson;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;
import org.bukkit.Bukkit;
import org.bukkit.configuration.file.FileConfiguration;
import org.bukkit.plugin.java.JavaPlugin;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.util.stream.Collectors;

public class flowlist extends JavaPlugin {

    private static final int DEFAULT_PORT = 8080;
    private HttpServer server;
    private String secret;
    private int port;

    @Override
    public void onEnable() {
        saveDefaultConfig();
        loadConfig();

        if (secret == null || secret.isEmpty() || secret.length() != 16) {
            getLogger().severe("Secret in config.yml must be exactly 16 characters long. Please set it and restart the server.");
            Bukkit.getPluginManager().disablePlugin(this);
            return;
        }

        try {
            startServer();
            getLogger().info("flowlist plugin has been enabled!");
        } catch (IOException e) {
            getLogger().severe("Failed to start the HTTP server: " + e.getMessage());
            Bukkit.getPluginManager().disablePlugin(this);
        }
    }

    @Override
    public void onDisable() {
        if (server != null) {
            server.stop(0);
        }
        getLogger().info("flowlist plugin has been disabled!");
    }

    private void loadConfig() {
        FileConfiguration config = getConfig();
        secret = config.getString("secret");
        port = config.getInt("port", DEFAULT_PORT);
    }

    private void startServer() throws IOException {
        server = HttpServer.create(new InetSocketAddress(port), 0);
        server.createContext("/execute", new CommandHandler());
        server.setExecutor(null);
        server.start();
        getLogger().info("HTTP server started on port " + port);
    }

    private class CommandHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if (!"POST".equals(exchange.getRequestMethod())) {
                sendResponse(exchange, 405, "Method Not Allowed");
                return;
            }

            String requestBody = new BufferedReader(new InputStreamReader(exchange.getRequestBody(), StandardCharsets.UTF_8))
                    .lines().collect(Collectors.joining("\n"));

            try {
                String decrypted = decrypt(requestBody);
                Gson gson = new Gson();
                CommandRequest request = gson.fromJson(decrypted, CommandRequest.class);

                if (request == null || request.command == null || request.command.isEmpty()) {
                    sendResponse(exchange, 400, "Bad Request");
                    return;
                }

                Bukkit.getScheduler().runTask(flowlist.this, () -> {
                    Bukkit.getServer().dispatchCommand(Bukkit.getConsoleSender(), request.command);
                });

                sendResponse(exchange, 200, "Command executed successfully");
            } catch (Exception e) {
                sendResponse(exchange, 400, "Decryption failed or invalid request");
            }
        }

        private void sendResponse(HttpExchange exchange, int statusCode, String response) throws IOException {
            exchange.sendResponseHeaders(statusCode, response.length());
            try (OutputStream os = exchange.getResponseBody()) {
                os.write(response.getBytes());
            }
        }
    }

    private String decrypt(String encryptedText) throws Exception {
        SecretKeySpec secretKey = new SecretKeySpec(secret.getBytes(StandardCharsets.UTF_8), "AES");
        Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5PADDING");
        cipher.init(Cipher.DECRYPT_MODE, secretKey);
        return new String(cipher.doFinal(Base64.getDecoder().decode(encryptedText)));
    }

    private static class CommandRequest {
        String command;
    }
}