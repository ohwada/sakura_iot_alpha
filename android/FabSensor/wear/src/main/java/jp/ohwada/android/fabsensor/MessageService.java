/**
 * Fab Sensor
 * 2016-11-01 K.OHWADA
 */
package jp.ohwada.android.fabsensor;

import android.content.Intent;
import android.net.Uri;
import android.util.Log;

import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.wearable.DataEvent;
import com.google.android.gms.wearable.DataEventBuffer;
import com.google.android.gms.wearable.MessageEvent;
import com.google.android.gms.wearable.Wearable;
import com.google.android.gms.wearable.WearableListenerService;

import java.util.concurrent.TimeUnit;

/**
 * MessageService
 * Listens to DataItems and Messages from the local node.
 */
public class MessageService extends WearableListenerService {

   // debug
    private static final String TAG_SUB = MessageService.class.getSimpleName();
    
    private static final long CONNECT_TIMEOUT = 30;
            
    private GoogleApiClient mGoogleApiClient;

    /*
     * === onCreate ===
     */ 
    @Override
    public void onCreate() {
        log_d("onCreate");
        super.onCreate();
        mGoogleApiClient = new GoogleApiClient.Builder(this)
            .addApi(Wearable.API)
            .build();
        mGoogleApiClient.connect();
    }

    /*
     * === onDataChanged ===
     */
    @Override
    public void onDataChanged(DataEventBuffer buffer) {
        log_d("onDataChanged");

        // connect, if not connected
        if (!mGoogleApiClient.isConnected() || !mGoogleApiClient.isConnecting()) {
            ConnectionResult result = mGoogleApiClient.blockingConnect(
                CONNECT_TIMEOUT, TimeUnit.SECONDS);
            if (!result.isSuccess()) {
                log_d("onDataChanged: connect failed: " + result.getErrorCode() );
                return;
            }
        }

        // Loop through the events and send a message back to the node that created the data item.
        for (DataEvent event : buffer) {
            int type = event.getType();
            String path = event.getDataItem().getUri().getPath();
            log_d("onDataChanged: " + type + " " + path);
            if ( MessageConstant.PATH_SENSOR.equals(path)) {
                sendSensorMessage(event);
            }
        }
    }

    /*
     * sendSensorMessage
     */
    private void sendSensorMessage(DataEvent event) {
        Uri uri = event.getDataItem().getUri();
        // Get the node id of the node that created the data item from the host portion of the uri.
        String nodeId = uri.getHost();
        // Set the data of the message to be the bytes of the Uri.
        byte[] payload = uri.toString().getBytes();
        // Send the rpc
        Wearable.MessageApi.sendMessage(
            mGoogleApiClient, 
            nodeId,
            MessageConstant.PATH_DATA_ITEM_RECEIVED, 
            payload );
    }
                    
    /*
     * === onMessageReceived ===
     */
    @Override
    public void onMessageReceived(MessageEvent event) {
        String path = event.getPath();
        log_d("onMessageReceived " + path);
        // Check to see if the message is to start an activity
        if ( MessageConstant.PATH_START_ACTIVITY.equals(path) ) {
            startMainActivity();
        }
    }

    /*
     * startMainActivity
     */
    private void startMainActivity() {
        Intent intent = new Intent(this, MainActivity.class);
        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        startActivity(intent);
    }
            
    /**
     * log_d
     */
    private static void log_d(String str) {
        if (Constant.DEBUG) Log.d(Constant.TAG, TAG_SUB + " " + str);
    }

}