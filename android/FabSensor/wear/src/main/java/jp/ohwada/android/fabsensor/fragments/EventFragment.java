/**
 * Fab Sensor
 * 2016-11-01 K.OHWADA
 */
package jp.ohwada.android.fabsensor.fragments;

import android.app.Fragment;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ListView;

import jp.ohwada.android.fabsensor.Constant;
import jp.ohwada.android.fabsensor.R;

/**
 * EventFragment
 * A fragment that shows a list of DataItems received from the phone
 */
public class EventFragment extends Fragment {

   // debug
    private static final String TAG_SUB = EventFragment.class.getSimpleName();

    private EventAdapter mAdapter;
    private boolean isInitialized = false;

    /**
     * === onCreateView ===
     */
    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_event_round, container, false);
        ListView listView = (ListView) view.findViewById(R.id.ListView_event);
        mAdapter = new EventAdapter( getActivity(), android.R.layout.simple_list_item_1 );
        listView.setAdapter(mAdapter);
        isInitialized = true;
        return view;
    }

    /**
     * append
     * @param String title
     * @param String text
     */
    public void append(String title, String text) {
        log_d("append");
        if (!isInitialized) {
            return;
        }
        mAdapter.append( title, text );
    }

    /**
     * log_d
     */
    private static void log_d(String str) {
        if (Constant.DEBUG) Log.d(Constant.TAG, TAG_SUB + " " + str);
    }
    
}
