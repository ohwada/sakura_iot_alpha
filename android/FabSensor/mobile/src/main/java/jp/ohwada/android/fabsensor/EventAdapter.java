/**
 * Fab Sensor
 * 2016-11-01 K.OHWADA
 */
package jp.ohwada.android.fabsensor;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

/**
 * EventAdapter
 * A View Adapter for presenting the EventRec objects in a list
 */
public class EventAdapter extends ArrayAdapter<EventRec> {

    private final Context mContext;

    /**
     * Constractor
     * @param Context context
     * @param int unusedResource     
     */
    public EventAdapter( Context context, int unusedResource ) {
        super(context, unusedResource);
        mContext = context;
    }

    /**
     * === getView ===
     */
    @Override
    public View getView(int position, View view, ViewGroup parent ) {
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
        EventRec event = getItem(position);
        holder.title.setText(event.title);
        holder.text.setText(event.text);
        return view;
    }

    /**
     * class Holder
     */
    private class Holder {
        TextView title;
        TextView text;
    }
}
