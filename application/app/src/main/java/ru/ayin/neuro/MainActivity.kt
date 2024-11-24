package ru.ayin.neuro

import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.View
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class MainActivity : AppCompatActivity() {

    private val apiService = RetrofitClient.instance
    private var isDeviceOn = false  // Флаг для управления состоянием устройства

    private lateinit var btnToggle: Button
    private lateinit var txtPulse: TextView
    private lateinit var txtStressNum: TextView
    private lateinit var txtStressLevel: TextView

    private val handler = Handler(Looper.getMainLooper())  // Handler для циклического обновления данных

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Инициализация элементов интерфейса
        btnToggle = findViewById(R.id.btnToggle)
        txtPulse = findViewById(R.id.txtPulse)
        txtStressNum = findViewById(R.id.txtStressNum)
        txtStressLevel = findViewById(R.id.txtStressLevel)

        // Установка обработчика нажатия на кнопку
        btnToggle.setOnClickListener {
            toggleDevice()
        }
    }

    private fun toggleDevice() {
        isDeviceOn = !isDeviceOn  // Переключение состояния

        if (isDeviceOn) {
            // Устройство включено
            btnToggle.text = "Выключить"
            txtPulse.visibility = View.VISIBLE
            txtStressNum.visibility = View.VISIBLE
            txtStressLevel.visibility = View.VISIBLE
            startCheckingPulse()
        } else {
            // Устройство выключено
            btnToggle.text = "Включить"
            txtPulse.visibility = View.GONE
            txtStressNum.visibility = View.GONE
            txtStressLevel.visibility = View.GONE
            stopCheckingPulse()
        }
    }

    private fun startCheckingPulse() {
        handler.postDelayed(object : Runnable {
            override fun run() {
                if (isDeviceOn) {
                    checkPulse()
                    handler.postDelayed(this, 1000)  // Повторяем каждые 1 секунду
                }
            }
        }, 1000)
    }

    private fun stopCheckingPulse() {
        handler.removeCallbacksAndMessages(null)  // Останавливаем все запланированные задачи
    }

    private fun checkPulse() {
        val deviceName = "Callibri_Blue"  // ID устройства
        apiService.getPulseData(deviceName).enqueue(object : Callback<CalibriResponse> {
            override fun onResponse(call: Call<CalibriResponse>, response: Response<CalibriResponse>) {
                if (response.isSuccessful) {
                    val data = response.body()
                    data?.let {
                        txtPulse.text = "RR: ${it.RR}"
                        txtStressNum.text = "Stress Num: ${it.stress_num}"
                        txtStressLevel.text = "Stress Level: ${it.stress_level}"
                    }
                } else {
                    Toast.makeText(this@MainActivity, "Ошибка: ${response.code()}", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onFailure(call: Call<CalibriResponse>, t: Throwable) {
                Toast.makeText(this@MainActivity, "Ошибка: ${t.message}", Toast.LENGTH_SHORT).show()
            }
        })
    }
}
