package com.example.academiarecommendersystem

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import com.google.firebase.auth.FirebaseAuth
import kotlinx.android.synthetic.main.activity_login.*

class LoginActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)
        Login_button.setOnClickListener {
            val email=email_login.text.toString()
            val password=password_login.text.toString()
            if(email.isEmpty() || password.isEmpty())
            {
                Toast.makeText(this,"Please enter Text in email/password/username",Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }
            val uname=intent.getStringExtra("uname")
            val eemail=intent.getStringExtra("email")
            Log.d("Login","Attempt Login with email/password: $email/***")

            FirebaseAuth.getInstance().signInWithEmailAndPassword(email,password)
                .addOnCompleteListener {
                    if(!it.isSuccessful) return@addOnCompleteListener
                    val intent= Intent(this,HomeActivity::class.java)
                    intent.putExtra("uname",uname)
                    intent.putExtra("email",eemail)
                    startActivity(intent)
                }
                .addOnFailureListener {
                    Toast.makeText(this,"Failed to login user: ${it.message}", Toast.LENGTH_SHORT).show()
                }
        }
        dont_have_account_textview.setOnClickListener {
            finish()
        }
    }
}