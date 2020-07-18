package com.example.academiarecommendersystem

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import com.google.firebase.auth.FirebaseAuth
import kotlinx.android.synthetic.main.activity_main.*

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        register_btn.setOnClickListener {
           performRegister()
        }
        Already_registered_textview.setOnClickListener {
            Log.d("MainActivity","Try to show login Activity")
            val intent= Intent(this,LoginActivity::class.java)
            startActivity(intent)
        }
    }
   private fun performRegister(){
       val email=email_register.text.toString()
       val password=password_register.text.toString()
       val uname=username_register.text.toString()
       if(uname.isEmpty() || password.isEmpty()||email.isEmpty()) {
           Toast.makeText(this,"Please enter Text in email/password/username",Toast.LENGTH_SHORT).show()
           return
       }
       Log.d("MainActivity","Email is : "+email)
       Log.d("MainActivity","password is : $password")
       FirebaseAuth.getInstance().createUserWithEmailAndPassword(email,password)
           .addOnCompleteListener {
               if(!it.isSuccessful) return@addOnCompleteListener
               Log.d("Main","Successfully created user with uid: ${it.result?.user?.uid}")
               val intent=Intent(this,LoginActivity::class.java)
               intent.putExtra("uname", uname)
               intent.putExtra("email", email)
               startActivity(intent)
           }
           .addOnFailureListener {
               Log.d("Main","Failed to create user: ${it.message}")
               Toast.makeText(this,"Failed to create user: ${it.message}",Toast.LENGTH_SHORT).show()
           }
   }
}
