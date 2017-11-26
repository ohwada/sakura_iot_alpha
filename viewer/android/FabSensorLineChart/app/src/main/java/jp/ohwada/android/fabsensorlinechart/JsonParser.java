/**
 * fab sensor line chart 
 * 2017-11-01 K.OHWADA
 */

package jp.ohwada.android.fabsensorlinechart;

import android.util.Log;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

/*
 * JsonParser
 */ 
public class JsonParser {

   // debug
    private static final boolean D = Constant.DEBUG;
    private static final String TAG_SUB = JsonParser.class.getSimpleName();

    /**
     * JsonParser
     */
    public JsonParser() {
        // dummy
    }

    /**
     * parse
     * @param String text
     * @return parse result
     */
    public List<SensorRec> parse( String text ) {
        int num = -1;
        JSONArray items = null;
        try {
            JSONObject obj = new JSONObject( text );
            num = obj.getInt("num");
            if ( obj.has("items") ){ 
                items = obj.getJSONArray("items");
            }
        } catch (JSONException e) {
            if (D) e.printStackTrace();
        }

        if ( items != null ) {
            return parseItems( items );
        }
        
        List<SensorRec> list = new ArrayList<SensorRec>();
        return list;
    }

    /**
     * parseArray
     */
    private List<SensorRec> parseItems( JSONArray array ) {
        List<SensorRec> list = new ArrayList<SensorRec>();
        for (int i = 0; i < array.length(); i++) {
            try {
                JSONObject obj = array.getJSONObject(i);
                SensorRec item = new SensorRec();
                item.time = obj.getInt("time");
                item.temperature = (float)obj.getDouble("temperature");
                item.humidity = (float)obj.getDouble("humidity");
                item.pressure = (float)obj.getDouble("pressure");                                        
                item.light = (float)obj.getDouble("light");                                                                                                                       
                item.noise = (float)obj.getDouble("noise");
                list.add( item );   
            } catch (JSONException e) {
                if (D) e.printStackTrace();
            }
        }
        return list;
    }

    /**
     * log_d
     */
    private static void log_d(String str) {
        if (Constant.DEBUG) Log.d(Constant.TAG, TAG_SUB + " " + str);
    }

}
