package com.mao.earth_clock

import android.app.AlarmManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.graphics.BitmapFactory
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.mao.earth_clock.databinding.ActivityMainBinding
import java.io.File

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val alarmService: AlarmManager = getSystemService(Context.ALARM_SERVICE) as AlarmManager
        alarmService.setRepeating(
            AlarmManager.RTC_WAKEUP,
            System.currentTimeMillis() + 5 * 1000,
            10 * 60 * 1000,
            PendingIntent.getBroadcast(
                this, 0, Intent(this, AlarmReceiver::class.java),
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )
        )

    }

    override fun onResume() {
        super.onResume()
        val image = File(cacheDir, "earth.png")
        if (image.exists()) {
            binding.imageView.setImageBitmap(BitmapFactory.decodeFile(image.absolutePath))
        }
    }
}