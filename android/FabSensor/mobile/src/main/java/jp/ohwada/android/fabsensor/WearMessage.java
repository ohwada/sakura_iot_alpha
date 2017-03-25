/**
 * Fab Sensor
 * 2016-11-01 K.OHWADA
 */
package jp.ohwada.android.fabsensor;

import android.app.Activity;

import android.content.IntentSender;
import android.net.Uri;
import android.os.AsyncTask;

import android.os.Bundle;
import android.util.Log;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.common.api.GoogleApiClient.ConnectionCallbacks;
import com.google.android.gms.common.api.GoogleApiClient.OnConnectionFailedListener;
import com.google.android.gms.common.api.ResultCallback;
import com.google.android.gms.wearable.CapabilityApi;
import com.google.android.gms.wearable.CapabilityInfo;
import com.google.android.gms.wearable.DataApi;
import com.google.android.gms.wearable.DataApi.DataItemResult;
import com.google.android.gms.wearable.DataEvent;
import com.google.android.gms.wearable.DataEventBuffer;
import com.google.android.gms.wearable.MessageApi;
import com.google.android.gms.wearable.MessageApi.SendMessageResult;
import com.google.android.gms.wearable.MessageEvent;
import com.google.android.gms.wearable.Node;
import com.google.android.gms.wearable.NodeApi;
import com.google.android.gms.wearable.PutDataMapRequest;
import com.google.android.gms.wearable.PutDataRequest;
import com.google.android.gms.wearable.Wearable;

import java.util.Collection;
import java.util.HashSet;

/*
 * WearMessage
 */ 
public class WearMessage implements
        CapabilityApi.CapabilityListener,
        MessageApi.MessageListener,
        DataApi.DataListener,
        ConnectionCallbacks,
        OnConnectionFailedListener {

   // debug
    private static final boolean D = Constant.DEBUG;
    private static final String TAG_SUB = WearMessage.class.getSimpleName();

    // Request code for launching the Intent to resolve Google Play services errors.
    private static final int REQUEST_RESOLVE_ERROR = 1000;

    // connection status
    public static final int STATUS_CONNECTED = 1;
    public static final int STATUS_CONNECTION_SUSPENDED = 2;
    public static final int STATUS_CONNECTION_FAILED = 3;

    // input parameter
    private  Activity mActivity;
    
    // local object        
    private GoogleApiClient mGoogleApiClient;

    // variable
    private boolean isResolvingError = false;

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
        void onStartActivityResult( SendMessageResult result );
        void onSendSensorResult( DataItemResult result );
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
    public WearMessage( Activity activity ) {
        mActivity = activity;
        mGoogleApiClient = new GoogleApiClient.Builder(activity)
            .addApi(Wearable.API)
            .addConnectionCallbacks(this)
            .addOnConnectionFailedListener(this)
            .build();                
    }

    /**
     * connect
     */  
    public void connect() {
        log_d("connect");
        // connect, if resolved
        if (!isResolvingError) {
            mGoogleApiClient.connect();
        }
    }

    /**
     * disconnect
     */
    public void disconnect() {
        log_d("disconnect");
        // disconnect, if connected
        if (!isResolvingError && (mGoogleApiClient != null) && (mGoogleApiClient.isConnected())) {
            removeListener();
            mGoogleApiClient.disconnect();
        }
    }

    /**
     * removeListener
     */
    private void removeListener() {
        Wearable.DataApi.removeListener(mGoogleApiClient, this);
        Wearable.MessageApi.removeListener(mGoogleApiClient, this);
        Wearable.CapabilityApi.removeListener(mGoogleApiClient, this);
    }
   
    /**
     * === onConnected ===
     */
    @Override
    public void onConnected( Bundle connectionHint ) {
        log_d("onConnected");
        isResolvingError = false;
        Wearable.DataApi.addListener(mGoogleApiClient, this);
        Wearable.MessageApi.addListener(mGoogleApiClient, this);
        Wearable.CapabilityApi.addListener(
            mGoogleApiClient, this, Uri.parse("wear://"), CapabilityApi.FILTER_REACHABLE);
        notifyConnectionChanged( STATUS_CONNECTED );
    }

    /**
     * === onConnectionSuspended ===
     */
    @Override
    public void onConnectionSuspended(int cause) {
        log_d("onConnectionSuspended " + cause);
        notifyConnectionChanged( STATUS_CONNECTION_SUSPENDED );
    }

    /**
     * === onConnectionFailed ===
     */
    @Override
    public void onConnectionFailed(ConnectionResult result) {
        log_d("onConnectionFailed: " + isResolvingError + " " + result.hasResolution() );
        if (!isResolvingError) {
            if (result.hasResolution()) {
                // start Resolution, if has Resolution
                try {
                    isResolvingError = true;
                    result.startResolutionForResult(mActivity, REQUEST_RESOLVE_ERROR);
                } catch (IntentSender.SendIntentException e) {
                    // There was an error with the resolution intent. Try again.
                    if (D) e.printStackTrace();
                    mGoogleApiClient.connect();
                }
            } else {
                // remove Listener, if NOT has Resolution
                isResolvingError = false;
                removeListener();
                notifyConnectionChanged( STATUS_CONNECTION_FAILED );
            }
        }
    }

    /**
     * === onDataChanged ===
     */
    @Override
    public void onDataChanged(DataEventBuffer dataEventItems) {
        log_d("onDataChanged");
        for (DataEvent event : dataEventItems) {
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
    public void onMessageReceived(final MessageEvent event) {
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
    public void onCapabilityChanged(final CapabilityInfo info) {
        log_d("onCapabilityChanged");
        notifyCapabilityChanged(info);
    }

    /**
     * startWearableActivity
     * Sends an RPC to start a fullscreen Activity on the wearable.
     */
    public void startWearableActivity() {
        log_d("startWearableActivity");
        // Trigger an AsyncTask that will query for a list of connected nodes and send a
        // "start-activity" message to each connected node.
        new StartWearableActivityTask().execute();
    }

    /**
     * sendStartActivityMessage
     */
    private void sendStartActivityMessage(String node) {
        Wearable.MessageApi.sendMessage(
            mGoogleApiClient, 
            node, 
            MessageConstant.PATH_START_ACTIVITY, 
            new byte[0])
        .setResultCallback(
            new ResultCallback<SendMessageResult>() {
                @Override
                public void onResult(SendMessageResult result) {
                    int code = result.getStatus().getStatusCode();
                    log_d("sendStartActivityMessage onResult: " + code );
                    notifyStartActivityResult( result );
                }
            }
        );
    }

    /**
     * getNodes
     */
    private Collection<String> getNodes() {
        HashSet<String> results = new HashSet<>();
        NodeApi.GetConnectedNodesResult nodes =
            Wearable.NodeApi.getConnectedNodes(mGoogleApiClient).await();
        for (Node node : nodes.getNodes()) {
            results.add(node.getId());
        }
        return results;
    }
    
    /**
     * sendSensorData
     * @param SensorRec rec
     */
    public void sendSensorData( SensorRec rec ) {
        log_d("sendSensorData");
        PutDataMapRequest req = PutDataMapRequest.create( MessageConstant.PATH_SENSOR);
        req.getDataMap().putLong( MessageConstant.KEY_TIMESTAMP, System.currentTimeMillis() );
        req.getDataMap().putInt( MessageConstant.KEY_TIME, rec.time );
        req.getDataMap().putFloat( MessageConstant.KEY_TEMPERATURE, rec.temperature );
        req.getDataMap().putFloat( MessageConstant.KEY_HUMIDITY, rec.humidity );
        req.getDataMap().putFloat( MessageConstant.KEY_PRESSURE, rec.pressure );
        req.getDataMap().putFloat( MessageConstant.KEY_LIGHT, rec.light );
        req.getDataMap().putFloat( MessageConstant.KEY_NOISE, rec.noise );        
        PutDataRequest request = req.asPutDataRequest();
        request.setUrgent();

        Wearable.DataApi.putDataItem(mGoogleApiClient, request)
            .setResultCallback(new ResultCallback<DataItemResult>() {
                @Override
                public void onResult(DataItemResult result) {
                    boolean isSuccess = result.getStatus().isSuccess();
                    log_d("sendSensorData onResult: " + isSuccess);
                    notifySendSensorResult(result);
                }
            });
    }
                           
    /**
     * log_d
     */
    private static void log_d(String str) {
        if (Constant.DEBUG) Log.d(Constant.TAG, TAG_SUB + " " + str);
    }

    /**
     * class StartWearableActivityTask
     */
    private class StartWearableActivityTask extends AsyncTask<Void, Void, Void> {
        /**
         * doInBackground
         */
        @Override
        protected Void doInBackground(Void... args) {
            Collection<String> nodes = getNodes();
            for (String node : nodes) {
                sendStartActivityMessage(node);
            }
            return null;
        }
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
     * notifyMessageReceived
     */
    private void notifyCapabilityChanged(CapabilityInfo Info) {
        if ( mListener != null ) {
            mListener.onCapabilityChanged(Info);
        }
    }

    /**
     * notifyMessageReceived
     */             
    private void notifyStartActivityResult( SendMessageResult result ) {
        if ( mListener != null ) {
            mListener.onStartActivityResult(result);
        }
    }

    /**
     * notifySendSensorResult
     */         
    private void notifySendSensorResult( DataItemResult result ) {
        if ( mListener != null ) {
            mListener.onSendSensorResult(result);
        }
    }
                                        
}
