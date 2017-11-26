/**
 * fab sensor line chart 
 * 2017-11-01 K.OHWADA
 */

package jp.ohwada.android.fabsensorlinechart;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileDescriptor;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.List;

import android.content.Context;
import android.content.res.AssetFileDescriptor;
import android.content.res.AssetManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Environment;
import android.util.DisplayMetrics;
import android.util.Log;

/**
 * File Utility
 */
public class FileUtility {
	
	// dubug
	private final static boolean D = Constant.DEBUG; 
	private final static String TAG_SUB = "MyFileUtility";
					 
	private AssetManager mAssetManager;

		
	/**
     * === constractor ===
	 * @ param Context context
	 */	    
	 public FileUtility( Context context  ) {
		mAssetManager = context.getAssets();
	} //  constractor

	
	/**
     * readAssets
	 * @ param String fileName
	 */	
public String readAssets( String fileName ) {
	
String text = "";
BufferedReader br = null;

InputStream is = getAssetsInputStream( fileName );
if ( is == null ) return text;

  String str;       
try {
        br = new BufferedReader(new InputStreamReader(is));
       
        // read line one by one
        while ((str = br.readLine()) != null) {
            text += str + "\n";
        } // while
        
} catch (Exception e){
    			if (D) e.printStackTrace();
} // try

    try {
        if (is != null) is.close();
        if (br != null) br.close();
} catch (Exception e){
    			if (D) e.printStackTrace();
} // try

	return text;
} // read

	
	/**
	 * getAssetsInputStream
	 */ 	
	private InputStream getAssetsInputStream( String fileName ) {
		
		InputStream is = null;
		try {
			is = mAssetManager.open(fileName);
		} catch (IOException e) {
			if (D) e.printStackTrace();
		} 
		
	return is;
} //getAssetsInputStream

		

 	/**
	 * write into logcat
	 */ 
	private void log_d( String msg ) {
	    if (Constant.DEBUG) Log.d( Constant.TAG, TAG_SUB + " " + msg );
	} // log_d


} // class FileUtility