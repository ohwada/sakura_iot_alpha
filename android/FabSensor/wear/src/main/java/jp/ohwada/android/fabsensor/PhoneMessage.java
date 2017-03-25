/**
 * Fab Sensor
 * 2016-11-01 K.OHWADA
 */
package jp.ohwada.android.fabsensor;

import android.app.Activity;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.common.api.GoogleApiClient.ConnectionCallbacks;
import com.google.android.gms.common.api.GoogleApiClient.OnConnectionFailedListener;
import com.google.android.gms.wearable.CapabilityApi;
import com.google.android.gms.wearable.CapabilityInfo;
import com.google.android.gms.wearable.DataApi;
import com.google.android.gms.wearable.DataEvent;
import com.google.android.gms.wearable.DataEventBuffer;
import com.google.android.gms.wearable.MessageApi;
import com.google.android.gms.wearable.MessageEvent;
import com.google.android.gms.wearable.Wearable;

/**
 * PhoneMessage
 */
public class PhoneMessage implements
        ConnectionCallbacks,
        OnConnectionFailedListener,
        DataApi.DataListener,
        MessageApi.MessageListener,
        CapabilityApi.CapabilityListener {

   // debug
    private static final String TAG_SUB = PhoneMessage.class.getSimpleName();

    // connection status
    public static final int STATUS_CONNECTED = 1;
    public static final int STATUS_CONNECTION_SUSPENDED = 2;
    public static final int STATUS_CONNECTION_FAILED = 3;

    // input parameter
    private  Activity mActivity;
    
    // object   
    private GoogleApiClient mGoogleApiClient;

    // callback 
    private OnChangedListener mListener;  

    /*
     * callback interface
     */    
    public interface OnChangedListener {
        void onConnectionChanged( int status );
        void onDataChanged( DataEvent event );
        void onMessageReceived( MessageEvent event );
        void onCapabilityChanged( CapabilityInfo Info );
    }

    /*
     * callback
     */ 
    public void setOnChangedListener( OnChangedListener listener ) {
        mListener = listener;
    }

    /**
      * Constractor
      * @param Activity activity
      */      
    public PhoneMessage( Activity activity ) {
        mActivity = activity;
        mGoogleApiClient = new GoogleApiClient.Builder(activity)
            .addApi(Wearable.API)
            .addConnectionCallbacks(this)
            .addOnConnectionFailedListener(this)
            .build();
    }

    /*
     * connect
     */ 
    public void connect() {
        mGoogleApiClient.connect();
    }

    /*
     * disconnect
     */ 
    public void disconnect() {
        // disconnect, if connected
        if ((mGoogleApiClient != null) && mGoogleApiClient.isConnected()) {
            Wearable.DataApi.removeListener(mGoogleApiClient, this);
            Wearable.MessageApi.removeListener(mGoogleApiClient, this);
            Wearable.CapabilityApi.removeListener(mGoogleApiClient, this);
            mGoogleApiClient.disconnect();
        }
    }

    /*
     * === onConnected ===
     */ 
    @Override
    public void onConnected(Bundle connectionHint) {
        log_d("onConnected");
        Wearable.DataApi.addListener(mGoogleApiClient, this);
        Wearable.MessageApi.addListener(mGoogleApiClient, this);
        Wearable.CapabilityApi.addListener(
            mGoogleApiClient, this, Uri.parse("wear://"), CapabilityApi.FILTER_REACHABLE);
        notifyConnectionChanged( STATUS_CONNECTED );
    }

    /*
     * === onConnectionSuspended ===
     */ 
    @Override
    public void onConnectionSuspended(int cause) {
        log_d("onConnectionSuspended " + cause);
        notifyConnectionChanged( STATUS_CONNECTION_SUSPENDED );
    }

    /*
     * === onConnectionSuspended ===
     */ 
    @Override
    public void onConnectionFailed(ConnectionResult result) {
        log_d("onConnectionFailed");
        notifyConnectionChanged( STATUS_CONNECTION_FAILED );
    }

    /**
     * === onDataChanged ===
     */
    @Override
    public void onDataChanged(DataEventBuffer buffer) {
        log_d("onDataChanged");
        for (DataEvent event : buffer) {
            int type = event.getType();
            String path = event.getDataItem().getUri().getPath();
            log_d("onDataChanged: " + type + " " + path);
            nofityDataChanged(event);
        }
    }

    /**
     * === onMessageReceived ===
     */
    @Override
    public void onMessageReceived(MessageEvent event) {
        int id = event.getRequestId();
        String path = event.getPath();
        String message = new String(event.getData());
        log_d("onMessageReceived: " + id + " " + path + " " + message);
        notifyMessageReceived(event);
    }

    /**
     * === onCapabilityChanged ===
     */
    @Override
    public void onCapabilityChanged(CapabilityInfo info) {
        log_d("onCapabilityChanged");
        notifyCapabilityChanged(info);
    }

    /**
     * notifyConnectionChanged
     */
    private void notifyConnectionChanged( int status ) {
        if ( mListener != null ) {
            mListener.onConnectionChanged( status );
        }
    }

    /**
     * nofityDataChanged
     */    
    private void nofityDataChanged(DataEvent event) {
        if ( mListener != null ) {
            mListener.onDataChanged(event);
        }
    }   

    /**
     * notifyMessageReceived
     */ 
    private void notifyMessageReceived(MessageEvent event) {
        if ( mListener != null ) {
            mListener.onMessageReceived(event);
        }
    }

    /**
     * notifyCapabilityChanged
     */
    private void notifyCapabilityChanged(CapabilityInfo Info) {
        if ( mListener != null ) {
            mListener.onCapabilityChanged(Info);
        }
    }

    /**
     * log_d
     */
    private static void log_d(String str) {
        if (Constant.DEBUG) Log.d(Constant.TAG, TAG_SUB + " " + str);
    }
                                            
}