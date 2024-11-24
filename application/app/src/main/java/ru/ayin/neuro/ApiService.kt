package ru.ayin.neuro

import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Path

// Модель тела запроса
data class CommandRequest(val command: String)

// Интерфейс API
interface ApiService {
    @POST("py/script-control/")
    fun sendCommand(@Body request: CommandRequest): Call<Void>

    @GET("api/calibri/{name}/")
    fun getPulseData(@Path("name") name: String): Call<CalibriResponse>
}

