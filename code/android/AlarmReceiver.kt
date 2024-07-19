package com.mao.earth_clock

import android.app.WallpaperManager
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.ColorMatrixColorFilter
import android.graphics.Paint
import android.util.Log
import java.io.File
import java.io.FileOutputStream
import java.net.HttpURLConnection
import java.net.URL
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class AlarmReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context?, intent: Intent?) {
        Thread {
            val httpURLConnection =
                URL("https://xxx.oss-cn-hongkong.aliyuncs.com/earth.png")
                    .openConnection() as HttpURLConnection
            val inputStream = httpURLConnection.inputStream
            val bitmap = BitmapFactory.decodeStream(inputStream)
            inputStream.close()

            if (bitmap.allocationByteCount < 50 * 1000) {
                Log.d("MMM", "No image(" + bitmap.allocationByteCount + ")")
                return@Thread
            }
            val timeStr = SimpleDateFormat("ddHHmm", Locale.getDefault()).format(Date())
            Log.d("MMM", timeStr)

            val newBitmap = Bitmap.createBitmap(750, 1100, Bitmap.Config.ARGB_8888)
            val canvas = Canvas(newBitmap)
            canvas.drawRect(0f, 0f, 750f, 1100f, Paint().apply { color = Color.BLACK })
            canvas.drawBitmap(bitmap, 100f, 275f,
                Paint().apply {
                    // 增加亮度
                    val floatArray = FloatArray(20)
                    floatArray[0] = 1.3f
                    floatArray[6] = 1.3f
                    floatArray[12] = 1.3f
                    floatArray[18] = 1f
                    colorFilter = ColorMatrixColorFilter(floatArray)
                }
            )
            canvas.drawText(timeStr, 350f, 850f,
                Paint().apply { color = Color.WHITE;alpha = 40;textSize = 14f }
            )
            val cacheDir = context?.cacheDir
            val file = File(cacheDir, "earth.png")
            FileOutputStream(file).use { outputStream ->
                newBitmap.compress(Bitmap.CompressFormat.PNG, 100, outputStream)
                outputStream.flush()
                outputStream.close()
            }

            val wallpaperManager = WallpaperManager.getInstance(context)
            wallpaperManager.setBitmap(newBitmap)
        }.start()
    }

}