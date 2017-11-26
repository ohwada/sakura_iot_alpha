/**
 * fab sensor line chart 
 * 2017-11-01 K.OHWADA
 */

package jp.ohwada.android.fabsensorlinechart;

import android.app.Activity;
import android.content.Context;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;

import android.util.Log;

import android.graphics.Color;
import android.support.v7.app.AppCompatActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import com.github.mikephil.charting.charts.LineChart;

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

import static jp.ohwada.android.fabsensorlinechart.R.id.LineChart;


/**
 * class MainActivity
 */    
public class MainActivity extends Activity {

   // debug
    private static final boolean D = Constant.DEBUG;
    private static final String TAG_SUB = "MainActivity";
        
    // volley
    private static final int VOLLEY_REQ_API = 1;



// SharedPreferences    
    private static final String PREF_KEY_URL = "url";
    private static final String PREF_DEFAULT_URL = "";           
    private static final String EXAMPLE_URL = "http://example.com/";

    /* Intent request codes */
    private static final int REQUEST_SETTING = 1;

    // object
    private SharedPreferences mPreferences;
    private VolleyUtil mVolley;
    private JsonParser mParser;
    private FileUtility mFileUtility;
    

    
    // UI
     private TextView mTextViewPeriod;


 private MyLineChartTime mLineChartTime;
 
 
   private SimpleDateFormat mFormat = new SimpleDateFormat("yyyy-MM-dd kk:mm");

   
/**
 * === onCreate ===
 */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        LineChart chart = (LineChart) findViewById(LineChart);
        
       mTextViewPeriod = (TextView) findViewById(R.id.TextView_period);
       
         mLineChartTime = new MyLineChartTime( chart );
         
mLineChartTime.setLeftAxisMinimum(10f);
 mLineChartTime.setLeftAxisMaximum(40f);
 mLineChartTime.setXAxisLabelsToSkip( 240 );
  mLineChartTime.setDateFormat( "MM-dd HH" );  
  mLineChartTime.setLineLegend( "temperature" );
  
  mFileUtility = new FileUtility(this);
  
            mParser = new JsonParser();
        mPreferences = PreferenceManager.getDefaultSharedPreferences(this);
       
         startVolley(this);
        
        // initFile();
        
    } // onCreate


    /*
     * === onResume ===
     */
    @Override
    public void onResume() {
        log_d("onResume");
        super.onResume();
        String url = mPreferences.getString(PREF_KEY_URL, PREF_DEFAULT_URL);
        if ( !url.isEmpty() ) {
         mVolley.requestServer(url, VOLLEY_REQ_API);
         } // if
         
    } // onResume
        
        
    /**
     * === onDestroy ===
     */ 
    @Override
    public void onDestroy() {
        log_d( "onDestroy" );
        super.onDestroy();
        mVolley.stop();
    } // onDestroy
   
   
       /**
     * === onCreateOptionsMenu ===
     */
    @Override
    public boolean onCreateOptionsMenu( Menu menu ) {
        log_d( "onCreateOptionsMenu" );
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    } // onCreateOptionsMenu
    
    
        /**
     * === onOptionsItemSelected ===
     */
    @Override
    public boolean onOptionsItemSelected( MenuItem item ) {
        log_d( "onOptionsItemSelected" );
        int id = item.getItemId();
        if ( id == R.id.menu_setting ) {
            startActivitySetting();
        }
        return true;
    } // OptionsItemSelected
    
    
        /**
     * === onActivityResult ===
     */
    @Override
    public void onActivityResult( int request, int result, Intent data ) {
        log_d( "onActivityResult" );
        // dummy
    } // onActivityResult
    
    
       /**
     * initFile
     */ 
       private void initFile() { 
    String text = mFileUtility.readAssets( "test.json" );
    List<SensorRec> list = mParser.parse( text );
            int size = list.size();
        if (size == 0) {
            toast_short("Unable to read file");
            return;
        } // if
        
        initChart(list);

    } //  initFile
    
    
      /**
     * initChart
     */ 
       private void initChart(List<SensorRec> list) { 
            int size = list.size();
        if ( size == 0 ) {
            return;
        } // if
        
         SensorRec item_first = list.get( 0 );
     SensorRec item_last = list.get( size - 1 );
     String period = convTime( item_first.time ) + " - " + convTime( item_last.time );
              mTextViewPeriod.setText( period );
               setChartData( list );
               
    } //  initChart 
   
    
        /**
     * startVolley
     */
    private void startVolley(Context context) {
        mVolley = new VolleyUtil( context );
        mVolley.setOnChangedListener(new VolleyUtil.OnChangedListener() {
            @Override
            public void onResponse(int mode, String response) {
                procVolleyResponse(mode, response);
            }
            @Override
            public void onErrorResponse(String error) {
                procVolleyErrorResponse(error);
            }
        });
        mVolley.start();
    } // startVolley
    
    
       /**
     * procVolleyResponse
     */ 
    private void procVolleyResponse( int mode, String response ) {
        long memory = Runtime.getRuntime().freeMemory();
        log_d( "procVolleyResponse: " + mode + ", FreeMemory; " + memory );
        switch( mode ) {
            case VOLLEY_REQ_API:
                procVolleyResponseApi(response);
                break;
        }
    } // procVolleyResponse
    
    
      /**
     * procVolleyResponseApi
     */
    private void procVolleyResponseApi( String response ) {
        if ( response.isEmpty()) {
            toast_short("Unable to get data from the server");
            return;
        } // if
        List<SensorRec> list = mParser.parse( response );
        int size = list.size();
        if (size == 0) {
            toast_short("Unable to get data from the server");
            return;
        } // if
        
              initChart(list);
        
    } // procVolleyResponseApi
    
    
      /**
     * convTime
     */
    private String convTime(int unixtime) {
        Date date = new Date( unixtime * 1000L );
        return mFormat.format(date);
    } // convTime
    
    
  
        /**
     * procVolleyErrorResponse
     */ 
    private void procVolleyErrorResponse(String error) {
        toast_short( "Server Error " + error );
    } // procVolleyErrorResponse
      
      
      /**
     * startActivitySetting
     */
    private void startActivitySetting() {
        Intent intent = new Intent( this, SettingActivity.class );
        startActivityForResult( intent, REQUEST_SETTING );        
    } // startActivitySetting
    
       
/**
 * setChartData
 */
    private void setChartData( List<SensorRec> list ) {
    
      for ( SensorRec rec: list ) {
        
          Date date = new Date( rec.time * 1000L );
          
        mLineChartTime.addData( date, rec.temperature );
    } // for
      
    } // setData



    /**
     * toast short
     */       
    private void toast_short( int id ) {
        ToastMaster.makeText(this, id, Toast.LENGTH_SHORT).show();
    } // toast_short
    
    
    /**
     * toast short
     */       
    private void toast_short( String str ) {
        ToastMaster.makeText(this, str, Toast.LENGTH_SHORT).show();
    } // toast_short
   
   
                               
    /**
     * log_d
     */
    private static void log_d(String str) {
        if (Constant.DEBUG) Log.d(Constant.TAG, TAG_SUB + " " + str);
    } // log_d
    
       
} // MainActivity
