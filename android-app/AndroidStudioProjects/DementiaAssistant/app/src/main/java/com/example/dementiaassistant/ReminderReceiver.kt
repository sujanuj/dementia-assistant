package com.example.dementiaassistant

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.os.Build
import androidx.core.app.NotificationCompat

class ReminderReceiver : BroadcastReceiver() {

    override fun onReceive(context: Context, intent: Intent) {

        val message = intent.getStringExtra("message") ?: "Reminder"

        val channelId = "reminder_channel"

        val manager =
            context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

        // ✅ Create Notification Channel (Required Android 8+)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                channelId,
                "Reminders",
                NotificationManager.IMPORTANCE_HIGH
            ).apply {
                description = "Reminder Notifications"
            }
            manager.createNotificationChannel(channel)
        }

        // ✅ Open app when notification clicked
        val intentOpenApp = Intent(context, MainActivity::class.java)

        val pendingIntent = PendingIntent.getActivity(
            context,
            0,
            intentOpenApp,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        // ✅ Build Notification
        val notification = NotificationCompat.Builder(context, channelId)
            .setContentTitle("⏰ Reminder")
            .setContentText(message)
            .setSmallIcon(android.R.drawable.ic_dialog_info)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setContentIntent(pendingIntent)
            .setAutoCancel(true)
            .build()

        // ✅ Show Notification
        manager.notify(System.currentTimeMillis().toInt(), notification)
    }
}