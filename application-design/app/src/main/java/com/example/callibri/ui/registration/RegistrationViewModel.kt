package com.example.callibri.registration

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel

class RegistrationViewModel : ViewModel() {

    private val _registrationStatus = MutableLiveData<Boolean>()
    val registrationStatus: LiveData<Boolean> get() = _registrationStatus

    fun register(username: String, email: String, password: String) {
        // Здесь можно добавить логику для регистрации пользователя
        if (isValidRegistration(username, email, password)) {
            _registrationStatus.value = true
        } else {
            _registrationStatus.value = false
        }
    }

    private fun isValidRegistration(username: String, email: String, password: String): Boolean {
        // Простая проверка на валидность данных
        return username.isNotEmpty() && email.isNotEmpty() && password.isNotEmpty()
    }
}