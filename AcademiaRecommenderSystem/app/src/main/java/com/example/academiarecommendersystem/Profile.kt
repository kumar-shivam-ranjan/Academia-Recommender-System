package com.example.academiarecommendersystem

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import com.google.firebase.auth.ktx.auth
import com.google.firebase.ktx.Firebase

class Profile : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_profile)
        val logout=findViewById<Button>(R.id.logout_btn)
        val uname_text=findViewById<TextView>(R.id.uname_textview)
        val email_text=findViewById<TextView>(R.id.email_textview)
        val uname=intent.getStringExtra("uname")
        val user=Firebase.auth.currentUser
        user?.let {
            for (profile in it.providerData){
                val name=profile.displayName
                val email=profile.email
                uname_text.text=name
                email_text.text=email
            }
            uname_text.text=uname
        }
        logout.setOnClickListener {
            Firebase.auth.signOut()
            val intent= Intent(this,LoginActivity::class.java)
            startActivity(intent)
        }
    }
}