package com.example.callibri

import androidx.navigation.fragment.findNavController
import android.os.Bundle
import android.view.View
import android.widget.ImageView
import android.widget.TextView
import androidx.core.view.GravityCompat
import com.google.android.material.snackbar.Snackbar
import com.google.android.material.navigation.NavigationView
import androidx.navigation.findNavController
import androidx.navigation.ui.AppBarConfiguration
import androidx.navigation.ui.navigateUp
import androidx.navigation.ui.setupActionBarWithNavController
import androidx.navigation.ui.setupWithNavController
import androidx.drawerlayout.widget.DrawerLayout
import androidx.appcompat.app.AppCompatActivity
import androidx.navigation.NavOptions
import com.example.callibri.databinding.ActivityMainBinding
import com.example.callibri.R
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.net.InetAddress

class MainActivity : AppCompatActivity() {

    private lateinit var appBarConfiguration: AppBarConfiguration
    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)


        var isUserLoggedIn: Boolean = true



        setSupportActionBar(binding.appBarMain.toolbar)

        checkHostReachability()

        binding.appBarMain.fab.setOnClickListener { view ->
            Snackbar.make(view, "", Snackbar.LENGTH_LONG)
                .setAction("Action", null)
                .setAnchorView(R.id.fab).show()
        }
        val drawerLayout: DrawerLayout = binding.drawerLayout
        val navView: NavigationView = binding.navView
        val navController = findNavController(R.id.nav_host_fragment_content_main)
        appBarConfiguration = AppBarConfiguration(
            setOf(
                R.id.nav_home, R.id.nav_gallery, R.id.nav_slideshow, R.id.nav_login, R.id.nav_registration
            ), drawerLayout
        )
        setupActionBarWithNavController(navController, appBarConfiguration)
        navView.setupWithNavController(navController)

        val headerView: View = navView.getHeaderView(0)
        val textView: TextView = headerView.findViewById(R.id.textView)
        val imageView: ImageView = headerView.findViewById(R.id.imageView)



        textView.setOnClickListener {
            if (navController.currentDestination?.id != R.id.nav_login) {
                val navOptions = NavOptions.Builder()
                    .setPopUpTo(R.id.nav_home, inclusive = true)
                    .build()
                navController.navigate(R.id.nav_login, null, navOptions)
                drawerLayout.closeDrawer(GravityCompat.START)
            } else {
                drawerLayout.closeDrawer(GravityCompat.START)
            }
        }

        textView.setOnClickListener {
            if (navController.currentDestination?.id != R.id.nav_login) {
                val navOptions = NavOptions.Builder()
                    .setPopUpTo(R.id.nav_home, inclusive = true)
                    .build()
                navController.navigate(R.id.nav_login, null, navOptions)
                drawerLayout.closeDrawer(GravityCompat.START)
            } else {
                drawerLayout.closeDrawer(GravityCompat.START)
            }
        }

        imageView.setOnClickListener {
            if (navController.currentDestination?.id != R.id.nav_login) {
                val navOptions = NavOptions.Builder()
                    .setPopUpTo(R.id.nav_home, inclusive = true)
                    .build()
                navController.navigate(R.id.nav_login, null, navOptions)
                drawerLayout.closeDrawer(GravityCompat.START)
            } else {
                drawerLayout.closeDrawer(GravityCompat.START)
            }
        }

//        fun onImageViewClick(view: View) {
//            val navController = findNavController(R.id.nav_host_fragment_content_main)
//            val drawerLayout: DrawerLayout = binding.drawerLayout
//
//            if (navController.currentDestination?.id != R.id.nav_login) {
//                val navOptions = NavOptions.Builder()
//                    .setPopUpTo(R.id.nav_home, inclusive = true)
//                    .build()
//                navController.navigate(R.id.nav_login, null, navOptions)
//                drawerLayout.closeDrawer(GravityCompat.START)
//            } else {
//                drawerLayout.closeDrawer(GravityCompat.START)
//            }
//        }


        // Проверка доступности хоста vk.com при старте приложения

    }


    private fun checkHostReachability() {
        CoroutineScope(Dispatchers.IO).launch {
            val isHostReachable = try {
                InetAddress.getByName("vk.com").isReachable(5000)
            } catch (e: Exception) {
                false
            }

            withContext(Dispatchers.Main) {
                if (!isHostReachable) {
                    Snackbar.make(binding.root, "Оффлайн режим", Snackbar.LENGTH_LONG).show()
                }
            }
        }
    }

    override fun onSupportNavigateUp(): Boolean {
        val navController = findNavController(R.id.nav_host_fragment_content_main)
        return navController.navigateUp(appBarConfiguration) || super.onSupportNavigateUp()
    }
}