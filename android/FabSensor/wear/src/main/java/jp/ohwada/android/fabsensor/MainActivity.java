/**
 * Fab Sensor
 * 2016-11-01 K.OHWADA
 */
package jp.ohwada.android.fabsensor;

import android.app.Activity;
import android.app.Fragment;
import android.os.Bundle;
import android.support.wearable.view.DotsPageIndicator;
import android.support.wearable.view.GridViewPager;
import android.util.Log;
import android.view.WindowManager;
import android.widget.Toast;

import jp.ohwada.android.fabsensor.fragments.SensorFragment;
import jp.ohwada.android.fabsensor.fragments.EventFragment;

import com.google.android.gms.wearable.CapabilityInfo;
import com.google.android.gms.wearable.DataEvent;
import com.google.android.gms.wearable.DataMap;
import com.google.android.gms.wearable.DataMapItem;
import com.google.android.gms.wearable.MessageEvent;

import java.util.ArrayList;
import java.util.List;

/**
 * MainActivity<p/>
 * The main activity with a view pager, containing three pages:<p/>
 * <ul>
  * <li>
 * Page 1: shows sensor values received from the server
 * </li>
 * <li>
 * Page 2: shows a list of DataItems received from the phone application
 * </li>
 * </ul>
 */
public class MainActivity extends Activity {

   // debug
    private static final String TAG_SUB = MainActivity.class.getSimpleName();

    // object
    private PhoneMessage mMessage;
    
    // UI
    private GridViewPager mPager;
    private SensorFragment mSensorFragment;
    private EventFragment mEventFragment;

    /*
     * === onCreate ===
     */      
    @Override
    public void onCreate(Bundle savedInstanceState) {
        log_d("onCreate");
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        setupViews();
        setupPhoneMessage(this);
    }

    /*
     * === onResume ===
     */ 
    @Override
    protected void onResume() {
        log_d("onResume");
        super.onResume();
        mMessage.connect();
    }

    /*
     * === onPause ===
     */ 
    @Override
    protected void onPause() {
        log_d("onResume");
        mMessage.disconnect();
        super.onPause();
    }

    /**
     * setupViews
     */
    private void setupViews() {
        mPager = (GridViewPager) findViewById(R.id.pager);
        mPager.setOffscreenPageCount(1);
        DotsPageIndicator dotsPageIndicator = (DotsPageIndicator) findViewById(R.id.page_indicator);
        dotsPageIndicator.setDotSpacing((int) getResources().getDimension(R.dimen.dots_spacing));
        dotsPageIndicator.setPager(mPager);

        mSensorFragment = new SensorFragment();
        mEventFragment = new EventFragment();
        List<Fragment> pages = new ArrayList<>();
        pages.add(mSensorFragment);
        pages.add(mEventFragment);

        final SensorPagerAdapter adapter = new SensorPagerAdapter(getFragmentManager(), pages);
        mPager.setAdapter(adapter);
    }

    /**
     * moveToPage
     * Switches to the page {@code index}. The first page has index 0.
     */
    private void moveToPage(int index) {
        mPager.setCurrentItem(0, index, true);
    }

    /**
     * setupPhoneMessage
     */     
    private void setupPhoneMessage( Activity activity ) {
        mMessage = new PhoneMessage( activity );
        mMessage.setOnChangedListener(new PhoneMessage.OnChangedListener() {
            @Override
            public void onConnectionChanged( int status ) {
                procPhoneConnectionChanged( status );
            }
            @Override
            public void onDataChanged( DataEvent event ) {
                procPhoneDataChanged(event );
            }
            @Override
            public void onMessageReceived( MessageEvent event ) {
                procPhoneMessageReceived( event );
            }
            @Override
            public void onCapabilityChanged( CapabilityInfo Info ) {
                procPhoneCapabilityChanged( Info );
            }
        });
    }

    /**
     * procPhoneConnectionChanged
     */
    void procPhoneConnectionChanged( int status ) {
        switch (status) {
            case PhoneMessage.STATUS_CONNECTED:
//                toast_short( "Phone connected" );
                break;
        }    
    } 

    /**
     * procPhoneDataChanged
     */    
    void procPhoneDataChanged( DataEvent event ) {
        String path = event.getDataItem().getUri().getPath();
        int type = event.getType();
        if (type == DataEvent.TYPE_CHANGED) {             
            if (MessageConstant.PATH_SENSOR.equals(path)) {
                procPhoneDataChangedSensor(event);
            } else {
                mEventFragment.append("Data Changed", "path: " + path );
            }
        } else if (type == DataEvent.TYPE_DELETED) {
            mEventFragment.append("Data Deleted", "path: " + path );
        } else {
            mEventFragment.append("Data Unknown", "type: " + type );
        }
    }

    /**
     * procPhoneDataChangedSensor
     */ 
    private void procPhoneDataChangedSensor( DataEvent event ) {
        log_d("procPhoneDataChangedSensor");
        DataMapItem item = DataMapItem.fromDataItem(event.getDataItem());
        DataMap map = item.getDataMap();
        long timestamp = map.getLong( MessageConstant.KEY_TIMESTAMP );
        int time = map.getInt( MessageConstant.KEY_TIME );
        float temperature = map.getFloat( MessageConstant.KEY_TEMPERATURE );                
        float humidity = map.getFloat( MessageConstant.KEY_HUMIDITY );
        float pressure = map.getFloat( MessageConstant.KEY_PRESSURE );
        float light = map.getFloat( MessageConstant.KEY_LIGHT );
        float noise = map.getFloat( MessageConstant.KEY_NOISE ); 
        mSensorFragment.setValue( time, temperature, humidity, pressure, light, noise ); 
        mEventFragment.append("Sensor", "timestamp: " + timestamp );  
        toast_short( "refresh" );
    }

    /**
     * procPhoneMessageReceived
     */         
    void procPhoneMessageReceived( MessageEvent event ) {
        String path = event.getPath();
        String data = new String(event.getData());
        mEventFragment.append("Message", path + " " + data);
    }    

    /**
     * procPhoneCapabilityChanged
     */     
    void procPhoneCapabilityChanged( CapabilityInfo info ) {
        mEventFragment.append("Capability Changed", info.toString());
    }

    /**
     * toast short
     */       
    private void toast_short( String str ) {
        Toast.makeText(this, str, Toast.LENGTH_SHORT).show();
    }

    /**
     * log_d
     */
    private static void log_d(String str) {
        if (Constant.DEBUG) Log.d(Constant.TAG, TAG_SUB + " " + str);
    }
        
}