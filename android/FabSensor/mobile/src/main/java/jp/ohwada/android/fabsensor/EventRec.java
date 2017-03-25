/**
 * Fab Sensor
 * 2016-11-01 K.OHWADA
 */
package jp.ohwada.android.fabsensor;

/**
 * EventRec
 */
public class EventRec {
    String title = "";
    String text = "";

    /**
     * Constractor
     * @param String title
     * @param String text
     */
    public EventRec( String _title, String _text ) {
        this.title = _title;
        this.text = _text;
    }
}