package com.example.callibri.login

import android.os.Bundle
import android.text.Html
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.navigation.fragment.findNavController
import com.example.callibri.R

class LoginFragment : Fragment() {

    private lateinit var viewModel: LoginViewModel
    private lateinit var editTextLogin: EditText
    private lateinit var editTextPassword: EditText
    private lateinit var buttonLogin: Button

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_login, container, false)
        editTextLogin = view.findViewById(R.id.editTextLogin)
        editTextPassword = view.findViewById(R.id.editTextPassword)
        buttonLogin = view.findViewById(R.id.buttonLogin)
        return view
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        viewModel = ViewModelProvider(this).get(LoginViewModel::class.java)

        val reg = view.findViewById<TextView>(R.id.textViewToPassword)

        reg.text = Html.fromHtml("<u>Нет аккаунта? Зарегистрироваться</u>")

        // Добавляем обработчик клика на текст
        reg.setOnClickListener {
            findNavController().navigate(R.id.nav_registration)
        }

        buttonLogin.setOnClickListener {
            val username = editTextLogin.text.toString()
            val password = editTextPassword.text.toString()
            viewModel.login(username, password)
        }

        viewModel.loginStatus.observe(viewLifecycleOwner, { isSuccess ->
            if (isSuccess) {
                Toast.makeText(requireContext(), "Login successful", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(requireContext(), "Login failed", Toast.LENGTH_SHORT).show()
            }
        })
    }
}