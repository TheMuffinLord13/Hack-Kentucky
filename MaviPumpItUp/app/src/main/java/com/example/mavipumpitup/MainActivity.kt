package com.example.mavipumpitup

import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.Image
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.res.painterResource
import com.example.mavipumpitup.ui.theme.MaviPumpItUpTheme
import kotlinx.coroutines.delay

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MaviPumpItUpTheme {
                SplashScreen()
            }
        }
    }

    @Composable
    fun SplashScreen() {
        // LaunchedEffect ensures this runs once when the Composable is first shown
        LaunchedEffect(Unit) {
            delay(1500) // Wait for 1.5 seconds
            startActivity(Intent(this@MainActivity, ActivityHome::class.java))
            finish() // Finish Splash Activity so user can't go back to it
        }

        // Show the splash image
        Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
            GreetingImage(
                modifier = Modifier.padding(innerPadding)
            )
        }
    }
}

@Composable
fun GreetingImage(modifier: Modifier = Modifier) {
    val image = painterResource(R.drawable.earth_splash)
    Image(
        painter = image,
        contentDescription = null,
        modifier = Modifier.fillMaxSize(),
    )
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    MaviPumpItUpTheme {
        GreetingImage()
    }
}


//package com.example.mavipumpitup
//
//import android.os.Bundle
//import androidx.activity.ComponentActivity
//import androidx.activity.compose.setContent
//import androidx.activity.enableEdgeToEdge
//import androidx.compose.foundation.layout.fillMaxSize
//import androidx.compose.foundation.layout.padding
//import androidx.compose.foundation.Image
//import androidx.compose.material3.Scaffold
//import androidx.compose.material3.Text
//import androidx.compose.runtime.Composable
//import androidx.compose.ui.Modifier
//import androidx.compose.ui.tooling.preview.Preview
//import androidx.compose.ui.res.painterResource
//import com.example.mavipumpitup.ui.theme.MaviPumpItUpTheme
//
//class MainActivity : ComponentActivity() {
//    override fun onCreate(savedInstanceState: Bundle?) {
//        super.onCreate(savedInstanceState)
//        enableEdgeToEdge()
//        setContent {
//            MaviPumpItUpTheme {
//                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
//                    GreetingImage(
//                        modifier = Modifier.padding(innerPadding)
//                    )
//                }
//            }
//        }
//    }
//}
//
//@Composable
//fun GreetingImage(modifier: Modifier = Modifier) {
//    val image = painterResource(R.drawable.earth_splash)
//    Image(
//        painter = image,
//        contentDescription = null,
//        modifier = Modifier.fillMaxSize(),
//    )
//}
//
//@Preview(showBackground = true)
//@Composable
//fun GreetingPreview() {
//    MaviPumpItUpTheme {
//        GreetingImage()
//    }
//}