import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET

interface ApiService {
    @GET("your-endpoint")
    suspend fun getHeartRate(): HeartRateResponse
}

data class HeartRateResponse(
    val heartRate: Int
)

object ApiClient {
    private const val BASE_URL = "https://abf2-188-162-144-139.ngrok-free.app/api/calibri/Callibri_Blue/"

    private val retrofit: Retrofit by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }

    val apiService: ApiService by lazy {
        retrofit.create(ApiService::class.java)
    }
}