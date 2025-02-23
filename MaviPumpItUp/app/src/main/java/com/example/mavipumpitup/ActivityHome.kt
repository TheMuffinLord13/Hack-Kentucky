package com.example.mavipumpitup

import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import java.io.BufferedReader
import java.io.InputStreamReader
import java.io.OutputStream
import java.net.Socket
import kotlinx.coroutines.delay

class ActivityHome : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_home)

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        // Example: connect to ESP32's IP address (e.g., 192.168.4.1) on port 1234
        connectToSocket(ipAddress = "ch1246463.flespi.gw", port = 28782)
    }

    private fun connectToSocket(ipAddress: String, port: Int) {
        // Use coroutines to avoid blocking the main thread
        CoroutineScope(Dispatchers.IO).launch {
            try {
                val socket = Socket(ipAddress, port)

                // Get the input/output streams
                val inputStream = socket.getInputStream()
                val outputStream = socket.getOutputStream()
                val reader = BufferedReader(InputStreamReader(inputStream))

                // Example: Send data to the server
                sendData(outputStream, "Hello from Android")

                // Read response (blocking call)
                val response = reader.readLine()

                // Switch to UI thread to update the UI
                runOnUiThread {
                    if (response != null) {
                        Toast.makeText(this@ActivityHome, "Connected! Server says: $response", Toast.LENGTH_LONG).show()
                    } else {
                        Toast.makeText(this@ActivityHome, "Connected but no response received.", Toast.LENGTH_LONG).show()
                    }
                }

//                socket.setKeepAlive(true)

                startHeartbeat(outputStream)
//                // Close the socket
//                socket.close()
            } catch (e: Exception) {
                e.printStackTrace()
                // Show an error message on UI thread
                runOnUiThread {
                    Toast.makeText(this@ActivityHome, "Failed to connect: ${e.message}", Toast.LENGTH_LONG).show()
                }
            }
        }
    }

    private fun startHeartbeat(outputStream: OutputStream) {
        CoroutineScope(Dispatchers.IO).launch {
            while (true) {
                try {
                    sendData(outputStream, "ping")
                    delay(5000) // Send every 5 seconds
                } catch (e: Exception) {
                    e.printStackTrace()
                    runOnUiThread {
                        Toast.makeText(this@ActivityHome, "Connection lost: ${e.message}", Toast.LENGTH_LONG).show()
                    }
                    break // Stop heartbeat if connection is lost
                }
            }
        }
    }

    private fun sendData(outputStream: OutputStream, data: String) {
        outputStream.write((data + "\n").toByteArray())
        outputStream.flush()
    }
}