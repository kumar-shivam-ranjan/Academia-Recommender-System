package com.example.academiarecommendersystem

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import com.google.firebase.auth.ktx.auth
import com.google.firebase.ktx.Firebase
import kotlinx.android.synthetic.main.activity_dashboard.*

class DashboardActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_dashboard)
        val recommendation=findViewById<Button>(R.id.recommendations)
        val profile=findViewById<Button>(R.id.profile_btn)
        val logout=findViewById<Button>(R.id.logout_btn)
        val search=findViewById<Button>(R.id.search)
        val uname=intent.getStringExtra("uname")
        val email=intent.getStringExtra("email")

        profile.setOnClickListener {
            val intent= Intent(this,Profile::class.java)
            intent.putExtra("uname",uname)
            intent.putExtra("email",email)
            startActivity(intent)
        }
        recommendations.setOnClickListener {
            val intent=Intent(this,Recommendation::class.java)
            startActivity(intent)
        }
        logout.setOnClickListener {
            Firebase.auth.signOut()
            val intent=Intent(this,LoginActivity::class.java)
            startActivity(intent)
        }
    }
}