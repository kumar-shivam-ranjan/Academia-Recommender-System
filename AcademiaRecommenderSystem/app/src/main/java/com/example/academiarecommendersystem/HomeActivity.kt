package com.example.academiarecommendersystem

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import kotlinx.android.synthetic.main.activity_home.*

class HomeActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_home)
        val uname=intent.getStringExtra("uname")
        val eemail=intent.getStringExtra("email")
        button.setOnClickListener {
            val intent= Intent(this,DashboardActivity::class.java)
            intent.putExtra("uname",uname)
            intent.putExtra("email",eemail)
            startActivity(intent)
        }
    }
}