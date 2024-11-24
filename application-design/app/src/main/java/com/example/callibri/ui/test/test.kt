package com.example.callibri.ui.test//// RealTimeChartFragment.kt
//import android.os.Bundle
//import android.os.Handler
//import android.os.Looper
//import android.view.LayoutInflater
//import android.view.View
//import android.view.ViewGroup
//import androidx.fragment.app.Fragment
//import com.github.mikephil.charting.charts.LineChart
//import com.github.mikephil.charting.data.*
//import kotlin.random.Random
//
//class RealTimeChartFragment : Fragment() {
//
//    private lateinit var chart: LineChart
//    private val handler = Handler(Looper.getMainLooper())
//    private var xAxisValue = 0f
//
//    override fun onCreateView(
//        inflater: LayoutInflater, container: ViewGroup?,
//        savedInstanceState: Bundle?
//    ): View? {
//        val view = inflater.inflate(R.layout.fragment_real_time_chart, container, false)
//        chart = view.findViewById(R.id.chart)
//        return view
//    }
//
//    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
//        super.onViewCreated(view, savedInstanceState)
//        initializeChart()
//        startChartUpdates()
//    }
//
//    private fun initializeChart() {
//        // Chart configuration and initial setup
//        chart.description.isEnabled = false
//        chart.setTouchEnabled(true)
//        chart.setScaleEnabled(true)
//        chart.setDrawGridBackground(false)
//        chart.setDrawBorders(false)
//
//        // X-axis configuration
//        val xAxis = chart.xAxis
//        xAxis.position = XAxis.XAxisPosition.BOTTOM
//        xAxis.setDrawAxisLine(true)
//        xAxis.setDrawGridLines(true)
//
//        // Y-axis configuration
//        val leftAxis = chart.axisLeft
//        leftAxis.setDrawAxisLine(true)
//        leftAxis.setDrawGridLines(true)
//        leftAxis.axisMinimum = 0f
//
//        val rightAxis = chart.axisRight
//        rightAxis.setEnabled(false)
//
//        // Add initial data
//        val entries = arrayListOf<Entry>()
//        entries.add(Entry(0f, 0f))
//        val dataSet = LineDataSet(entries, "Data Set")
//        dataSet.color = Color.BLUE
//        dataSet.setDrawCircles(false)
//        dataSet.setDrawValues(false)
//
//        val data = LineData(dataSet)
//        chart.data = data
//    }
//
//    private fun startChartUpdates() {
//        handler.post(runnable)
//    }
//
//    private val runnable = Runnable {
//        // Generate new data point
//        val lastEntry = chart.data.getDataSetByIndex(0).getEntryForIndex(chart.data.getDataSetByIndex(0).entryCount - 1)
//        val newEntry = Entry(lastEntry.x + 1, (lastEntry.y + Random.nextFloat() * 10).toFloat())
//        chart.data.getDataSetByIndex(0).addEntry(newEntry)
//        chart.data.notifyDataChanged()
//        chart.notifyDataSetChanged()
//        chart.setVisibleXRangeMaximum(10f)
//        chart.moveViewToX(chart.data.entryCount.toFloat())
//        handler.postDelayed(runnable, 1000)
//    }
//
//    override fun onDestroy() {
//        super.onDestroy()
//        handler.removeCallbacks(runnable)
//    }
//}