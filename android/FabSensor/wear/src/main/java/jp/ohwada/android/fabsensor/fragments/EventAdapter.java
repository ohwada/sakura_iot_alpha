/**
 * Fab Sensor
 * 2016-11-01 K.OHWADA
 */
package jp.ohwada.android.fabsensor.fragments;

import android.content.Context;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import jp.ohwada.android.fabsensor.Constant;

/**
 * EventAdapter
 */
public class EventAdapter extends ArrayAdapter<EventRec> {

   // debug
    private static final String TAG_SUB = EventAdapter.class.getSimpleName();
    
    private final Context mContext;

    /**
     * Constractor
     * @param Context context
     * @param int resource
     */
    public EventAdapter(Context context, int resource) {
        super(context, resource);
        mContext = context;
    }

    /**
     * === getView ===
     */
    @Override
    public View getView( int position, View view, ViewGroup parent ) {
        Holder holder;
        if (view == null) {
            holder = new Holder();
            LayoutInflater inflater = (LayoutInflater) mContext.getSystemService(
                Context.LAYOUT_INFLATER_SERVICE);
            view = inflater.inflate(android.R.layout.two_line_list_item, null);
            view.setTag(holder);
            holder.title = (TextView) view.findViewById(android.R.id.text1);
            holder.text = (TextView) view.findViewById(android.R.id.text2);
        } else {
            holder = (Holder) view.getTag();
        }
        EventRec rec = getItem(position);
        holder.title.setText(rec.title);
        holder.text.setText(rec.text);
        return view;
    }

    /**
     * append
     * @param String title
     * @param String text
     */
    public void append(String title, String text) {
        log_d("append");
        add( new EventRec(title, text) );
    }

    /**
     * log_d
     */
    private static void log_d(String str) {
        if (Constant.DEBUG) Log.d(Constant.TAG, TAG_SUB + " " + str);
    }

    /**
     * class Holder
     */
    private class Holder {
        TextView title;
        TextView text;
    }
}
