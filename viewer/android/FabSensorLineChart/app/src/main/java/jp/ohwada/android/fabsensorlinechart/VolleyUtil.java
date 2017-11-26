/**
 * fab sensor line chart 
 * 2017-11-01 K.OHWADA
 */

package jp.ohwada.android.fabsensorlinechart;

import android.content.Context;
import android.util.Log;

import com.android.volley.Network;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.BasicNetwork;
import com.android.volley.toolbox.DiskBasedCache;
import com.android.volley.toolbox.HurlStack;
import com.android.volley.toolbox.StringRequest;

import java.io.File;

/*
 * VolleyUtil
 */ 
public class VolleyUtil {

   // debug
    private static final String TAG_SUB = VolleyUtil.class.getSimpleName();

    private static final String REQ_TAG = "volley";

    private static final String DEFAULT_CACHE_DIR = "volley";
    private static final int CACHE_SIZE = 16 * 1024 * 1024;  // 16 MB

    private RequestQueue mQueue;
    private String mUrl;

    // callback 
    private OnChangedListener mListener;  

    /*
     * callback interface
     */    
    public interface OnChangedListener {
        void onResponse( int mode, String response );
        void onErrorResponse( String error );
    }

    /*
     * callback
     */ 
    public void setOnChangedListener( OnChangedListener listener ) {
        mListener = listener;
    }

    /**
     * Constractor
     * @param Context context
     */
    public VolleyUtil( Context context ) {
        mQueue = newRequestQueue(context, CACHE_SIZE);
    }
    
    /**
     * newRequestQueue
     */
    private static RequestQueue newRequestQueue(Context context, int cacheSize) {
        File cacheDir = new File(context.getCacheDir(), DEFAULT_CACHE_DIR);
        Network network = new BasicNetwork(
            new HurlStack());
        RequestQueue queue = new RequestQueue(
            new DiskBasedCache(cacheDir, cacheSize),
            network);
        return queue;
    }

   /**
     * start
     */
    public void start() {
        log_d("start");
        mQueue.start();
    }

   /**
     * stop
     */
    public void stop() {
        log_d("stop");
        mQueue.stop();
    }

   /**
     * cancel
     */
    public void cancel() {
        log_d("cancel");
        mQueue.cancelAll(REQ_TAG);
    }

    /**
     * setUrl
     * @param String url
     */
    public void setUrl( String url ) {
       mUrl = url;
    }

    /**
     * request
     * @param int mode
     */
    public void request(int mode) {
       requestServer( mUrl, mode );
    }

    /**
     * requestServer
     * @param String url
     * @param int mode
     */
    public void requestServer( String url, int mode ) {
        log_d("requestServer " + url);
        final int final_mode = mode;
        StringRequest request =
            new StringRequest( 
                Request.Method.GET, 
                url, 
                new Response.Listener<String>() {
                    @Override
                    public void onResponse( String response ) {
                        log_d("onResponse");
                        notifyResponse( final_mode, response );
                    }
                },
                new Response.ErrorListener() {
                    @Override 
                    public void onErrorResponse( VolleyError e ) {
                        String msg = e.getMessage();
                        if ( msg == null ) {
                            msg = "Timeout";
                        }
                        log_d( msg );
                        notifyErrorResponse( msg );
                    }
                }
            );
        request.setTag( REQ_TAG );
        mQueue.add( request );
    }

    /**
     * notifyResponse
     */
    private void notifyResponse( int mode, String response ) {
        log_d("notifyResponse");
        if ( mListener != null ) {
            mListener.onResponse( mode, response );
        }
    }

    /**
     * notifyErrorResponse
     */
    private void notifyErrorResponse( String error ) {
        if ( mListener != null ) {
            mListener.onErrorResponse( error );
        }
    }

    /**
     * log_d
     */
    private void log_d( String str ) {
        if (Constant.DEBUG) Log.d( Constant.TAG, TAG_SUB + " " + str );
    }

}
