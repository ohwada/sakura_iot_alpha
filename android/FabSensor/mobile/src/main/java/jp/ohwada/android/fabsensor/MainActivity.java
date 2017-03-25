/**
 * Fab Sensor
 * 2016-11-01 K.OHWADA
 */
package jp.ohwada.android.fabsensor;

import android.app.Activity;
import android.content.Context;

import android.content.Intent;
import android.content.SharedPreferences;

import android.os.Bundle;
import android.preference.PreferenceManager;
import android.util.Log;

import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.wearable.CapabilityInfo;
import com.google.android.gms.wearable.DataApi.DataItemResult;
import com.google.android.gms.wearable.DataEvent;
import com.google.android.gms.wearable.DataMapItem;
import com.google.android.gms.wearable.MessageApi.SendMessageResult;
import com.google.android.gms.wearable.MessageEvent;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.ScheduledThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

/*
 * MainActivity
 */ 
public class MainActivity extends Activity {

   // debug
    private static final boolean D = Constant.DEBUG;
    private static final String TAG_SUB = MainActivity.class.getSimpleName();
    
    // volley
    private static final int VOLLEY_REQ_API = 1;

    // refresh
    private static final long REFRESH_INITIAL_DELAY = 1;
    private static final long REFRESH_DELAY = 10;

// SharedPreferences    
    private static final String PREF_KEY_URL = "url";
    private static final String PREF_KEY_DISPLAY = "display_event";
    private static final String PREF_KEY_INTERVAL = "refresh_interval";
    private static final String PREF_DEFAULT_URL = "";
    private static final boolean PREF_DEFAULT_DISPLAY = true;
    private static final String PREF_DEFAULT_INTERVAL = "10";
            
    private static final String EXAMPLE_URL = "http://example.com/";

    /* Intent request codes */
    private static final int REQUEST_SETTING = 1;

    // object
    private SharedPreferences mPreferences;
    private VolleyUtil mVolley;
    private JsonParser mParser;
    private WearMessage mMessage;

    // Refresh
    private ScheduledExecutorService mRefreshService;
    private ScheduledFuture<?> mRefreshFuture;
    
    // UI
    private TextView mTextViewTime;
    private TextView mTextViewTemperature;
    private TextView mTextViewHumidity;
    private TextView mTextViewPressure;
    private TextView mTextViewLight;
    private TextView mTextViewNoise; 
    private ListView mListViewEvent;
    
    private EventAdapter mEventAdapter;

    private SimpleDateFormat mFormat = new SimpleDateFormat("yyyy-MM-dd kk:mm");
        
    // variable    
    private boolean isWearConnected = false;
    private boolean isWearFirst = true;
    private String mUrl = PREF_DEFAULT_URL;

    /*
     * === onCreate ===
     */                                     
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        log_d("onCreate");
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main);

        mParser = new JsonParser();
        mPreferences = PreferenceManager.getDefaultSharedPreferences(this);
        startVolley(this);
        startWearMessage(this);

        mTextViewTime = (TextView) findViewById( R.id.TextView_time );
        mTextViewTemperature= (TextView) findViewById( R.id.TextView_temperature );
        mTextViewHumidity = (TextView) findViewById( R.id.TextView_humidity );
        mTextViewPressure = (TextView) findViewById( R.id.TextView_pressure );
        mTextViewLight = (TextView) findViewById( R.id.TextView_light );
        mTextViewNoise = (TextView) findViewById( R.id.TextView_noise );                                
        mListViewEvent = (ListView) findViewById(R.id.ListView_event);
                
        Button btnRefresh = (Button) findViewById( R.id.Button_refresh );
        btnRefresh.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                isWearFirst = true;
                procRefresh();
            }
        });

        // Stores DataItems received by the local broadcaster or from the paired watch.
        mEventAdapter = new EventAdapter(this, android.R.layout.simple_list_item_1);
        mListViewEvent.setAdapter(mEventAdapter);

        // refresh
        mRefreshService = new ScheduledThreadPoolExecutor(1);                
    }

    /*
     * === onStart ===
     */                                 
    @Override
    protected void onStart() {
        log_d("onStart");
        super.onStart();
        mMessage.connect();
    }

    /*
     * === onResume ===
     */
    @Override
    public void onResume() {
        log_d("onResume");
        super.onResume();
        mUrl = mPreferences.getString(PREF_KEY_URL, PREF_DEFAULT_URL);
        boolean isDisplay = mPreferences.getBoolean(PREF_KEY_DISPLAY, PREF_DEFAULT_DISPLAY);
        int interval  = parseInt( mPreferences.getString(PREF_KEY_INTERVAL, PREF_DEFAULT_INTERVAL) );
        if ( "".equals(mUrl) || mUrl.endsWith(EXAMPLE_URL) ) {
            toast_short( R.string.edittext_pref_url_summary );
            startActivitySetting();
            return;
        }
        if ( isDisplay ) {
            mEventAdapter.clear();
            mListViewEvent.setVisibility(View.VISIBLE);
        } else {
            mListViewEvent.setVisibility(View.INVISIBLE);
        }
        isWearFirst = true;
        mRefreshFuture = mRefreshService.scheduleWithFixedDelay(
            new RefreshGenerator(), REFRESH_INITIAL_DELAY,  interval, TimeUnit.SECONDS);
    }

    /*
     * === onPause ===
     */
    @Override
    public void onPause() {
        log_d("onPause");
        super.onPause();
        if ( mRefreshFuture != null ) {
            mRefreshFuture.cancel(true);
        }
    }

    /*
     * === onStop ===
     */        
    @Override
    protected void onStop() {
        log_d("onStop");
        mMessage.disconnect();
        super.onStop();
    }
        
    /**
     * === onDestroy ===
     */ 
    @Override
    public void onDestroy() {
        log_d( "onDestroy" );
        super.onDestroy();
        mVolley.stop();
    }

    /**
     * === onCreateOptionsMenu ===
     */
    @Override
    public boolean onCreateOptionsMenu( Menu menu ) {
        log_d( "onCreateOptionsMenu" );
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }
 
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
    }

    /**
     * === onActivityResult ===
     */
    @Override
    public void onActivityResult( int request, int result, Intent data ) {
        log_d( "onActivityResult" );
        // dummy
    }
                                        
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
    }
    
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
    }

    /**
     * procVolleyResponseApi
     */
    private void procVolleyResponseApi( String response ) {
        if ( response.isEmpty()) {
            toast_short("Unable to get data from the server");
            return;
        }
        List<SensorRec> list = mParser.parse( response );
        int size = list.size();
        if (size == 0) {
            toast_short("Unable to get data from the server");
            return;
        }
        // show sensor data
        toast_short( "refresh" );
        SensorRec item = list.get( size - 1 );
        mTextViewTime.setText( convTime( item.time ));
        mTextViewTemperature.setText( convFloat( item.temperature ));
        mTextViewHumidity.setText( convFloat( item.humidity ));
        mTextViewPressure.setText( convFloat( item.pressure ));
        mTextViewLight.setText( convFloat( item.light ));
        mTextViewNoise.setText( convFloat( item.noise ));
        // send sensor data to wear divice
        if ( isWearConnected ) {
            mMessage.sendSensorData( item );
        }
    }

    /**
     * convTime
     */
    private String convTime(int unixtime) {
        Date date = new Date( unixtime * 1000L );
        return mFormat.format(date);
    }

    /**
     * convFloat
     */
    private String convFloat(float value) {
        return String.format("%.1f", value);
    }

    /**
     * procVolleyErrorResponse
     */ 
    private void procVolleyErrorResponse(String error) {
        toast_short( "Server Error " + error );
    }

    /**
     * startWearMessage
     */     
    private void startWearMessage( Activity activity ) {
        mMessage = new WearMessage( activity );
        mMessage.setOnChangedListener(new WearMessage.OnChangedListener() {
            @Override
            public void onConnectionChanged( int status ) {
                procWearConnectionChanged( status );
            }
            @Override
            public void onDataChanged( DataEvent event ) {
                procWearDataChanged(event );
            }
            @Override
            public void onMessageReceived( MessageEvent event ) {
                procWearMessageReceived( event );
            }
            @Override
            public void onCapabilityChanged( CapabilityInfo Info ) {
                procWearCapabilityChanged( Info );
            }
            @Override
            public void onStartActivityResult( SendMessageResult result ) {
                procWearStartActivityResult( result );
            }
            @Override
            public void onSendSensorResult( DataItemResult result ) {
                procWearSendSensorResult( result );
            }
        });
    }

    /**
     * procWearConnectionChanged
     */
    void procWearConnectionChanged( int status ) {
        switch (status) {
            case WearMessage.STATUS_CONNECTED:
                isWearConnected = true;
                toast_short( "Wear connected" );
                break;
            case WearMessage.STATUS_CONNECTION_SUSPENDED:
                isWearConnected = false;   
                toast_short( "Wear connection suspended" );
                break;
             case WearMessage.STATUS_CONNECTION_FAILED:
                isWearConnected = false;   
                toast_short( "Wear connection failed" );
                break;
        }    
    }    

    /**
     * procWearDataChanged
     */    
    void procWearDataChanged( DataEvent event ) {
        String path = event.getDataItem().getUri().getPath();
        int type = event.getType();
        if (type == DataEvent.TYPE_CHANGED) {
            if ( MessageConstant.PATH_SENSOR.equals(path) ) {
                DataMapItem dataMapItem = DataMapItem.fromDataItem(event.getDataItem());
                int time = dataMapItem.getDataMap().getInt( MessageConstant.KEY_TIME );
                mEventAdapter.add(
                    new EventRec("Data changed", "time " + time ));
            } else {
                mEventAdapter.add(
                    new EventRec("Data changed", event.getDataItem().toString() ));
            }        
        } else if (type == DataEvent.TYPE_DELETED) {
            mEventAdapter.add(
                new EventRec("Data deleted", event.getDataItem().toString()));
        }                
    }

    /**
     * procWearMessageReceived
     */         
    void procWearMessageReceived( MessageEvent event ) {
        String path = event.getPath();
        String data = new String(event.getData());
        mEventAdapter.add(new EventRec("Message", path + " " + data ));
    }    

    /**
     * procWearCapabilityChanged
     */     
    void procWearCapabilityChanged( CapabilityInfo info ) {
        mEventAdapter.add(new EventRec("onCapabilityChanged", info.toString()));
    }

    /**
     * procWearStartActivityResult
     */         
    void procWearStartActivityResult( SendMessageResult result ) {
        if (result.getStatus().isSuccess()) {
//            toast_short( "StartActivity Success" );
        } else {
            toast_short( "Wear start ativity failed" ); 
        }               
    }    

    /**
     * procWearSendSensorResult
     */ 
    void procWearSendSensorResult( DataItemResult result ) {
        if (result.getStatus().isSuccess()) {
//            toast_short( "SendSensor Success" );
        } else {
            toast_short( "Wear send sensor failed" ); 
        }  
    }    

    /**
     * startActivitySetting
     */
    private void startActivitySetting() {
        Intent intent = new Intent( this, SettingActivity.class );
        startActivityForResult( intent, REQUEST_SETTING );        
    }

   /**
     * parseInt
     */
    private int parseInt(String str) {
        int v = 0;
        try {
            v = Integer.parseInt(str);
        } catch (NumberFormatException e) {
            if (D) e.printStackTrace();
        }
        return v;
    }
    
    /**
     * procRefresh
     */
    private void procRefresh() {
        if ( isWearFirst && isWearConnected ) {
            isWearFirst = false;
            mMessage.startWearableActivity();
        }
        if ( !mUrl.isEmpty() ) {
            mVolley.requestServer(mUrl, VOLLEY_REQ_API);
        }                
    }

    /**
     * class RefreshGenerator
     */
    private class RefreshGenerator implements Runnable {
        @Override
        public void run() {
            procRefresh();
        }
    }
    
    /**
     * toast short
     */       
    private void toast_short( int id ) {
        ToastMaster.makeText(this, id, Toast.LENGTH_SHORT).show();
    }
    
    /**
     * toast short
     */       
    private void toast_short( String str ) {
        ToastMaster.makeText(this, str, Toast.LENGTH_SHORT).show();
    }
                               
    /**
     * log_d
     */
    private static void log_d(String str) {
        if (Constant.DEBUG) Log.d(Constant.TAG, TAG_SUB + " " + str);
    }

}
