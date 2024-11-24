package com.example.callibri.login

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel

class LoginViewModel : ViewModel() {

    private val _loginStatus = MutableLiveData<Boolean>()
    val loginStatus: LiveData<Boolean> get() = _loginStatus

    fun login(username: String, password: String) {
        // Здесь можно добавить логику для проверки логина и пароля
        if (username == "admin" && password == "password") {
            _loginStatus.value = true
        } else {
            _loginStatus.value = false
        }
    }
}