/**
 * Fab Sensor
 * 2016-11-01 K.OHWADA
 */
package jp.ohwada.android.fabsensor;

import android.app.Fragment;
import android.app.FragmentManager;
import android.support.wearable.view.FragmentGridPagerAdapter;

import java.util.List;

/**
 * SensorPagerAdapter
 */     
public class SensorPagerAdapter extends FragmentGridPagerAdapter {

    private List<Fragment> mFragments;

    /**
      * Constractor
      */ 
    public SensorPagerAdapter(FragmentManager fm, List<Fragment> fragments) {
        super(fm);
        mFragments = fragments;
    }

    /**
      * === getRowCount ===
      */ 
    @Override
    public int getRowCount() {
        return 1;
    }

    /**
      * === getColumnCount ===
      */ 
    @Override
    public int getColumnCount(int row) {
        return mFragments == null ? 0 : mFragments.size();
    }

    /**
      * === getFragment ===
      */ 
    @Override
    public Fragment getFragment(int row, int column) {
        return mFragments.get(column);
    }
    
}
