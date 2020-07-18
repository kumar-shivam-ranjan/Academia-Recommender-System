package com.example.academiarecommendersystem

import android.content.Context
import android.graphics.Color
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.BaseAdapter
import android.widget.ListView
import android.widget.TextView

class ResultActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_result)
        val listview=findViewById<ListView>(R.id.main_list_view)
       // val redcolor= Color.parseColor("#ff0000")
       // listview.setBackgroundColor(redcolor)
        listview.adapter=MycustomAdaptor(this)

    }
    private class MycustomAdaptor(context: Context):BaseAdapter(){
        private val mcontext: Context
        init {
            this.mcontext=context
        }
        override fun getCount(): Int {
            return  1
        }
        override fun getItemId(position: Int): Long {
            return position.toLong()

        }
        override fun getItem(position: Int): Any {
            return "TEST STRING"
        }
        override fun getView(position: Int, convertView: View?, viewGroup: ViewGroup?): View? {
            val layout =LayoutInflater.from(mcontext)
            val rowMain=layout.inflate(R.layout.main_row,viewGroup,false)
            return rowMain
        }


    }

}