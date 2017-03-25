/**
 * Fab Sensor
 * 2016-11-01 K.OHWADA
 */
package jp.ohwada.android.fabsensor.fragments;

import android.app.Fragment;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import java.text.SimpleDateFormat;
import java.util.Date;

import jp.ohwada.android.fabsensor.R;

/**
 * SensorFragment
 */
public class SensorFragment extends Fragment {
    
    private SimpleDateFormat mFormat = new SimpleDateFormat("yyyy-MM-dd kk:mm");

    // UI  
    private TextView mTextViewTime;
    private TextView mTextViewTemperature;
    private TextView mTextViewHumidity;
    private TextView mTextViewPressure;
    private TextView mTextViewLight;
    private TextView mTextViewNoise;
                
    private boolean isInitialized;

    /**
     * === onCreateView ===
     */        
    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
        Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_sensor_round, container, false);
        mTextViewTime = (TextView) view.findViewById(R.id.TextView_time);
        mTextViewTemperature = (TextView) view.findViewById(R.id.TextView_temperature);
        mTextViewHumidity = (TextView) view.findViewById(R.id.TextView_humidity);
        mTextViewTemperature = (TextView) view.findViewById(R.id.TextView_temperature);
        mTextViewPressure = (TextView) view.findViewById(R.id.TextView_pressure);
        mTextViewLight = (TextView) view.findViewById(R.id.TextView_light);
        mTextViewNoise = (TextView) view.findViewById(R.id.TextView_noise);
                           
//        View view = inflater.inflate(R.layout.sensor_fragment, container, false);
//        final WatchViewStub stub = (WatchViewStub) view.findViewById(R.id.WatchViewStub_sensor);
//        stub.setOnLayoutInflatedListener(new WatchViewStub.OnLayoutInflatedListener() {
//            @Override
 //           public void onLayoutInflated(WatchViewStub stub) {
 //               mTextViewTime = (TextView) stub.findViewById(R.id.TextView_time);
//                mTextViewTemp = (TextView) stub.findViewById(R.id.TextView_temp);
//            }
//        }); 

        isInitialized = true;               
        return view;
    }

    /**
     * setValue
      * @param int time
      * @param float temperature
      * @param float humidity
      * @param float pressure
      * @param float light
     * @param float noise     
     */ 
    public void setValue( int time, float temperature, float humidity, float pressure, float light, float noise ) {
        if (!isInitialized) {
            return;
        }
        mTextViewTime.setText( convTime(time) );
        mTextViewTemperature.setText( convFloat(temperature) );
        mTextViewHumidity.setText( convFloat(humidity) );
        mTextViewPressure.setText( convFloat(pressure) );
        mTextViewLight.setText( convFloat(light) );
        mTextViewNoise.setText( convFloat(noise) );
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
}
